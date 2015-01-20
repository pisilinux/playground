#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import os
import sys
import math
from parted import fileSystemType
import pardus.sysutils
import gettext

__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import yali.util
import yali.sysutils
import yali.context as ctx
from yali.storage.formats import Format, FormatError, register_device_format

class FilesystemError(FormatError):
    pass

class FilesystemFormatError(FilesystemError):
    pass

class FilesystemResizeError(FilesystemError):
    pass

class FilesystemCheckError(FilesystemError):
    pass

class FilesystemMigrateError(FilesystemError):
    pass

global kernel_filesystems

def get_kernel_filesystems():
    fs_list = []
    for line in open("/proc/filesystems").readlines():
        fs_list.append(line.split()[-1])
    return fs_list

kernel_filesystems = get_kernel_filesystems()

class Filesystem(Format):
    _type = "filesystem"  # fs type name
    _modules = []                        # kernel modules required for support
    _mountType = None                    # like _type but for passing to mount
    _name = None
    _mkfs = ""                           # mkfs utility
    _resizefs = ""                       # resize utility
    _labelfs = ""                        # labeling utility
    _fsck = ""                           # fs check utility
    _fsckErrors = {}                     # fs check command error codes & msgs
    _migratefs = ""                      # fs migration utility
    _infofs = ""                         # fs info utility
    _formatOptions = []                  # default options passed to mkfs
    _mountOptions = ["defaults"]         # default options passed to mount
    _labelOptions = []
    _checkOptions = []
    _migrateOptions = []
    _infoOptions = []
    _migrationTarget = None
    _existingSizeFields = []
    _fsProfileSpecifier = None           # mkfs option specifying fsprofile

    def __init__(self, *args, **kwargs):
        """ Create a Filesystem instance.

            Keyword Args:

                device -- path to the device containing the filesystem
                mountpoint -- the filesystem's mountpoint
                label -- the filesystem label
                uuid -- the filesystem UUID
                mountopts -- mount options for the filesystem
                size -- the filesystem's size in MiB
                exists -- indicates whether this is an existing filesystem

        """
        if self.__class__ is Filesystem:
            raise TypeError("Filesystem is an abstract class.")

        Format.__init__(self, *args, **kwargs)
        self.mountpoint = kwargs.get("mountpoint")
        self.mountopts = kwargs.get("mountopts")
        self.label = kwargs.get("label")
        self.fsprofile = kwargs.get("fsprofile")

        # filesystem size does not necessarily equal device size
        self._size = kwargs.get("size", 0)
        self._minInstanceSize = None    # min size of this FS instance
        self._mountpoint = None     # the current mountpoint when mounted
        if self.exists and self.supported:
            self._size = self._getExistingSize()
            foo = self.minSize      # force calculation of minimum size

        self._targetSize = self._size

        if self.supported:
            self.loadModule()

    def __str__(self):
        s = Format.__str__(self)
        s += ("  mountpoint = %(mountpoint)s  mountopts = %(mountopts)s\n"
              "  label = %(label)s  size = %(size)s\n" %
              {"mountpoint": self.mountpoint, "mountopts": self.mountopts,
               "label": self.label, "size": self._size})
        return s

    def _setTargetSize(self, newsize):
        """ Set a target size for this filesystem. """
        if not self.exists:
            raise FilesystemError("filesystem has not been created")

        if newsize is None:
            # unset any outstanding resize request
            self._targetSize = self._size
            return

        if not self.minSize <= newsize < self.maxSize:
            raise ValueError("invalid target size request")

        self._targetSize = newsize

    def _getTargetSize(self):
        """ Get this filesystem's target size. """
        return self._targetSize

    targetSize = property(_getTargetSize, _setTargetSize,
                          doc="Target size for this filesystem")

    def _getSize(self):
        """ Get this filesystem's size. """
        size = self._size
        if self.resizable and self.targetSize != size:
            size = self.targetSize
        return size

    size = property(_getSize, doc="This filesystem's size, accounting "
                                  "for pending changes")

    def _getExistingSize(self):
        """ Determine the size of this filesystem.  Filesystem must
            exist.  Each filesystem varies, but the general procedure
            is to run the filesystem dump or info utility and read
            the block size and number of blocks for the filesystem
            and compute megabytes from that.
        """
        size = self._size

        if self.infofs and self.mountable and self.exists and not size:
            try:
                values = []
                argv = self._infoOptions + [ self.device ]

                buf = yali.util.run_batch(self.infofs, argv)[1]

                for line in buf.splitlines():
                    found = False

                    line = line.strip()
                    tmp = line.split(' ')
                    tmp.reverse()

                    for field in self._existingSizeFields:
                        if line.startswith(field):
                            for subfield in tmp:
                                try:
                                    values.append(long(subfield))
                                    found = True
                                    break
                                except ValueError:
                                    continue

                        if found:
                            break

                    if len(values) == len(self._existingSizeFields):
                        break

                if len(values) != len(self._existingSizeFields):
                    return 0

                size = 1
                for value in values:
                    size *= value

                # report current size as megabytes
                size = math.floor(size / 1024.0 / 1024.0)
            except Exception as e:
                ctx.logger.error("failed to obtain size of filesystem on %s: %s" % (self.device, e))

        return size

    @property
    def currentSize(self):
        """ The filesystem's current actual size. """
        size = 0
        if self.exists:
            size = self._size
        return float(size)

    def _getFormatOptions(self, options=None):
        argv = []
        if options and isinstance(options, list):
            argv.extend(options)
        argv.extend(self.formatOptions)
        if self._fsProfileSpecifier and self.fsprofile:
            argv.extend([self._fsProfileSpecifier, self.fsprofile])
        argv.append(self.device)
        return argv

    @property
    def resizeArgs(self):
        argv = [self.device, "%d" % (self.targetSize,)]
        return argv

    def _getCheckArgs(self):
        argv = []
        argv.extend(self.checkOptions)
        argv.append(self.device)
        return argv

    def _fsckFailed(self, rc):
        return False

    def _fsckErrorMessage(self, rc):
        return _("Unknown return code: %d.") % (rc,)

    def doMigrate(self, intf=None):
        if not self.exists:
            raise FilesystemMigrateError("filesystem has not been created", self.device)

        if not self.migratable or not self.migrate:
            return

        if not os.path.exists(self.device):
            raise FilesystemMigrateError("device does not exist", self.device)

        # if journal already exists skip
        if yali.sysutils.ext2HasJournal(self.device):
            ctx.logger.info("Skipping migration of %s, has a journal already." % self.device)
            return

        w = None
        if intf:
            w = intf.progressWindow(_("Migrating %s filesystem on %s") % (self.type, self.device))

        argv = self._migrateOptions[:]
        argv.append(self.device)
        try:
            rc = yali.util.run_batch(self.migratefs, argv)[0]
        except Exception as e:
            raise FilesystemMigrateError("filesystem migration failed: %s" % e, self.device)
        else:
            if rc:
                raise FilesystemMigrateError("filesystem migration failed: %s" % rc, self.device)

            # the other option is to actually replace this instance with an
            # instance of the new filesystem type.
            self._type = self.migrationTarget
        finally:
            if w:
                w.pop()

    def doFormat(self, *args, **kwargs):
        """ Create the filesystem.

            Arguments:

                None

            Keyword Arguments:

                options -- list of options to pass to mkfs

        """
        intf = kwargs.get("intf")
        options = kwargs.get("options")

        if self.exists:
            raise FilesystemFormatError("filesystem already exists", self.device)

        if not self.formattable:
            return

        if not self.mkfs:
            return

        if self.exists:
            return

        if not os.path.exists(self.device):
            raise FilesystemFormatError("device does not exist", self.device)

        argv = self._getFormatOptions(options=options)
        w = None
        if intf:
            w = intf.progressWindow(_("Creating %(type)s filesystem on %(device)s") % {"type":self.type, "device":self.device})

        try:
            rc = yali.util.run_batch(self.mkfs, argv)[0]
        except Exception as e:
            raise FilesystemFormatError(e, self.device)
        else:
            if rc:
                raise FilesystemFormatError("Create format failed: %s" % rc, self.device)
            else:
                self.exists = True
                self.notifyKernel()

                if self.label:
                    self.writeLabel(self.label)
        finally:
            if w:
                w.pop()

    def doResize(self, *args, **kwargs):
        """ Resize this filesystem to new size @newsize.

            Arguments:

        """
        intf = kwargs.get("intf")

        if not self.exists:
            raise FilesystemResizeError("filesystem does not exist", self.device)

        if not self.resizable:
            raise FilesystemResizeError("filesystem not resizable", self.device)

        if not self.resizefs:
            return

        if not os.path.exists(self.device):
            raise FilesystemResizeError("device does not exist", self.device)

        self.doCheck(intf=intf)

        self._minInstanceSize = None
        if self.targetSize < self.minSize:
            self.targetSize = self.minSize
            ctx.logger.info("Minimum size changed, setting targetSize on %s to %s" \
                     % (self.device, self.targetSize))
        w = None
        if intf:
            w = intf.progressWindow(_("Resizing filesystem on %s")
                                    % (self.device,))

        try:
            rc = yali.util.run_batch(self.resizefs, self.resizeArgs)[0]
        except Exception as e:
            raise FilesystemResizeError(e, self.device)
        else:
            if rc:
                raise FilesystemResizeError("resize failed: %s" % rc, self.device)

            self.doCheck(intf=intf)
            self.notifyKernel()
        finally:
            if w:
                w.pop()



    def doCheck(self, intf=None):
        if not self.exists:
            raise FilesystemError("filesystem has not been created", self.device)

        if not self.fsck:
            return

        if not os.path.exists(self.device):
            raise FilesystemError("device does not exist", self.device)

        w = None
        if intf:
            w = intf.progressWindow(_("Checking filesystem on %s")
                                    % (self.device))

        try:
            rc = yali.util.run_batch(self.fsck, self._getCheckArgs())[0]
        except Exception as e:
            raise FilesystemError("filesystem check failed: %s" % e, self.device)
        else:
            if self._fsckFailed(rc):
                hdr = _("%(type)s filesystem check failure on %(device)s: ") % \
                        {"type":self.type, "device":self.device}
                msg = self._fsckErrorMessage(rc)
                if intf:
                    help = _("Errors like this usually mean there is a problem "
                             "with the filesystem that will require user "
                             "interaction to repair. Restart installation "
                             "after you have corrected the problems on the "
                             "filesystem.")

                    intf.messageWindow(_("Unrecoverable Error"),
                                       hdr + "<br><br>" + msg + "<br><br>" + help,
                                       customIcon='error')
                else:
                    raise FilesystemError(hdr + msg)
        finally:
            if w:
                w.pop()


    def loadModule(self):
        """Load whatever kernel module is required to support this filesystem."""
        global kernel_filesystems

        if not self._modules or self.mountType in kernel_filesystems:
            return

        for module in self._modules:
            try:
                rc = yali.util.run_batch("modprobe", [module])
            except Exception as e:
                ctx.logger.error("Could not load kernel module %s: %s" % (module, e))
                self._supported = False
                return

            if rc:
                ctx.logger.error("Could not load kernel module %s" % module)
                self._supported = False
                return

        # If we successfully loaded a kernel module, for this filesystem, we
        # also need to update the list of supported filesystems.
        kernel_filesystems = get_kernel_filesystems()

    def mount(self, *args, **kwargs):
        """ Mount this filesystem.

            Arguments:

                None

            Keyword Arguments:

                options -- mount options (overrides all other option strings)
                chroot -- prefix to apply to mountpoint
                mountpoint -- mountpoint (overrides self.mountpoint)
        """
        options = kwargs.get("options", "")
        chroot = kwargs.get("chroot", "/")
        mountpoint = kwargs.get("mountpoint")

        if not self.exists:
            raise FilesystemError("filesystem has not been created")

        if not mountpoint:
            mountpoint = self.mountpoint

        if not mountpoint:
            raise FilesystemError("no mountpoint given")

        if self.status:
            return

        chrootedMountpoint = os.path.normpath("%s/%s" % (chroot, mountpoint))
        yali.util.mkdirChain(chrootedMountpoint)

        # passed in options override default options
        if not options or not isinstance(options, str):
            options = self.options

        bindMount = False
        if self.mountType == "bind":
            bindMount = True

        try:
            rc = yali.util.mount(self.device, chrootedMountpoint,
                                filesystem=self.mountType,
                                bindMount=bindMount,
                                options=options)
        except Exception as e:
            raise FilesystemError("mount failed: %s" % e)

        if rc:
            raise FilesystemError("mount failed: %s" % rc)

        self._mountpoint = chrootedMountpoint

    def unmount(self):
        """ Unmount this filesystem. """
        if not self.exists:
            raise FilesystemError("filesystem has not been created")

        if not self._mountpoint:
            # not mounted
            return

        if not os.path.exists(self._mountpoint):
            raise FilesystemError("mountpoint does not exist")

        rc = yali.util.umount(self._mountpoint, removeDir=False)
        if rc:
            raise FilesystemError("umount failed")

        self._mountpoint = None

    def _getLabelArgs(self, label):
        argv = []
        argv.extend(self.labelOptions)
        argv.extend([self.device, label])
        return argv 

    def writeLabel(self, label):
        """ Create a label for this filesystem. """
        if not self.exists:
            raise FilesystemError("filesystem has not been created")

        if not self.labelfs:
            return

        if not os.path.exists(self.device):
            raise FilesystemError("device does not exist")

        argv = self._getLabelArgs(label)
        rc = yali.util.run_batch(self.labelfs, argv)[0]

        if rc:
            raise FilesystemError("label failed")

        self.label = label
        self.notifyKernel()

    @property
    def isDirty(self):
        return False

    @property
    def mkfs(self):
        """ Program used to create filesystems of this type. """
        return self._mkfs

    @property
    def fsck(self):
        """ Program used to check filesystems of this type. """
        return self._fsck

    @property
    def resizefs(self):
        """ Program used to resize filesystems of this type. """
        return self._resizefs

    @property
    def labelfs(self):
        """ Program used to manage labels for this filesystem type. """
        return self._labelfs

    @property
    def migratefs(self):
        """ Program used to migrate filesystems of this type. """
        return self._migratefs

    @property
    def infofs(self):
        """ Program used to get information for this filesystem type. """
        return self._infofs

    @property
    def migrationTarget(self):
        return self._migrationTarget

    @property
    def utilsAvailable(self):
        for prog in [self.mkfs, self.resizefs, self.labelfs, self.infofs]:
            if not prog:
                continue

            if not filter(lambda d: os.access("%s/%s" % (d, prog), os.X_OK),
                          os.environ["PATH"].split(":")):
                ctx.logger.debug("%s program not available in % format type" % (prog, self.type))
                return False

        return True

    @property
    def supported(self):
        return self._supported and self.utilsAvailable

    @property
    def mountable(self):
        return (self.mountType in kernel_filesystems) or \
               (os.access("/sbin/mount.%s" % (self.mountType,), os.X_OK))

    @property
    def formatOptions(self):
        """ Default options passed to mkfs for this filesystem type. """
        # return a copy to prevent modification
        return self._formatOptions[:]

    @property
    def mountOptions(self):
        """ Default options passed to mount for this filesystem type. """
        # return a copy to prevent modification
        return self._mountOptions[:]

    @property
    def labelOptions(self):
        """ Default options passed to labeler for this filesystem type. """
        # return a copy to prevent modification
        return self._labelOptions[:]

    @property
    def checkOptions(self):
        """ Default options passed to checker for this filesystem type. """
        # return a copy to prevent modification
        return self._checkOptions[:]

    def _getOptions(self):
        options = ",".join(self.mountOptions)
        if self.mountopts:
            options = self.mountopts
        return options

    def _setOptions(self, options):
        self.mountopts = options

    options = property(_getOptions, _setOptions)

    def _isMigratable(self):
        """ Can filesystems of this type be migrated? """
        return bool(self._migratable and self.migratefs and
                    filter(lambda d: os.access("%s/%s"
                                               % (d, self.migratefs,),
                                               os.X_OK),
                           os.environ["PATH"].split(":")) and
                    self.migrationTarget)

    migratable = property(_isMigratable)

    def _setMigrate(self, migrate):
        if not migrate:
            self._migrate = migrate
            return

        if self.migratable and self.exists:
            self._migrate = migrate
        else:
            raise ValueError("cannot set migrate on non-migratable filesystem")

    migrate = property(lambda f: f._migrate, lambda f,m: f._setMigrate(m))

    @property
    def type(self):
        return self._type

    @property
    def mountType(self):
        if not self._mountType:
            self._mountType = self._type

        return self._mountType

    def create(self, *args, **kwargs):
        if self.exists:
            raise FilesystemError("filesystem already exists")

        Format.create(self, *args, **kwargs)

        return self.doFormat(*args, **kwargs)

    def setup(self, *args, **kwargs):
        """ Mount the filesystem.

            The filesystem will be mounted at the directory indicated by
            self.mountpoint.
        """
        return self.mount(**kwargs)

    def teardown(self, *args, **kwargs):
        return self.unmount(*args, **kwargs)

    @property
    def status(self):
        # FIXME check /proc/mounts or similar
        if not self.exists:
            return False
        return self._mountpoint is not None

