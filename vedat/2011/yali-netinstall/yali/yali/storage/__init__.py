#!/usr/bin/python
import os
import sys
import parted
import gettext
_ = gettext.translation('yali', fallback=True).ugettext

import yali
import yali.util
import yali.context as ctx
from yali.baseudev import udev_trigger

class StorageError(yali.Error):
    pass

from yali.storage.library import lvm
from yali.storage.devices.device import Device, DeviceError
from yali.storage.devices.partition import Partition
from yali.storage.devices.volumegroup import VolumeGroup
from yali.storage.devices.logicalvolume import LogicalVolume
from yali.storage.devices.raidarray import RaidArray
from yali.storage.formats import FormatError, getFormat, get_default_filesystem_type
from yali.storage.devicetree import DeviceTree, DeviceTreeError
from yali.storage.storageset import StorageSet, FSTabError
from yali.storage.operations import OperationCreateDevice, OperationCreateFormat, OperationDestroyFormat, OperationDestroyDevice, OperationDestroyFormat, OperationCreateFormat


def initialize(storage, intf):
    storage.shutdown()
    # touch /dev/.in_sysinit so that /lib/udev/rules.d/65-md-incremental.rules
    # does not mess with any mdraid sets
    open("/dev/.in_sysinit", "w")
    udev_trigger(subsystem="block", action="change")
    lvm.lvm_vg_blacklist = []
    storage.reset()

    check = storage.checkDisks(intf)
    if check == None:
        sys.exit(2)
    else:
        return check

def complete(storage, intf):
    returncode = False
    try:
        storage.devicetree.teardownAll()
    except DeviceTreeError, msg:
        ctx.logger.debug(_("Failed teardownAll in storage.complete with error:%s") % msg)
        return returncode

    title = None
    message = None
    details = None
    try:
        storage.doIt()
    except DeviceError as (msg, device):
        title = _("Storage Device Error")
        message = _("There was an error encountered while "
                    "partitioning on device %s.") % (device,)
        details = msg
        returncode = False
    except FormatError as (msg, device):
        title = _("Storage Format Error")
        message = _("There was an error encountered while "
                    "formatting on device %s.") % (device,)
        details = "%s" % (msg,)
        returncode = False
    else:
        ctx.logger.debug("Partitioning finished")
        returncode = True
    finally:
        if title:
            rc = intf.detailedMessageWindow(title, message, details,
                                            type="custom", customIcon="error",
                                            customButtons=[_("Exit installer"), _("Ignore")])
            if not rc:
                sys.exit(2)

    return returncode


def findExistingRootDevices(storage):
    """ Return a list of:
        all root filesystems with release strings in the device tree.
    """
    roots = []
    for device in storage.devicetree.leaves:
        if not device.format.linuxNative or not device.format.mountable:
            continue

        if device.protected:
            # can't upgrade the part holding hd: media so why look at it?
            continue

        try:
            device.setup()
        except DeviceError as e:
            ctx.logger.warning("setup of %s failed: %s" % (device.name, e))
            continue

        try:
            device.format.mount(options="ro", mountpoint=ctx.consts.tmp_mnt_dir)
        except FormatError as e:
            ctx.logger.warning("mount of %s as %s failed: %s" % (device.name,
                                                                 device.format.type, e))
            device.teardown()
            continue

        if os.access(os.path.join(ctx.consts.tmp_mnt_dir, "etc/fstab"), os.R_OK):
            release_str = yali.util.product_name(ctx.consts.tmp_mnt_dir)
            if release_str:
                roots.append((device, release_str))

        # this handles unmounting the filesystem
        device.teardown(recursive=True)

    return roots

