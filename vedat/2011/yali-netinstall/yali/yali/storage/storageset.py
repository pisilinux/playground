#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import errno
import gettext

__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import yali.util
import yali.context as ctx
from yali.storage import StorageError
from yali.storage.devices.directorydevice import DirectoryDevice
from yali.storage.devices.filedevice import FileDevice
from yali.storage.devices.opticaldevice import OpticalDevice
from yali.storage.devices.nodevice import NoDevice
from yali.storage.devices.device import Device, DeviceError
from yali.storage.formats import getFormat, get_device_format
from yali.storage.formats.filesystem import FilesystemError
from yali.storage.library import devicemapper
from yali.storage.library import swap

from pardus import fstabutils

class StorageSetError(StorageError):
    pass

class FSTabError(StorageSetError):
    pass

class FSTabEntryError(StorageSetError):
    pass

class BlkidTabError(StorageError):
    pass

class CryptTabError(StorageError):
    pass

def get_containing_device(path, devicetree):
    """ Return the device that a path resides on. """
    if not os.path.exists(path):
        return None

    st = os.stat(path)
    major = os.major(st.st_dev)
    minor = os.minor(st.st_dev)
    link = "/sys/dev/block/%s:%s" % (major, minor)
    if not os.path.exists(link):
        return None

    try:
        device_name = os.path.basename(os.readlink(link))
    except Exception:
        return None

    if device_name.startswith("dm-"):
        device_name = devicemapper.name_from_dm_node(device_name)

    return devicetree.getDeviceByName(device_name)

class BlkidTab(object):
    """ Dictionary-like interface to blkid.tab with device path keys """
    def __init__(self, chroot="/"):
        self.devices = {}
        self.path = os.path.join(chroot, "etc/blkid/blkid.tab")

    def parse(self):
        with open(self.path) as blkidTab:
            for line in blkidTab.readlines():
                # this is pretty ugly, but an XML parser is more work than
                # is justifiable for this purpose
                if not line.startswith("<device "):
                    continue

                line = line[len("<device "):-len("</device>\n")]
                (data, sep, device) = line.partition(">")
                if not device:
                    continue

                self.devices[device] = {}
                for pair in data.split():
                    try:
                        (key, value) = pair.split("=")
                    except ValueError:
                        continue

                    self.devices[device][key] = value[1:-1] # strip off quotes

    def __getitem__(self, key):
        return self.devices[key]

    def get(self, key, default=None):
        return self.devices.get(key, default)

class CryptTab(object):
    """ Dictionary-like interface to crypttab entries with map name keys """
    def __init__(self, devicetree, blkidTab=None, chroot=""):
        self.devicetree = devicetree
        self.blkidTab = blkidTab
        self.chroot = chroot
        self.mappings = {}

    def parse(self, chroot=""):
        """ Parse /etc/crypttab from an existing installation. """
        if not chroot or not os.path.isdir(chroot):
            chroot = ""

        path = "%s/etc/crypttab" % chroot
        ctx.logger.debug("parsing %s" % path)
        with open(path) as crypttab:
            if not self.blkidTab:
                try:
                    self.blkidTab = BlkidTab(chroot=chroot)
                    self.blkidTab.parse()
                except Exception:
                    self.blkidTab = None

            for line in crypttab.readlines():
                (line, pound, comment) = line.partition("#")
                fields = line.split()
                if not 2 <= len(fields) <= 4:
                    continue
                elif len(fields) == 2:
                    fields.extend(['none', ''])
                elif len(fields) == 3:
                    fields.append('')

                (name, devspec, keyfile, options) = fields

                # resolve devspec to a device in the tree
                device = self.devicetree.resolveDevice(devspec,
                                                       blkidTab=self.blkidTab)
                if device:
                    self.mappings[name] = {"device": device,
                                           "keyfile": keyfile,
                                           "options": options}

    def populate(self):
        """ Populate the instance based on the device tree's contents. """
        for device in self.devicetree.devices:
            # XXX should we put them all in there or just the ones that
            #     are part of a device containing swap or a filesystem?
            #
            #       Put them all in here -- we can filter from FSSet
            if device.format.type != "luks":
                continue

            key_file = device.format.keyFile
            if not key_file:
                key_file = "none"

            options = device.format.options
            if not options:
                options = ""

            self.mappings[device.format.mapName] = {"device": device,
                                                    "keyfile": key_file,
                                                    "options": options}

    def crypttab(self):
        """ Write out /etc/crypttab """
        crypttab = ""
        for name in self.mappings:
            entry = self[name]
            crypttab += "%s UUID=%s %s %s\n" % (name,
                                                entry['device'].format.uuid,
                                                entry['keyfile'],
                                                entry['options'])
        return crypttab                       

    def __getitem__(self, key):
        return self.mappings[key]

    def get(self, key, default=None):
        return self.mappings.get(key, default)