class Ext2Filesystem(Filesystem):
    """ ext2 filesystem. """
    _type = "ext2"
    _modules = ["ext2"]
    _mkfs = "mke2fs"
    _resizefs = "resize2fs"
    _labelfs = "e2label"
    _fsck = "e2fsck"
    _fsckErrors = {4: _("File system errors left uncorrected."),
                   8: _("Operational error."),
                   16: _("Usage or syntax error."),
                   32: _("e2fsck cancelled by user request."),
                   128: _("Shared library error.")}
    _formattable = True
    _supported = True
    _resizable = True
    _bootable = True
    _linuxNative = True
    _formatOptions = []
    _mountOptions = ["defaults"]
    _checkOptions = ["-f", "-p", "-C", "0"]
    _dump = True
    _check = True
    _migratable = True
    _migrationTarget = "ext3"
    _migratefs = "tune2fs"
    _migrateOptions = ["-j"]
    _infofs = "dumpe2fs"
    _infoOptions = ["-h"]
    _existingSizeFields = ["Block count:", "Block size:"]
    _fsProfileSpecifier = "-T"
    _maxSize = 8 * 1024 * 1024
    _minSize = 0
    partedSystem = fileSystemType["ext2"]

    def _fsckFailed(self, rc):
        for errorCode in self._fsckErrors.keys():
            if rc & errorCode:
                return True
        return False

    def _fsckErrorMessage(self, rc):
        msg = ''

        for errorCode in self._fsckErrors.keys():
            if rc & errorCode:
                msg += "\n" + self._fsckErrors[errorCode]

        return msg.strip()

    def doMigrate(self, intf=None):
        Filesystem.doMigrate(self, intf=intf)
        self.tuneFilesystem()

    def _getFormatOptions(self, options=None):
        argv = []
        if options and isinstance(options, list):
            argv.extend(options)
        argv.extend(self.formatOptions)

        #5616: reserved-blocks-percentage
        device = ctx.storage.devicetree.getDeviceByPath(self.device)
        if device and device.size > 10240: #if bigger than 10 GB
            reserved_size = 500.0
            reserved_percentage = int(math.ceil(100.0 * reserved_size / device.size))
            argv.append("-m %d" % reserved_percentage)

        argv.append(self.device)
        return argv

    def doFormat(self, *args, **kwargs):
        Filesystem.doFormat(self, *args, **kwargs)
        self.tuneFilesystem()

    def tuneFilesystem(self):
        if not yali.sysutils.ext2HasJournal(self.device):
            # only do this if there's a journal
            return

        try:
            rc = yali.util.run_batch("tune2fs", ["-c0", "-i0","-ouser_xattr,acl", self.device])[0]
        except Exception as e:
            ctx.logger.error("failed to run tune2fs on %s: %s" % (self.device, e))
        else:
            return rc

    @property
    def minSize(self):
        """ Minimum size for this filesystem in MB. """
        if self._minInstanceSize is None:
            # try once in the beginning to get the minimum size for an
            # existing filesystem.
            size = self._minSize
            blockSize = None

            if self.exists and os.path.exists(self.device):
                # get block size
                rc, out, err = yali.util.run_batch(self.infofs, ["-h", self.device])
                for line in out.splitlines():
                    if line.startswith("Block size:"):
                        blockSize = int(line.split(" ")[-1])
                        break

                if blockSize is None:
                    raise FilesystemError("failed to get block size for %s filesystem on %s" %
                                         (self.mountType, self.device))

                # get minimum size according to resize2fs
                rc, out, err = yali.util.run_batch(self.resizefs, ["-Pf", self.device])
                #BUG:14255:resizefs needs file system check
                for line in out.splitlines():
                    if "minimum size of the filesystem:" not in line:
                        continue

                    # line will look like:
                    # Estimated minimum size of the filesystem: 1148649
                    #
                    # NOTE: The minimum size reported is in blocks.  Convert
                    # to bytes, then megabytes, and finally round up.
                    (text, sep, minSize) = line.partition(": ")
                    size = long(minSize) * blockSize
                    size = math.ceil(size / 1024.0 / 1024.0)
                    break

                if size is None:
                    ctx.logger.warning("failed to get minimum size for %s filesystem "
                                "on %s" % (self.mountType, self.device))

            self._minInstanceSize = size

        return self._minInstanceSize

    @property
    def isDirty(self):
        return yali.sysutils.ext2IsDirty(self.device)

    @property
    def resizeArgs(self):
        argv = ["-p", self.device, "%dM" % (self.targetSize,)]
        return argv

