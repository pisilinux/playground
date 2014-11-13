#!/usr/bin/python
# -*- coding: utf-8 -*-
import gettext

__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import yali.context as ctx

from yali.baseudev import udev_settle
from yali.storage.devices.device import Device, DeviceError
from yali.storage.devices.devicemapper import DeviceMapper
from yali.storage.formats import get_device_format

class DMRaidArrayError(DeviceError):
    pass

class DMRaidArray(DeviceMapper):
    """ A dmraid (device-mapper RAID) device """
    _type = "dm-raid array"
    _packages = ["dmraid"]
    _partitionable = True
    _isDisk = True

    def __init__(self, name, raidSet=None, format=None,
                 size=None, parents=None, sysfsPath=''):
        """ Create a DMRaidArray instance.

            Arguments:

                name -- the dmraid name also the device node's basename

            Keyword Arguments:

                raidSet -- the RaidSet object from block
                parents -- a list of the member devices
                sysfsPath -- sysfs device path
                size -- the device's size
                format -- a DeviceFormat instance
        """
        if isinstance(parents, list):
            for parent in parents:
                if not parent.format or parent.format.type != "dmraidmember":
                    raise ValueError("parent devices must contain dmraidmember format")
        DeviceMapper.__init__(self, name, format=format, size=size,
                          parents=parents, sysfsPath=sysfsPath, exists=True)

        self.formatClass = get_device_format("dmraidmember")
        if not self.formatClass:
            raise DMRaidArrayError("cannot find class for 'dmraidmember'")

        self._raidSet = raidSet

    @property
    def raidSet(self):
        return self._raidSet

    def _addDevice(self, device):
        """ Add a new member device to the array.

            XXX This is for use when probing devices, not for modification
                of arrays.
        """
        if not self.exists:
            raise DMRaidArrayError("device has not been created", self.name)

        if not isinstance(device.format, self.formatClass):
            raise ValueError("invalid device format for dmraid member")

        if device in self.members:
            raise ValueError("device is already a member of this array")

        # we added it, so now set up the relations
        self.devices.append(device)
        device.addChild()

    @property
    def members(self):
        return self.parents

    @property
    def devices(self):
        """ Return a list of this array's member device instances. """
        return self.parents

    def deactivate(self):
        """ Deactivate the raid set. """
        # This call already checks if the set is not active.
        self._raidSet.deactivate()

    def activate(self):
        """ Activate the raid set. """
        # This call already checks if the set is active.
        self._raidSet.activate(mknod=True)
        udev_settle()

    def setup(self, intf=None, orig=False):
        """ Open, or set up, a device. """
        Device.setup(self, intf=None, orig=orig)
        self.activate()

    def teardown(self, recursive=None):
        """ Close, or tear down, a device. """
        if not self.exists and not recursive:
            raise DMRaidArrayError("device has not been created", self.name)

        ctx.logger.debug("not tearing down dmraid device %s" % self.name)

    @property
    def description(self):
        return "BIOS RAID set (%s)" % self._raidSet.rs.set_type

    @property
    def model(self):
        return self.description