class StorageSet(object):
    _bootFSTypes = ["ext4", "ext3", "ext2"]
    def __init__(self, devicetree, rootpath):
        self.devicetree = devicetree
        self.rootpath = rootpath
        self.active = False
        self._dev = None
        self._debugfs = None
        self._sysfs = None
        self._proc = None
        self._devshm = None
        self.preserveLines = []
        self.blkidTab = None
        self.cryptTab = None

    @property
    def devices(self):
        return sorted(self.devicetree.devices, key=lambda d: d.path)

    @property
    def dev(self):
        if not self._dev:
            self._dev = DirectoryDevice("/dev", format=getFormat("bind",
                                                                 device="/dev",
                                                                 mountpoint="/dev",
                                                                 exists=True),
                                        exists=True)

        return self._dev
    @property
    def sysfs(self):
        if not self._sysfs:
            self._sysfs = NoDevice(format=getFormat("sysfs",
                                                    device="sys",
                                                    mountpoint="/sys"))
        return self._sysfs

    @property
    def debugfs(self):
        if not self._debugfs:
            self._debugfs = NoDevice(format=getFormat("debugfs",
                                                     device="debugfs",
                                                     mountpoint="/sys/kernel/debug"))
        return self._debugfs

    @property
    def proc(self):
        if not self._proc:
            self._proc = NoDevice(format=getFormat("proc",
                                                   device="proc",
                                                   mountpoint="/proc"))
        return self._proc

    @property
    def devshm(self):
        if not self._devshm:
            self._devshm = NoDevice(format=getFormat("tmpfs",
                                                     device="tmpfs",
                                                     mountpoint="/dev/shm"))
        return self._devshm

    @property
    def mountpoints(self):
        filesystems = {}
        for device in self.devices:
            if device.format.mountable and device.format.mountpoint:
                filesystems[device.format.mountpoint] = device
        return filesystems

    def mountFilesystems(self, readOnly=None, skipRoot=False):
        devices = self.mountpoints.values() + self.swapDevices
        devices.extend([self.dev, self.sysfs, self.proc])
        devices.sort(key=lambda d: getattr(d.format, "mountpoint", None))

        for device in devices:
            if not device.format.mountable or not device.format.mountpoint:
                continue

            if skipRoot and device.format.mountpoint == "/":
                continue

            options = device.format.options
            if "noauto" in options.split(","):
                continue

            if device.format.type == "bind" and device != self.dev:
                # set up the DirectoryDevice's parents now that they are
                # accessible
                #
                # -- bind formats' device and mountpoint are always both
                #    under the chroot. no exceptions. none, damn it.
                targetDir = "%s/%s" % (ctx.consts.target_dir, device.path)
                parent = get_containing_device(targetDir, self.devicetree)
                if not parent:
                    ctx.logger.error("cannot determine which device contains "\
                                     "directory %s" % device.path)
                    device.parents = []
                    self.devicetree._removeDevice(device)
                    continue
                else:
                    device.parents = [parent]

            try:
                device.setup()
            except Exception as msg:
                continue

            if readOnly:
                options = "%s,%s" % (options, readOnly)

            try:
                device.format.setup(options=options,
                                    chroot=ctx.consts.target_dir)
            except OSError as msg:
                ctx.logger.error("OSError: (%d) %s" % (msg.errno, msg.strerror))

                if ctx.interface.messageWindow:
                    if msg.errno == errno.EEXIST:
                        ctx.interface.messageWindow(_("Invalid mount point"),
                                                    _("An error occurred when trying "
                                                      "to create %s.  Some element of "
                                                      "this path is not a directory. "
                                                      "This is a fatal error and the "
                                                      "install cannot continue.\n\n"
                                                      "Press <Enter> to exit the "
                                                      "installer.")
                                                    % (device.format.mountpoint,),
                                                    type="error")
                    else:
                        na = {'mountpoint': device.format.mountpoint,
                              'msg': msg.strerror}
                        ctx.interface.messageWindow(_("Invalid mount point"),
                                                    _("An error occurred when trying "
                                                      "to create %(mountpoint)s: "
                                                      "%(msg)s.  This is "
                                                      "a fatal error and the install "
                                                      "cannot continue.\n\n"
                                                      "Press <Enter> to exit the "
                                                      "installer.") % na,
                                                    type="error")
                    sys.exit(2)


            except SystemError as (num, msg):
                ctx.logger.error("SystemError: (%d) %s" % (num, msg) )

                if ctx.interface.messageWindow and not device.format.linuxNative:
                    na = {'path': device.path,
                          'mountpoint': device.format.mountpoint}
                    ret = ctx.interface.messageWindow(_("Unable to mount filesystem"),
                                                 _("An error occurred mounting "
                                                   "device %(path)s as "
                                                   "%(mountpoint)s.  You may "
                                                   "continue installation, but "
                                                   "there may be problems.") % na,
                                                   type="custom", customIcon="warning",
                                                   customButtons=[_("Exit installer"), _("Continue")])

                    if ret == 0:
                        sys.exit(2)
                    else:
                        continue

            except FilesystemError as msg:
                ctx.logger.error("FilesystemError: %s" % msg)

                if ctx.interface.messageWindow:
                    na = {'path': device.path,
                          'mountpoint': device.format.mountpoint,
                          'msg': msg}
                    ctx.interface.messageWindow(_("Unable to mount filesystem"),
                                                _("An error occurred mounting "
                                                  "device %(path)s as %(mountpoint)s: "
                                                  "%(msg)s. This is "
                                                  "a fatal error and the install "
                                                  "cannot continue.\n\n"
                                                  "Press <Enter> to exit the "
                                                  "installer.") % na,
                                                type="error")
                    sys.exit(2)

        self.active = True

    def umountFilesystems(self, swapoff=True):
        devices = self.mountpoints.values() + self.swapDevices
        devices.extend([self.dev, self.sysfs, self.proc])
        devices.sort(key=lambda d: getattr(d.format, "mountpoint", None))
        devices.reverse()
        for device in devices:
            if not device.format.mountable and \
               (device.format.type != "swap" or swapoff):
                continue

            device.format.teardown()
            device.teardown()

        self.active = False

    def turnOnSwap(self):
        def swapError(msg, device):
            if not ctx.interface.messageWindow:
                sys.exit(2)

            ret = ctx.interface.messageWindow(_("Error"),
                                              msg,
                                              type="custom",
                                              customButtons=[_("Skip"),
                                                             _("Format"),
                                                             _("Exit")],
                                              customIcon="error")

            if ret == 0:
                self.devicetree._removeDevice(device)
                return False
            elif ret == 1:
                device.format.create(force=True)
                return True
            else:
                sys.exit(2)

        for device in self.swapDevices:
            if isinstance(device, FileDevice):
                targetDir = "%s/%s" % (self.rootPath, device.path)
                parent = get_containing_device(targetDir, self.devicetree)
                if not parent:
                    ctx.logger.error("cannot determine which device contains "
                                     "directory %s" % device.path)
                    device.parents = []
                    self.devicetree._removeDevice(device)
                    continue
                else:
                    device.parents = [parent]

            while True:
                try:
                    device.setup()
                    device.format.setup()
                except swap.OldSwapError:
                    msg = _("The swap device:\n\n     %s\n\n"
                            "is an old-style Linux swap partition.  If "
                            "you want to use this device for swap space, "
                            "you must reformat as a new-style Linux swap "
                            "partition.") \
                          % device.path

                    if swapError(msg, device):
                        continue

                except swap.SuspendError:
                    msg = _("The swap device:\n\n     %s\n\n"
                                "in your /etc/fstab file is currently in "
                                "use as a software suspend device, "
                                "which means your system is hibernating. "
                                "If you are performing a new install, "
                                "make sure the installer is set "
                                "to format all swap devices.") \
                              % device.path

                    if swapError(msg, device):
                        continue

                except swap.UnknownSwapError:
                    msg = _("The swap device:\n\n     %s\n\n"
                            "does not contain a supported swap volume.  In "
                            "order to continue installation, you will need "
                            "to format the device or skip it.") \
                          % device.path

                    if swapError(msg, device):
                        continue

                except DeviceError as (msg, name):
                    if ctx.interface.messageWindow:
                        error = _("Error enabling swap device %(name)s: "
                                  "%(msg)s<br><br>"
                                  "This most likely means this swap "
                                  "device has not been initialized.<br><br>"
                                  "Press OK to exit the installer.") % \
                                {'name': name, 'msg': msg}
                        ctx.interface.messageWindow(_("Error"),
                                                    error,
                                                    type="error")
                    sys.exit(2)

                break

    def createSwapFile(self, device, size, rootPath=None):
        """ Create and activate a swap file under rootPath. """
        if not rootPath:
            rootPath = self.rootpath

        filename = "/SWAP"
        count = 0
        basedir = os.path.normpath("%s/%s" % (rootPath, device.format.mountpoint))
        while os.path.exists("%s/%s" % (basedir, filename)) or \
              self.devicetree.getDeviceByName(filename):
            file = os.path.normpath("%s/%s" % (basedir, filename))
            count += 1
            filename = "/SWAP-%d" % count

        dev = FileDevice(filename,
                         size=size,
                         parents=[device],
                         format=getFormat("swap", device=filename))
        dev.create()
        dev.setup()
        dev.format.create()
        dev.format.setup()
        self.devicetree._addDevice(dev)

    @property
    def bootFilesystemTypes(self):
        return self._bootFSTypes

    def checkBootRequest(self, request):
        """Perform an architecture-specific check on the boot device.  Not all
           platforms may need to do any checks.  Returns a list of errors if
           there is a problem, or [] otherwise."""
        errors = []

        if not request:
            return [_("You have not created a bootable partition.")]

        # can't have bootable partition on LV
        if request.type == "lvmlv":
            errors.append(_("Bootable partitions cannot be on a logical volume."))

        # can't have bootable partition on Raid Array
        if request.type == "mdarray":
            errors.append(_("Bootable partitions cannot be on a raid array."))

        # Make sure /boot is on a supported FS type.  This prevents crazy
        # things like boot on vfat.
        if not request.format.bootable or \
           (getattr(request.format, "mountpoint", None) == "/boot" and
            request.format.type not in self.bootFilesystemTypes):
            errors.append(_("Bootable partitions cannot be on an %s filesystem.") % request.format.type)

        return errors

    @property
    def bootDevice(self):
        def mountDict():
            """Return a dictionary mapping mount points to devices."""
            ret = {}
            for device in [d for d in self.devices if d.format.mountable]:
                if device.format.mountpoint:
                    ret[device.format.mountpoint] = device

            return ret

        _mountpoints = mountDict()
        if yali.util.isEfi():
            return _mountpoints.get("/boot/efi")
        else:
            return _mountpoints.get("/boot", _mountpoints.get("/"))

    @property
    def rootDevice(self):
        for path in ["/", self.rootpath]:
            for device in self.devices:
                try:
                    mountpoint = device.format.mountpoint
                except AttributeError:
                    mountpoint = None

                if mountpoint == path:
                    return device

    @property
    def swapDevices(self):
        swaps = []
        swaps = [d for d in self.devices if d.format.type == "swap"]
        swaps.sort(key=lambda d: d.name)
        return swaps

    def fstab(self):
        format = "%-23s %-23s %-7s %-15s %d %d\n"
        fstab = """
#
# Created by YALI on %s
#
""" % time.asctime()

        devices = sorted(self.mountpoints.values(),
                         key=lambda d: d.format.mountpoint)
        devices += self.swapDevices
        devices.extend([self.devshm, self.debugfs, self.sysfs, self.proc])
        for device in devices:
            # why the hell do we put swap in the fstab, anyway?
            if not device.format.mountable and device.format.type != "swap":
                continue

            # Don't write out lines for optical devices, either.
            if isinstance(device, OpticalDevice):
                continue

            fstype = getattr(device.format, "mountType", device.format.type)
            if fstype == "swap":
                mountpoint = "swap"
                options = device.format.options
            else:
                mountpoint = device.format.mountpoint
                options = device.format.options
                if not mountpoint:
                    ctx.logger.warning("%s filesystem on %s has no mountpoint" % \
                                                            (fstype,
                                                             device.path))
                    continue

            options = options or "defaults"
            devspec = device.fstabSpec
            dump = device.format.dump
            if device.format.check and mountpoint == "/":
                passno = 1
            elif device.format.check:
                passno = 2
            else:
                passno = 0
            fstab = fstab + device.fstabComment
            fstab = fstab + format % (devspec, mountpoint, fstype, options, dump, passno)

            for line in self.preserveLines:
                fstab += line

        return fstab

    def write(self, installPath):
        """ write out all config files based on the set of filesystems """
        if not installPath:
            installPath = self.rootpath

        # /etc/fstab
        fstabPath = os.path.normpath("%s/etc/fstab" % installPath)
        fstab = self.fstab()
        open(fstabPath, "w").write(fstab)

    def _parseFSTabEntry(self, entry):
        if "noauto" in entry.get_fs_mntopts():
            ctx.logger.error("ignoring noauto entry")
            raise FSTabEntryError(_("Ignoring noauto entry"))

        devspec =  entry.get_fs_spec()
        mountpoint = entry.get_fs_file()
        fstype = entry.get_fs_vfstype()
        options = entry.get_fs_mntopts()
        dump = entry.get_fs_freq()
        passno = entry.get_fs_passno()

        # find device in the tree
        device = self.devicetree.resolveDevice(devspec,
                                               cryptTab=self.cryptTab,
                                               blkidTab=self.blkidTab)
        if device:
            # fall through to the bottom of this block
            pass
        elif devspec.startswith("/dev/loop"):
            # FIXME: create devices.LoopDevice
            ctx.logger.warning("completely ignoring your loop mount")
        elif ":" in devspec and fstype.startswith("nfs"):
            # NFS -- preserve but otherwise ignore
            ctx.logger.info("Skipping unsupported NFS Device.")
            return None
        elif devspec.startswith("/") and fstype == "swap":
            # swap file
            device = FileDevice(devspec,
                                parents=get_containing_device(devspec, self.devicetree),
                                format=getFormat(fstype, device=devspec,exists=True),
                                exists=True)
        elif fstype == "bind" or "bind" in options:
            # bind mount... set fstype so later comparison won't
            # turn up false positives
            fstype = "bind"

            # This is probably not going to do anything useful, so we'll
            # make sure to try again from FSSet.mountFilesystems. The bind
            # mount targets should be accessible by the time we try to do
            # the bind mount from there.
            parents = get_containing_device(devspec, self.devicetree)
            device = DirectoryDevice(devspec, parents=parents, exists=True)
            device.format = getFormat("bind",
                                      device=device.path,
                                      exists=True)
        elif mountpoint in ("/proc", "/sys", "/dev/shm", "/dev/pts",
                            "/selinux", "/proc/bus/usb"):
            ctx.logger.info("dropping %s mountpoint" % mountpoint)
            return None
        else:
            # nodev filesystem -- preserve or drop completely?
            format = getFormat(fstype)
            if devspec == "none" or \
               isinstance(format, get_device_format("nodev")):
                device = NoDevice(format=format)
            else:
                device = Device(devspec, format=format)

        if device is None:
            ctx.logger.error("failed to resolve %s (%s) from fstab" % (devspec, fstype))
            raise FSTabEntryError(_("Failed to resolve %s (%s) from fstab") % (devspec, fstype))

        fmt = getFormat(fstype, device=device.path)
        if fstype != "auto" and None in (device.format.type, fmt.type):
            ctx.logger.info("Unrecognized filesystem type for %s (%s)"
                     % (device.name, fstype))
            raise FSTabEntryError(_("Unrecognized filesystem type for %s (%s)") % (device.name, fstype))

        # make sure, if we're using a device from the tree, that
        # the device's format we found matches what's in the fstab
        ftype = getattr(fmt, "mountType", fmt.type)
        dtype = getattr(device.format, "mountType", device.format.type)
        if fstype != "auto" and ftype != dtype:
            raise StorageSetError(_("Scanned format (%s) differs from fstab format (%s)") % (dtype, ftype))
        del ftype
        del dtype

        if device.format.mountable:
            device.format.mountpoint = mountpoint
            device.format.options = options

        return device

    def parseFSTab(self, chroot=None):
        """
            All storage devices have been scanned, including filesystems
        """


        if not chroot or not os.path.isdir(chroot):
            chroot = ctx.consts.target_dir

        path = "%s/etc/fstab" % chroot
        if not os.access(path, os.R_OK):
            ctx.logger.info("cannot open %s for read" % path)
            raise FSTabError(_("Cannot open %s for read") % path)
        blkidTab = BlkidTab(chroot=chroot)
        try:
            blkidTab.parse()
        except Exception as e:
            ctx.logger.error("Parsing blkid.tab: %s" % e)
            blkidTab = None
        else:
            ctx.logger.debug("blkid.tab devs: %s" % blkidTab.devices.keys())

        cryptTab = CryptTab(self.devicetree, blkidTab=blkidTab, chroot=chroot)
        try:
            cryptTab.parse(chroot=chroot)
            ctx.logger.debug("crypttab maps: %s" % cryptTab.mappings.keys())
        except Exception as e:
            ctx.logger.info("error parsing crypttab: %s" % e)
            cryptTab = None

        self.blkidTab = blkidTab
        self.cryptTab = cryptTab

        fstab = fstabutils.Fstab(path)
        for entry in fstab.get_entries():

            try:
                device = self._parseFSTabEntry(entry)
            except FSTabEntryError:
                self.preserveLines.append(entry)
                continue
            except Exception as e:
                raise FSTabError(_("Fstab entry %s is malformed: %s") % (entry.get_fs_spec(), e))
            else:
                if not device:
                    continue

                if device not in self.devicetree.devices:
                    try:
                        self.devicetree._addDevice(device)
                    except ValueError:
                        self.preserveLines.append(entry)

    def crypttab(self):
        if not self.cryptTab:
            self.cryptTab = CryptTab(self.devicetree)
            self.cryptTab.populate()

        devices = self.mountpoints.values() + self.swapDevices

        # prune crypttab -- only mappings required by one or more entries
        for name in self.cryptTab.mappings.keys():
            keep = False
            mapInfo = self.cryptTab[name]
            cryptoDev = mapInfo['device']
            for device in devices:
                if device == cryptoDev or device.dependsOn(cryptoDev):
                    keep = True
                    break

            if not keep:
                del self.cryptTab.mappings[name]

        return self.cryptTab.crypttab()