register_device_format(Ext2Filesystem)

class Ext3Filesystem(Ext2Filesystem):
    """ ext3 filesystem. """
    _type = "ext3"
    _modules = ["ext3"]
    _formatOptions = ["-t", "ext3"]
    _migrationTarget = "ext4"
    _modules = ["ext3"]
    _migrateOptions = ["-O", "extents"]
    partedSystem = fileSystemType["ext3"]

register_device_format(Ext3Filesystem)

class Ext4Filesystem(Ext3Filesystem):
    """ ext4 filesystem. """
    _type = "ext4"
    _modules = ["ext4"]
    _migratable = False
    _formatOptions = ["-t", "ext4"]
    partedSystem = fileSystemType["ext4"]

register_device_format(Ext4Filesystem)

class FATFilesystem(Filesystem):
    """ FAT filesystem. """
    _type = "vfat"
    _modules = ["vfat"]
    _mkfs = "mkdosfs"
    _labelfs = "dosfslabel"
    _fsck = "dosfsck"
    _fsckErrors = {1: _("Recoverable errors have been detected or dosfsck has "
                        "discovered an internal inconsistency."),
                   2: _("Usage error.")}
    _supported = True
    _formattable = True
    _mountOptions = ["umask=0077", "shortname=winnt"]
    # FIXME this should be fat32 in some cases
    _maxSize = 1024 * 1024
    partedSystem = fileSystemType["fat16"]

    def _fsckFailed(self, rc):
        if rc >= 1:
            return True
        return False

    def _fsckErrorMessage(self, rc):
        return self._fsckErrors[rc]