def mountExistingSystem(storage, intf, rootDevice, allowDirty=None, warnDirty=None, readOnly=None):
    """ Mount filesystems specified in rootDevice's /etc/fstab file. """
    if readOnly:
        readOnly = "ro"
    else:
        readOnly = ""

        rootDevice.setup()
        rootDevice.format.mount(chroot=ctx.consts.target_dir,
                                mountpoint="/",
                                options=readOnly)

    try:
        storage.storageset.parseFSTab()
    except FSTabError, msg:
        ctx.logger.error("Parsing fstab file failed with:%s" % msg)
        rootDevice.format.unmount()
        rootDevice.teardown()
        return False
    except Exception, msg:
        ctx.logger.error("Unhandled exception:%s" % msg)
    else:
        dirtyDevs = []
        for device in storage.devices:
            if not hasattr(device.format, "isDirty"):
                continue

            try:
                device.setup()
            except DeviceError as e:
                # we'll catch this in the main loop
                continue

            if device.format.isDirty:
                ctx.logger.info("%s contains a dirty %s filesystem" % (device.path,
                                                                       device.format.type))
                dirtyDevs.append(device.path)

        if not allowDirty and dirtyDevs:
            intf.messageWindow(_("Dirty File Systems"),
                               _("The following file systems for your Linux system "
                                 "were not unmounted cleanly.  Please boot your "
                                 "Linux installation, let the file systems be "
                                 "checked and shut down cleanly to rescue.\n"
                                 "%s") % "\n".join(dirtyDevs), type="custom",
                               customIcon="warning", customButtons=[_("Ok")])
            storage.devicetree.teardownAll()
            return False
        elif warnDirty and dirtyDevs:
            rc = intf.messageWindow(_("Dirty File Systems"),
                                    _("The following file systems for your Linux "
                                      "system were not unmounted cleanly.  Would "
                                      "you like to mount them anyway?\n"
                                      "%s") % "\n".join(dirtyDevs),
                                    type="yesno")
            if rc :
                return False

        storage.storageset.mountFilesystems(readOnly=readOnly, skipRoot=True)
        return True


