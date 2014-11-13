#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import gettext

__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import yali.context as ctx
from yali.util import numeric_type
from yali.baseudev import udev_settle
from yali.storage.library import raid
from yali.storage.formats import get_device_format
from yali.storage.udev import udev_device_get_md_uuid, udev_get_block_device
from yali.storage.devices.device import Device, DeviceError

class RaidArrayError(DeviceError):
    pass

class RaidArray(Device):
    """ An raid (Linux RAID) device. """
    _type = "mdarray"
    _packages = ["mdadm"]

    def __init__(self, name, level=None, major=None, minor=None, size=None,
                 memberDevices=None, totalDevices=None,
                 uuid=None, format=None, exists=None,
                 parents=None, sysfsPath=''):
        """ Create a RaidArray instance.

            Arguments:

                name -- the device name (generally a device node's basename)

            Keyword Arguments:

                level -- the device's RAID level (a string, eg: '1' or 'raid1')
                parents -- list of member devices (Device instances)
                size -- the device's size (units/format TBD)
                uuid -- the device's UUID
                minor -- the device minor
                sysfsPath -- sysfs device path
                format -- a DeviceFormat instance
                exists -- indicates whether this is an existing device
        """
        Device.__init__(self, name, format=format, exists=exists,
                               major=major, minor=minor, size=size,
                               parents=parents, sysfsPath=sysfsPath)

        self.level = level
        if level == "container":
            self._type = "mdcontainer"
        elif level is not None:
            self.level = raid.raidLevel(level)

        # For new arrays check if we have enough members
        if (not exists and parents and
                len(parents) < raid.get_raid_min_members(self.level)):
            raise ValueError, _("A RAID%(level)d set requires at least %(min_member)d member") % \
                                {"level":self.level, "min_member":raid.get_raid_min_members(self.level)}

        self.uuid = uuid
        self._totalDevices = numeric_type(totalDevices)
        self._memberDevices = numeric_type(memberDevices)
        self.sysfsPath = "/devices/virtual/block/%s" % name
        self.chunkSize = 512.0 / 1024.0         # chunk size in MB
        self.superBlockSize = 2.0               # superblock size in MB

        self.createMetadataVer = "1.1"
        # bitmaps are not meaningful on raid0 according to mdadm-3.0.3
        self.createBitmap = self.level != 0

        # For container members probe size now, as we cannot determine it
        # when teared down.
        if self.parents and self.parents[0].type == "mdcontainer":
            self._size = self.currentSize
            self._type = "mdbiosraidarray"

        self.formatClass = get_device_format("mdmember")
        if not self.formatClass:
            raise RaidArrayError("cannot find class for 'mdmember'", self.name)

        if self.exists and self.uuid:
            # this is a hack to work around mdadm's insistence on giving
            # really high minors to arrays it has no config entry for
            open("/etc/mdadm.conf", "a").write("ARRAY %s UUID=%s\n"
                                                % (self.path, self.uuid))

    @property
    def smallestMember(self):
        try:
            smallest = sorted(self.devices, key=lambda d: d.size)[0]
        except IndexError:
            smallest = None
        return smallest

    @property
    def size(self):
        if not self.devices:
            return 0

        # For container members return probed size, as we cannot determine it
        # when teared down.
        if self.type == "mdbiosraidarray":
            return self._size

        size = 0
        smallestMemberSize = self.smallestMember.size - self.superBlockSize
        if not self.exists or not self.partedDevice:
            if self.level == raid.RAID0:
                size = self.memberDevices * smallestMemberSize
                size -= size % self.chunkSize
            elif self.level == raid.RAID1:
                size = smallestMemberSize
            elif self.level == raid.RAID4:
                size = (self.memberDevices - 1) * smallestMemberSize
                size -= size % self.chunkSize
            elif self.level == raid.RAID5:
                size = (self.memberDevices - 1) * smallestMemberSize
                size -= size % self.chunkSize
            elif self.level == raid.RAID6:
                size = (self.memberDevices - 2) * smallestMemberSize
                size -= size % self.chunkSize
            elif self.level == raid.RAID10:
                size = (self.memberDevices / 2.0) * smallestMemberSize
                size -= size % self.chunkSize
            ctx.logger.debug("non-existant RAID %s size == %s" % (self.level, size))
        else:
            size = self.partedDevice.getSize()
            ctx.logger.debug("existing RAID %s size == %s" % (self.level, size))

        return size

    @property
    def description(self):
        if self.level == raid.RAID0:
            levelstr = "stripe"
        elif self.level == raid.RAID1:
            levelstr = "mirror"
        else:
            levelstr = "raid%s" % self.level

        if self.type == "mdcontainer":
            return "BIOS RAID container"
        elif self.type == "mdbiosraidarray":
            return "BIOS RAID set (%s)" % levelstr
        else:
            return "MDRAID set (%s)" % levelstr

    def __str__(self):
        s = Device.__str__(self)
        s += ("  level = %(level)s  spares = %(spares)s\n"
              "  members = %(memberDevices)s\n"
              "  total devices = %(totalDevices)s" %
              {"level": self.level, "spares": self.spares,
               "memberDevices": self.memberDevices, "totalDevices": self.totalDevices})
        return s

    @property
    def dict(self):
        d = super(RaidArray, self).dict
        d.update({"level": self.level,
                  "spares": self.spares, "memberDevices": self.memberDevices,
                  "totalDevices": self.totalDevices})
        return d

    @property
    def mdadmConfEntry(self):
        """ This array's mdadm.conf entry. """
        if self.level is None or self.memberDevices is None or not self.uuid:
            raise RaidArrayError("array is not fully defined", self.name)

        # containers and the sets within must only have a UUID= parameter
        if self.type == "mdcontainer" or self.type == "mdbiosraidarray":
            fmt = "ARRAY %s UUID=%s\n"
            return fmt % (self.path, self.uuid)

        fmt = "ARRAY %s level=raid%d num-devices=%d UUID=%s\n"
        return fmt % (self.path, self.level, self.memberDevices, self.uuid)

    @property
    def totalDevices(self):
        """ Total number of devices in the array, including spares. """
        count = len(self.parents)
        if not self.exists:
            count = self._totalDevices
        return count

    def _getMemberDevices(self):
        return self._memberDevices

    def _setMemberDevices(self, number):
        if not isinstance(number, int):
            raise ValueError("memberDevices is an integer")

        if number > self.totalDevices:
            raise ValueError("memberDevices cannot be greater than totalDevices")
        self._memberDevices = number

    memberDevices = property(_getMemberDevices, _setMemberDevices,
                             doc="number of member devices")

    def _getSpares(self):
        spares = 0
        if self.memberDevices is not None:
            if self.totalDevices is not None:
                spares = self.totalDevices - self.memberDevices
            else:
                spares = self.memberDevices
                self._totalDevices = self.memberDevices
        return spares

    def _setSpares(self, spares):
        # FIXME: this is too simple to be right
        if self.totalDevices > spares:
            self.memberDevices = self.totalDevices - spares

    spares = property(_getSpares, _setSpares)

    def probe(self):
        """ Probe for any missing information about this device.

            I'd like to avoid paying any attention to "Preferred Minor"
            as it seems problematic.
        """
        if not self.exists:
            raise RaidArrayError("device has not been created", self.name)

        try:
            self.devices[0].setup()
        except Exception:
            return

        info = raid.mdexamine(self.devices[0].path)
        if self.level is None:
            self.level = raid.raidLevel(info['level'])

    def updateSysfsPath(self):
        """ Update this device's sysfs path. """
        if not self.exists:
            raise RaidArrayError("device has not been created", self.name)

        if self.status:
            self.sysfsPath = "/devices/virtual/block/%s" % self.name
        else:
            self.sysfsPath = ''

    def _addDevice(self, device):
        """ Add a new member device to the array.

            XXX This is for use when probing devices, not for modification
                of arrays.
        """
        if not self.exists:
            raise RaidArrayError("device has not been created", self.name)

        if not isinstance(device.format, self.formatClass):
            raise ValueError("invalid device format for raid member")

        if self.uuid and device.format.mdUuid != self.uuid:
            raise ValueError("cannot add member with non-matching UUID")

        if device in self.devices:
            raise ValueError("device is already a member of this array")

        # we added it, so now set up the relations
        self.devices.append(device)
        device.addChild()

        device.setup()
        udev_settle()
        try:
            raid.mdadd(device.path)
            # mdadd causes udev events
            udev_settle()
        except raid.RaidError as e:
            ctx.logger.warning("failed to add member %s to md array %s: %s"
                        % (device.path, self.path, e))

        if self.status:
            # we always probe since the device may not be set up when we want
            # information about it
            self._size = self.currentSize

    def _removeDevice(self, device):
        """ Remove a component device from the array.

            XXX This is for use by clearpart, not for reconfiguration.
        """
        if device not in self.devices:
            raise ValueError("cannot remove non-member device from array")

        self.devices.remove(device)
        device.removeChild()

    @property
    def status(self):
        """ This device's status.

            For now, this should return a boolean:
                True    the device is open and ready for use
                False   the device is not open
        """
        # check the status in sysfs
        status = False
        if not self.exists:
            return status

        state_file = "/sys/%s/md/array_state" % self.sysfsPath
        if os.access(state_file, os.R_OK):
            state = open(state_file).read().strip()
            ctx.logger.debug("%s state is %s" % (self.name, state))
            if state in ("clean", "active", "active-idle", "readonly", "read-auto"):
                status = True
            # mdcontainers have state inactive when started (clear if stopped)
            if self.type == "mdcontainer" and state == "inactive":
                status = True

        return status

    @property
    def degraded(self):
        """ Return True if the array is running in degraded mode. """
        rc = False
        degraded_file = "/sys/%s/md/degraded" % self.sysfsPath
        if os.access(degraded_file, os.R_OK):
            val = open(degraded_file).read().strip()
            ctx.logger.debug("%s degraded is %s" % (self.name, val))
            if val == "1":
                rc = True

        return rc

    @property
    def devices(self):
        """ Return a list of this array's member device instances. """
        return self.parents

    def setup(self, intf=None, orig=False):
        """ Open, or set up, a device. """
        if not self.exists:
            raise RaidArrayError("device has not been created", self.name)

        if self.status:
            return

        disks = []
        for member in self.devices:
            member.setup(orig=orig)
            disks.append(member.path)

        update_super_minor = True
        if self.type == "mdcontainer" or self.type == "mdbiosraidarray":
            update_super_minor = False

        raid.mdactivate(self.path,
                          members=disks,
                          super_minor=self.minor,
                          update_super_minor=update_super_minor,
                          uuid=self.uuid)

        udev_settle()

        # we always probe since the device may not be set up when we want
        # information about it
        self._size = self.currentSize

    def teardown(self, recursive=None):
        """ Close, or tear down, a device. """
        if not self.exists and not recursive:
            raise RaidArrayError("device has not been created", self.name)

        if self.status:
            if self.originalFormat.exists:
                self.originalFormat.teardown()
            if self.format.exists:
                self.format.teardown()
            udev_settle()

        # Since BIOS RAID sets (containers in raid terminology) never change
        # there is no need to stop them and later restart them. Not stopping
        # (and thus also not starting) them also works around bug 523334
        if self.type == "mdcontainer" or self.type == "mdbiosraidarray":
            return

        # We don't really care what the array's state is. If the device
        # file exists, we want to deactivate it. raid has too many
        # states.
        if self.exists and os.path.exists(self.path):
            raid.mddeactivate(self.path)

        if recursive:
            self.teardownParents(recursive=recursive)

    def preCommitFixup(self, *args, **kwargs):
        """ Determine create parameters for this set """
        mountpoints = kwargs.pop("mountpoints")

        if "/boot" in mountpoints:
            bootmountpoint = "/boot"
        else:
            bootmountpoint = "/"

        # If we are used to boot from we cannot use 1.1 metadata
        if getattr(self.format, "mountpoint", None) == bootmountpoint or \
           getattr(self.format, "mountpoint", None) == "/boot/efi" or \
           self.format.type == "prepboot":
            self.createMetadataVer = "1.0"

        # Bitmaps are not useful for swap and small partitions
        if self.size < 1000 or self.format.type == "swap":
            self.createBitmap = False

    def create(self, intf=None):
        """ Create the device. """
        if self.exists:
            raise RaidArrayError("device already exists", self.name)

        w = None
        if intf:
            w = intf.progressWindow(_("Creating device %s") % (self.path,))

        try:
            self.createParents()
            self.setupParents()

            disks = [disk.path for disk in self.devices]
            spares = len(self.devices) - self.memberDevices
            raid.mdcreate(self.path,
                            self.level,
                            disks,
                            spares,
                            metadataVer=self.createMetadataVer,
                            bitmap=self.createBitmap)
        except Exception, msg:
            raise RaidArrayError, msg
        else:
            self.exists = True
            # the array is automatically activated upon creation, but...
            self.setup()
            udev_settle()
            self.updateSysfsPath()
            info = udev_get_block_device(self.sysfsPath)
            self.uuid = udev_device_get_md_uuid(info)
            for member in self.devices:
                member.mdUuid = self.uuid
        finally:
            if w:
                w.pop()

    @property
    def formatArgs(self):
        formatArgs = []
        if self.format.type == "ext2":
            if self.level == raid.RAID5:
                formatArgs = ['-R',
                              'stride=%d' % ((self.memberDevices - 1) * 16)]
            if self.level == raid.RAID4:
                formatArgs = ['-R',
                              'stride=%d' % ((self.memberDevices - 1) * 16)]
            elif self.level == raid.RAID0:
                formatArgs = ['-R',
                              'stride=%d' % (self.memberDevices * 16)]

    def destroy(self):
        """ Destroy the device. """
        if not self.exists:
            raise RaidArrayError("device has not been created", self.name)

        self.teardown()

        # The destruction of the formatting on the member devices does the
        # real work, but it isn't our place to do it from here.
        self.exists = False

    @property
    def mediaPresent(self):
        # Containers should not get any format handling done
        # (the device node does not allow read / write calls)
        if self.type == "mdcontainer":
            return False
        # BIOS RAID sets should show as present even when teared down
        elif self.type == "mdbiosraidarray":
            return True
        else:
            return self.partedDevice is not None

    @property
    def model(self):
        return self.description

    @property
    def partitionable(self):
        return self.type == "mdbiosraidarray"

    @property
    def isDisk(self):
        return self.type == "mdbiosraidarray"