register_device_format(FATFilesystem)

class EFIFilesystem(FATFilesystem):
    _type = "efi"
    _modules = ["vfat"]
    _mountType = "vfat"
    _name = "EFI System Partition"
    _bootable = True
    _minSize = 50
    _maxSize = 256

    @property
    def supported(self):
        return yali.util.isEfi() and self.utilsAvailable

register_device_format(EFIFilesystem)

class BTRFilesystem(Filesystem):
    """ btrfs filesystem """
    _type = "btrfs"
    _modules = ["btrfs"]
    _mkfs = "mkfs.btrfs"
    _resizefs = "btrfsctl"
    _formattable = True
    _linuxNative = True
    _bootable = False
    _maxLabelChars = 256
    _supported = False
    _dump = True
    _check = True
    _maxSize = 16 * 1024 * 1024
    # FIXME parted needs to be thaught about btrfs so that we can set the
    # partition table type correctly for btrfs partitions
    # partedSystem = fileSystemType["btrfs"]

    def _getFormatOptions(self, options=None):
        argv = []
        if options and isinstance(options, list):
            argv.extend(options)
        argv.extend(self.formatOptions)
        if self.label:
            argv.extend(["-L", self.label])
        argv.append(self.device)
        return argv

    @property
    def resizeArgs(self):
        argv = ["-r", "%dm" % (self.targetSize,), self.device]
        return argv

    @property
    def supported(self):
        """ Is this filesystem a supported type? """
        supported = self._supported
        if "btrfs" in pardus.sysutils.get_kernel_option("yali"):
            supported = self.utilsAvailable

        return supported