class Storage(object):
    def __init__(self, ignoredDisks=[]):
        self._nextID = 0
        self.ignoredDisks = ignoredDisks
        self.exclusiveDisks = []
        self.doAutoPart = False
        self.clearPartType = None
        self.clearPartDisks = []
        self.clearPartChoice = None
        self.reinitializeDisks = False
        self.zeroMbr = None
        self.protectedDevSpecs = []
        self.autoPartitionRequests = []
        self.defaultFSType = get_default_filesystem_type()
        self.defaultBootFSType = get_default_filesystem_type(boot=True)
        self.eddDict = {}
        self.defaultFSType = get_default_filesystem_type()
        self.defaultBootFSType = get_default_filesystem_type(boot=True)
        self.devicetree = DeviceTree(ignored=self.ignoredDisks,
                                     exclusive=self.exclusiveDisks,
                                     type=self.clearPartType,
                                     clear=self.clearPartDisks,
                                     reinitializeDisks=self.reinitializeDisks,
                                     protected=self.protectedDevSpecs,
                                     zeroMbr=self.zeroMbr)
        self.storageset = StorageSet(self.devicetree, ctx.consts.target_dir)

    def compareDisks(self, first, second):
        if self.eddDict.has_key(first) and self.eddDict.has_key(second):
            one = self.eddDict[first]
            two = self.eddDict[second]
            if (one < two):
                return -1
            elif (one > two):
                return 1

        # if one is in the BIOS and the other not prefer the one in the BIOS
        if self.eddDict.has_key(first):
            return -1
        if self.eddDict.has_key(second):
            return 1

        if first.startswith("hd"):
            type1 = 0
        elif first.startswith("sd"):
            type1 = 1
        elif (first.startswith("vd") or first.startswith("xvd")):
            type1 = -1
        else:
            type1 = 2

        if second.startswith("hd"):
            type2 = 0
        elif second.startswith("sd"):
            type2 = 1
        elif (second.startswith("vd") or second.startswith("xvd")):
            type2 = -1
        else:
            type2 = 2

        if (type1 < type2):
            return -1
        elif (type1 > type2):
            return 1
        else:
            len1 = len(first)
            len2 = len(second)

            if (len1 < len2):
                return -1
            elif (len1 > len2):
                return 1
            else:
                if (first < second):
                    return -1
                elif (first > second):
                    return 1

        return 0

    def doIt(self):
        self.devicetree.processOperations()

        # now set the boot partition's flag
        try:
            boot = self.storageset.bootDevice
            bootDevs = [boot]
        except DeviceError:
            bootDevs = []
        else:
            for dev in bootDevs:
                if hasattr(dev, "bootable"):
                    skip = False
                    if dev.disk.format.partedDisk.type == "msdos":
                        for p in dev.disk.format.partedDisk.partitions:
                            if p.type == parted.PARTITION_NORMAL and \
                               p.getFlag(parted.PARTITION_BOOT):
                                skip = True
                                break
                    if skip:
                        ctx.logger.info("not setting boot flag on %s as there is"
                                        "another active partition" % dev.name)
                        continue
                    ctx.logger.info("setting boot flag on %s" % dev.name)
                    dev.bootable = True
                    dev.disk.setup()
                    dev.disk.format.commitToDisk()

    @property
    def nextID(self):
        id = self._nextID
        self._nextID += 1
        return id

    def shutdown(self):
        try:
            self.devicetree.teardownAll()
        except DeviceTreeError as msg:
            ctx.logger.error("failure tearing down device tree: %s" % msg)

    def reset(self):
        """ Reset storage configuration to reflect actual system state.

            This should rescan from scratch but not clobber user-obtained
            information like passphrases, iscsi config, &c

        """
        self.devicetree = DeviceTree(intf=ctx.interface,
                                     ignored=self.ignoredDisks,
                                     exclusive=self.exclusiveDisks,
                                     type=self.clearPartType,
                                     clear=self.clearPartDisks,
                                     reinitializeDisks=self.reinitializeDisks,
                                     protected=self.protectedDevSpecs,
                                     zeroMbr=self.zeroMbr)
        self.devicetree.populate()
        self.storageset = StorageSet(self.devicetree, ctx.consts.target_dir)
        self.eddDict = yali.util.get_edd_dict([disk.path for disk in self.partitioned])

    def deviceImmutable(self, device, ignoreProtected=False):
        """ Return any reason the device cannot be modified/removed.

            Return False if the device can be removed.

            Devices that cannot be removed include:

                - protected partitions
                - extended partition containing logical partitions that
                  meet any of the above criteria

        """
        if not isinstance(device, Device):
            raise ValueError("arg1 (%s) must be a Device instance" % device)

        if not ignoreProtected and device.protected:
            return _("This partition is holding the data for the hard "
                      "drive install.")
        elif isinstance(device, Partition) and device.isProtected:
            return _("You cannot delete a partition of a LDL formatted "
                     "DASD.")
        elif device.format.type == "mdmember":
            for array in self.raidArrays + self.raidContainers:
                if array.dependsOn(device):
                    if array.minor is not None:
                        return _("This device is part of the RAID "
                                 "device %s, you have to edit or "
                                 "remove the raid partition "
                                 "appropriately!") % (array.path,)
                    else:
                        return _("This device is part of a RAID device.")
        elif device.format.type == "lvmpv":
            for vg in self.vgs:
                if vg.dependsOn(device):
                    if vg.name is not None:
                        return _("This device is part of the LVM "
                                 "volume group '%s'.") % (vg.name,)
                    else:
                        return _("This device is part of a LVM volume "
                                 "group.")
        elif isinstance(device, Partition) and device.isExtended:
            reasons = {}
            for dep in self.deviceDeps(device):
                reason = self.deviceImmutable(dep)
                if reason:
                    reasons[dep.path] = reason
            if reasons:
                msg =  _("This device is an extended partition which "
                         "contains logical partitions that cannot be "
                         "deleted:\n\n")
                for dev in reasons:
                    msg += "%s: %s" % (dev, reasons[dev])
                return msg

        if device.immutable:
            return device.immutable

        return False

    @property
    def devices(self):
        """A list of all devices in the device tree."""
        devices =  self.devicetree.devices
        devices.sort(key=lambda d: d.name)
        return devices

    @property
    def drives(self):
        disks = self.disks
        partitioned = self.partitioned
        drives = [d.name for d in disks if d in partitioned]
        drives.sort(cmp=self.compareDisks)
        return drives

    @property
    def disks(self):
        """ A list of the disks in the device tree.

            Ignored disks are not included, as are disks with no media present.

            This is based on the current state of the device tree and
            does not necessarily reflect the actual on-disk state of the
            system's disks.
        """
        disks = []
        for device in self.devicetree.devices:
            if device.isDisk:
                if not device.mediaPresent:
                    ctx.logger.info("Skipping disk: %s: No media present" % device.name)
                    continue
                disks.append(device)
        disks.sort(key=lambda d: d.name, cmp=self.compareDisks)
        return disks

    def exceptionDisks(self):
        """ Return a list of removable devices to save exceptions to.

        """
        # When a usb is connected from before the start of the installation,
        # it is not correctly detected.
        udev_trigger(subsystem="block", action="change")
        self.reset()

        dests = []

        for disk in self.disks:
            if not disk.removable and \
                    disk.format is not None  and \
                    disk.format.mountable:
                dests.append([disk.path, disk.name])

        for part in self.partitions:
            if not part.disk.removable:
                continue

            elif part.partedPartition.active and \
                    not part.partedPartition.getFlag(parted.PARTITION_RAID) and \
                    not part.partedPartition.getFlag(parted.PARTITION_LVM) and \
                    part.format is not None and part.format.mountable:
                dests.append([part.path, part.name])

        return dests

    @property
    def partitions(self):
        """ A list of the partitions in the device tree.

            This is based on the current state of the device tree and
            does not necessarily reflect the actual on-disk state of the
            system's disks.
        """
        partitions = self.devicetree.getDevicesByInstance(Partition)
        partitions.sort(key=lambda d: d.name)
        return partitions

    @property
    def partitioned(self):
        """ A list of the partitioned devices in the device tree.

            Ignored devices are not included, nor disks with no media present.

            Devices of types for which partitioning is not supported are also
            not included.

            This is based on the current state of the device tree and
            does not necessarily reflect the actual on-disk state of the
            system's disks.
        """
        partitioned = []
        for device in self.devicetree.devices:
            if not device.partitioned:
                continue

            if not device.mediaPresent:
                ctx.logger.info("Skipping device: %s: No media present" % device.name)
                continue

            partitioned.append(device)

        partitioned.sort(key=lambda d: d.name)
        return partitioned

    @property
    def lvs(self):
        """ A list of the LVM Logical Volumes in the device tree.

            This is based on the current state of the device tree and
            does not necessarily reflect the actual on-disk state of the
            system's disks.
        """
        lvs = self.devicetree.getDevicesByType("lvmlv")
        lvs.sort(key=lambda d: d.name)
        return lvs

    @property
    def vgs(self):
        """ A list of the LVM Volume Groups in the device tree.

            This is based on the current state of the device tree and
            does not necessarily reflect the actual on-disk state of the
            system's disks.
        """
        vgs = self.devicetree.getDevicesByType("lvmvg")
        vgs.sort(key=lambda d: d.name)
        return vgs

    @property
    def pvs(self):
        """ A list of the LVM Physical Volumes in the device tree.

            This is based on the current state of the device tree and
            does not necessarily reflect the actual on-disk state of the
            system's disks.
        """
        devices = self.devicetree.devices
        pvs = [d for d in devices if d.format.type == "lvmpv"]
        pvs.sort(key=lambda d: d.name)
        return pvs

    @property
    def raidContainers(self):
        """ A list of the RAID containers in the device tree. """
        arrays = self.devicetree.getDevicesByType("mdcontainer")
        arrays.sort(key=lambda d: d.name)
        return arrays


    @property
    def raidArrays(self):
        """ A list of the MD arrays in the device tree.

            This is based on the current state of the device tree and
            does not necessarily reflect the actual on-disk state of the
            system's disks.
        """
        arrays = self.devicetree.getDevicesByType("mdarray")
        arrays.sort(key=lambda d: d.name)
        return arrays

    @property
    def raidMembers(self):
        """ A list of the MD member devices in the device tree.

            This is based on the current state of the device tree and
            does not necessarily reflect the actual on-disk state of the
            system's disks.
        """
        devices = self.devicetree.devices
        members = [d for d in devices if d.format.type == "mdmember"]
        members.sort(key=lambda d: d.name)
        return members

    def unusedPVS(self, vg=None):
        unused = []
        for pv in self.pvs:
            used = False
            for _vg in self.vgs:
                if _vg.dependsOn(pv) and _vg != vg:
                    used = True
                    break
                elif _vg == vg:
                    break
            if not used:
                unused.append(pv)
        return unused

    def unusedRaidMembers(self, array=None):
        unused = []
        for member in self.raidMembers:
            used = False
            for _array in self.raidArrays + self.raidContainers:
                if _array.dependsOn(member) and _array != array:
                    used = True
                    break
                elif _array == array:
                    break
            if not used:
                unused.append(member)
        return unused

    @property
    def unusedRaidMinors(self):
        """ Return a list of unused minors for use in RAID. """
        raidMinors = range(0, 32)
        for array in self.raidArrays + self.raidContainers:
            if array.minor is not None and array.minor in raidMinors:
                raidMinors.remove(array.minor)
        return raidMinors

    @property
    def rootDevice(self):
        return self.storageset.rootDevice

    @property
    def swaps(self):
        """ A list of the swap devices in the device tree.

            This is based on the current state of the device tree and
            does not necessarily reflect the actual on-disk state of the
            system's disks.
        """
        return self.storageset.swapDevices

    @property
    def mountpoints(self):
        return self.storageset.mountpoints

    def deviceDeps(self, device):
        return self.devicetree.getDependentDevices(device)

    @property
    def protectedDevices(self):
        devices = self.devicetree.devices
        protected = [d for d in devices if d.protected]
        protected.sort(key=lambda d: d.name)
        return protected

    def newPartition(self, *args, **kwargs):
        """ Return a new PartitionDevice instance for configuring. """
        if kwargs.has_key("fmt_type"):
            kwargs["format"] = getFormat(kwargs.pop("fmt_type"),
                                         mountpoint=kwargs.pop("mountpoint",None),
                                         **kwargs.pop("fmt_args", {}))

        if kwargs.has_key("disks"):
            parents = kwargs.pop("disks")
            if isinstance(parents, Device):
                kwargs["parents"] = [parents]
            else:
                kwargs["parents"] = parents

        if kwargs.has_key("name"):
            name = kwargs.pop("name")
        else:
            name = "req%d" % self.nextID

        return Partition(name, *args, **kwargs)

    def newVolumeGroup(self, *args, **kwargs):
        """ Return a new VolumeGroup instance. """
        pvs = kwargs.pop("pvs", [])
        for pv in pvs:
            if pv not in self.devices:
                raise ValueError("pv is not in the device tree")

        if kwargs.has_key("name"):
            name = kwargs.pop("name")
        else:
            name = self.createSuggestedVolumeGroupName()

        if name in [d.name for d in self.devices]:
            raise ValueError("name already in use")

        return VolumeGroup(name, pvs, *args, **kwargs)

    def newLogicalVolume(self, *args, **kwargs):
        """ Return a new LogicalVolumeDevice instance. """
        if kwargs.has_key("vg"):
            vg = kwargs.pop("vg")

        mountpoint = kwargs.pop("mountpoint", None)
        if kwargs.has_key("fmt_type"):
            kwargs["format"] = getFormat(kwargs.pop("fmt_type"),
                                         mountpoint=mountpoint)

        if kwargs.has_key("name"):
            name = kwargs.pop("name")
        else:
            if kwargs.get("format") and kwargs["format"].type == "swap":
                swap = True
            else:
                swap = False
            name = self.createSuggestedLogicalVolumeName(vg,
                                                         swap=swap,
                                                         mountpoint=mountpoint)

        if name in [d.name for d in self.devices]:
            raise ValueError("name already in use")

        return LogicalVolume(name, vg, *args, **kwargs)

    def newRaidArray(self, *args, **kwargs):
        """ Return a new MDRaidArrayDevice instance for configuring. """
        if kwargs.has_key("fmt_type"):
            kwargs["format"] = getFormat(kwargs.pop("fmt_type"),
                                         mountpoint=kwargs.pop("mountpoint",None))

        if kwargs.has_key("minor"):
            kwargs["minor"] = int(kwargs["minor"])
        else:
            kwargs["minor"] = self.unusedRaidMinors[0]

        if kwargs.has_key("name"):
            name = kwargs.pop("name")
        else:
            name = "md%d" % kwargs["minor"]

        return RaidArray(name, *args, **kwargs)

    def createDevice(self, device):
        """ Schedule creation of a device.

            TODO: We could do some things here like assign the next
                  available raid minor if one isn't already set.
        """
        self.devicetree.addOperation(OperationCreateDevice(device))
        if device.format.type:
            self.devicetree.addOperation(OperationCreateFormat(device))

    def destroyDevice(self, device):
        """ Schedule destruction of a device. """
        if device.format.exists and device.format.type:
            # schedule destruction of any formatting while we're at it
            self.devicetree.addOperation(OperationDestroyFormat(device))

        operation = OperationDestroyDevice(device)
        self.devicetree.addOperation(operation)

    def formatDevice(self, device, format):
        """ Schedule formatting of a device. """
        self.devicetree.addOperation(OperationDestroyFormat(device))
        self.devicetree.addOperation(OperationCreateFormat(device, format))

    def formatByDefault(self, device):
        """Return whether the device should be reformatted by default."""
        formatlist = ['/boot', '/var', '/tmp', '/usr']
        exceptlist = ['/home', '/usr/local', '/opt', '/var/www']

        if not device.format.linuxNative:
            return False

        if device.format.mountable:
            if not device.format.mountpoint:
                return False

            if device.format.mountpoint == "/" or \
               device.format.mountpoint in formatlist:
                return True

            for p in formatlist:
                if device.format.mountpoint.startswith(p):
                    for q in exceptlist:
                        if device.format.mountpoint.startswith(q):
                            return False
                    return True
        elif device.format.type == "swap":
            return True

        # be safe for anything else and default to off
        return False

    def turnOnSwap(self):
        self.storageset.turnOnSwap()

    def mountFilesystems(self, readOnly=None, skipRoot=False):
        self.storageset.mountFilesystems(readOnly=readOnly, skipRoot=skipRoot)

    def umountFilesystems(self, swapoff=True):
        self.storageset.umountFilesystems(swapoff=swapoff)

    def createSwapFile(self, device, size):
        self.storageset.createSwapFile(device, size)

    def raidConf(self):
        raise NotImplementedError("raidConf method not implemented in Interface class.")

    @property
    def extendedPartitionsSupported(self):
        """ Return whether any disks support extended partitions."""
        for disk in self.partitioned:
            if disk.format.partedDisk.supportsFeature(parted.DISK_TYPE_EXTENDED):
                return True
        return False

    def createSuggestedVolumeGroupName(self):
        """ Return a reasonable, unused VG name. """
        # try to create a volume group name incorporating the hostname
        hostname = ctx.installData.hostName
        release = open("/etc/pardus-release").read().split()
        releaseHostName = "".join(release[:2]).lower()
        vgnames = [vg.name for vg in self.vgs]
        if hostname is not None and hostname != '':
            if hostname == releaseHostName:
                vgtemplate = "VolGroup"
            elif hostname.find('.') != -1:
                template = "vg_%s" % (hostname.split('.')[0].lower(),)
                vgtemplate = lvm.safeLvmName(template)
            else:
                template = "vg_%s" % (hostname.lower(),)
                vgtemplate = lvm.safeLvmName(template)
        else:
            vgtemplate = "VolGroup"

        if vgtemplate not in vgnames and \
                vgtemplate not in lvm.lvm_vg_blacklist:
            return vgtemplate
        else:
            i = 0
            while 1:
                tmpname = "%s%02d" % (vgtemplate, i,)
                if not tmpname in vgnames and \
                        tmpname not in lvm.lvm_vg_blacklist:
                    break

                i += 1
                if i > 99:
                    tmpname = ""

            return tmpname

    def createSuggestedLogicalVolumeName(self, vg, swap=None, mountpoint=None):
        """ Return a suitable, unused name for a new logical volume. """
        # FIXME: this is not at all guaranteed to work
        if mountpoint:
            # try to incorporate the mountpoint into the name
            if mountpoint == '/':
                lvtemplate = 'lv_root'
            else:
                if mountpoint.startswith("/"):
                    template = "lv_%s" % mountpoint[1:]
                else:
                    template = "lv_%s" % (mountpoint,)

                lvtemplate = lvm.safeLvmName(template)
        else:
            if swap:
                if len([s for s in self.swaps if s in vg.lvs]):
                    idx = len([s for s in self.swaps if s in vg.lvs])
                    while True:
                        lvtemplate = "lv_swap%02d" % idx
                        if lvtemplate in [lv.lvname for lv in vg.lvs]:
                            idx += 1
                        else:
                            break
                else:
                    lvtemplate = "lv_swap"
            else:
                idx = len(vg.lvs)
                while True:
                    lvtemplate = "LogVol%02d" % idx
                    if lvtemplate in [l.lvname for l in vg.lvs]:
                        idx += 1
                    else:
                        break

        return lvtemplate

    def sanityCheck(self):
        """ Run a series of tests to verify the storage configuration.

            This function is called at the end of partitioning so that
            we can make sure you don't have anything silly (like no /,
            a really small /, etc).  Returns (errors, warnings) where
            each is a list of strings.
        """
        checkSizes = [('/usr', 250), ('/tmp', 50), ('/var', 384),
                      ('/home', 100), ('/boot', 75)]
        warnings = []
        errors = []

        mustbeonlinuxfs = ['/', '/var', '/tmp', '/usr', '/home', '/usr/share', '/usr/lib']
        mustbeonroot = ['/bin', '/dev', '/sbin', '/etc', '/lib', '/root', '/mnt', 'lost+found', '/proc']

        filesystems = self.mountpoints
        root = self.storageset.rootDevice
        swaps = self.storageset.swapDevices

        try:
            boot = self.storageset.bootDevice
        except StorageError:
            boot = None

        if not root:
            errors.append(_("You have not defined a root partition (/),which is required for installation "
                            "of %s to continue.") % yali.util.product_name())

        if (root and
            root.size < ctx.consts.min_root_size):
            errors.append(_("Your / partition is less than %(min)s MB which is lower than "
                            "recommended for a normal %(productName)s install.")
                            % {'min': ctx.consts.min_root_size, 'productName': yali.util.product_name()})

        for (mount, size) in checkSizes:
            if mount in filesystems and filesystems[mount].size < size:
                warnings.append(_("Your %(mount)s partition is less than %(size)s megabytes which is "
                                  "lower than recommended for a normal %(productName)s install.")
                                % {'mount': mount, 'size': size, 'productName': yali.util.product_name()})


        errors.extend(self.storageset.checkBootRequest(boot))

        if not swaps:
            if yali.util.memInstalled() < yali.util.EARLY_SWAP_RAM:
                errors.append(_("You have not specified a swap partition. Due to the amount of memory "
                                "present, a swap partition is required to complete installation."))
            else:
                warnings.append(_("You have not specified a swap partition. Although not strictly "
                                  "required in all cases, it will significantly improve performance"
                                  "for most installations."))

        for (mountpoint, dev) in filesystems.items():
            if mountpoint in mustbeonroot:
                errors.append(_("This mount point is invalid. The %s directory must be on the / file system.") % mountpoint)

            if mountpoint in mustbeonlinuxfs and (not dev.format.mountable or not dev.format.linuxNative):
                errors.append(_("The mount point %s must be on a linux file system.") % mountpoint)

        return (errors, warnings)

    def isProtected(self, device):
        """ Return True is the device is protected. """
        return device.protected

    def checkDisks(self, intf):
        """Check that there are valid disk devices.
            Args:
                intf -- Interface instance to show messages

            Returns:
                True -- If there is any disk
                False -- If there is no disk
                None -- If user accept reboot option from interface

        """
        if not self.disks:
            rc = intf.messageWindow(_("No Drives Found"),
                               _("An error has occurred - no valid devices were "
                                 "found on\nwhich to create new file systems. "
                                 "Please check your\nhardware for the cause "
                                 "of this problem."), type="custom",
                               customButtons=[_("Reboot"), _("Cancel")], customIcon="error")
            if not rc:
                return None
            else:
                return False

        return True