register_device_format(BTRFilesystem)

class ReiserFilesystem(Filesystem):
    """ reiserfs filesystem """
    _type = "reiserfs"
    _mkfs = "mkreiserfs"
    _resizefs = "resize_reiserfs"
    _labelfs = "reiserfstune"
    _formatOptions = ["-f", "-f"]
    _labelOptions = ["-l"]
    _maxLabelChars = 16
    _formattable = True
    _linuxNative = True
    _supported = False
    _dump = True
    _check = True
    _infofs = "debugreiserfs"
    _infoOptions = []
    _existingSizeFields = ["Count of blocks on the device:", "Blocksize:"]
    partedSystem = fileSystemType["reiserfs"]
    _maxSize = 16 * 1024 * 1024

    @property
    def supported(self):
        """ Is this filesystem a supported type? """
        supported = self._supported
        if "reiserfs" in pardus.sysutils.get_kernel_option("yali"):
            supported = self.utilsAvailable

        return supported

    @property
    def resizeArgs(self):
        argv = ["-s", "%dM" % (self.targetSize,), self.device]
        return argv


register_device_format(ReiserFilesystem)

class XFilesystem(Filesystem):
    """ XFilesystem filesystem """
    _type = "xfs"
    _modules = ["xfs"]
    _mkfs = "mkfs.xfs"
    _labelfs = "xfs_admin"
    _formatOptions = ["-f"]
    _labelOptions = ["-L"]
    _maxLabelChars = 16
    _formattable = True
    _linuxNative = True
    _supported = True
    _dump = True
    _check = True
    _infofs = "xfs_db"
    _infoOptions = ["-c", "\"sb 0\"", "-c", "\"p dblocks\"",
                           "-c", "\"p blocksize\""]
    _existingSizeFields = ["dblocks =", "blocksize ="]
    partedSystem = fileSystemType["xfs"]
    _maxSize = 16 * 1024 * 1024

register_device_format(XFilesystem)

class NTFSFilesystem(Filesystem):
    """ ntfs filesystem. """
    _type = "ntfs-3g"
    _mkfs = "mkfs.ntfs"
    _resizefs = "ntfsresize"
    _fsck = "ntfsresize"
    _supported = True
    _resizable = True
    _formattable = True
    _formatOptions = ["-Q"]
    _mountOptions = ["defaults", "ro"]
    _checkOptions = ["-c"]
    _infofs = "ntfsinfo"
    _infoOptions = ["-m"]
    _existingSizeFields = ["Cluster Size:", "Volume Size in Clusters:"]
    partedSystem = fileSystemType["ntfs"]
    _minSize = 1
    _maxSize = 16 * 1024 * 1024

    def _fsckFailed(self, rc):
        if rc != 0:
            return True
        return False

    @property
    def minSize(self):
        """ The minimum filesystem size in megabytes. """
        if self._minInstanceSize is None:
            # we try one time to determine the minimum size.
            size = self._minSize
            if self.exists and os.path.exists(self.device):
                minSize = None
                buf = yali.util.run_batch(self.resizefs, ["-m", self.device])[1]
                for l in buf.split("\n"):
                    if not l.startswith("Minsize"):
                        continue
                    try:
                        min = l.split(":")[1].strip()
                        minSize = int(min) + 250
                    except Exception, e:
                        minSize = None
                        ctx.logger.warning("Unable to parse output for minimum size on %s: %s" %(self.device, e))

                if minSize is None:
                    ctx.logger.warning("Unable to discover minimum size of filesystem on %s" %(self.device,))
                else:
                    size = minSize

            self._minInstanceSize = size

        return self._minInstanceSize

    @property
    def resizeArgs(self):
        # You must supply at least two '-f' options to ntfsresize or
        # the proceed question will be presented to you.
        argv = ["-ff", "-s", "%dM" % (self.targetSize,), self.device]
        return argv

register_device_format(NTFSFilesystem)

class HFS(Filesystem):
    _type = "hfs"
    _modules = ["hfs"]
    _mkfs = "hformat"
    _formattable = True
    partedSystem = fileSystemType["hfs"]

register_device_format(HFS)

class HFSPlus(Filesystem):
    _type = "hfs+"
    _modules = ["hfsplus"]
    _udevTypes = ["hfsplus"]
    partedSystem = fileSystemType["hfs+"]

register_device_format(HFSPlus)

class AppleBootstrap(HFS):
    _type = "appleboot"
    _mountType = "hfs"
    _name = "Apple Bootstrap"
    _bootable = True
    _minSize = 800.00 / 1024.00
    _maxSize = 1

    @property
    def supported(self):
        supported = self._supported
        if "appleboot" in pardus.sysutils.get_kernel_option("yali"):
            supported = self.utilsAvailable

        return supported

register_device_format(AppleBootstrap)

class JFS(Filesystem):
    """ JFS filesystem """
    _type = "jfs"
    _modules = ["jfs"]
    _mkfs = "mkfs.jfs"
    _labelfs = "jfs_tune"
    _formatOptions = ["-q"]
    _labelOptions = ["-L"]
    _maxLabelChars = 16
    _maxSize = 8 * 1024 * 1024
    _formattable = True
    _linuxNative = True
    _supported = False
    _dump = True
    _check = True
    _infofs = "jfs_tune"
    _infoOptions = ["-l"]
    _existingSizeFields = ["Aggregate block size:", "Aggregate size:"]
    partedSystem = fileSystemType["jfs"]

    @property
    def supported(self):
        """ Is this filesystem a supported type? """
        supported = self._supported
        if "jfs" in pardus.sysutils.get_kernel_option("yali"):
            supported = self.utilsAvailable

        return supported

register_device_format(JFS)

class Iso9660Filesystem(Filesystem):
    """ ISO9660 filesystem. """
    _type = "iso9660"
    _formattable = False
    _supported = True
    _resizable = False
    _bootable = False
    _linuxNative = False
    _dump = False
    _check = False
    _migratable = False
    _defaultMountOptions = ["ro"]


register_device_format(Iso9660Filesystem)

class NoDevFilesystem(Filesystem):
    """ nodev filesystem base class """
    _type = "nodev"

    def __init__(self, *args, **kwargs):
        Filesystem.__init__(self, *args, **kwargs)
        self.exists = True
        self.device = self.type

    def _setDevice(self, devspec):
        self._device = devspec

    def _getExistingSize(self):
        pass

register_device_format(NoDevFilesystem)


class DebugFilesystem(NoDevFilesystem):
    """ devpts filesystem. """
    _type = "debugfs"
    _mountOptions = ["debugfs", "defaults"]

register_device_format(DebugFilesystem)

class ProcFilesystem(NoDevFilesystem):
    _type = "proc"
    _defaultMountOptions = ["nosuid", "noexec"]

register_device_format(ProcFilesystem)


class SysFilesystem(NoDevFilesystem):
    _type = "sysfs"

register_device_format(SysFilesystem)


class TmpFilesystem(NoDevFilesystem):
    _type = "tmpfs"
    _mountOptions = ["nodev", "nosuid", "noexec"]

register_device_format(TmpFilesystem)

class BindFilesystem(Filesystem):
    _type = "bind"

    @property
    def mountable(self):
        return True

    def _getExistingSize(self):
        pass

register_device_format(BindFilesystem)
