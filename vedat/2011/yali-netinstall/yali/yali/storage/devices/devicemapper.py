#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import block
import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

from device import Device, DeviceError
from yali.storage.library import devicemapper

class DeviceMapperError(DeviceError):
    pass

class DeviceMapper(Device):
    """ A device-mapper device """
    _type = "dm"
    _devDir = "/dev/mapper"

    def __init__(self, name, format=None, size=None, dmUuid=None,
                 target=None, exists=None, parents=None, sysfsPath=''):
        """ Create a DMDevice instance.

            Arguments:

                name -- the device name (generally a device node's basename)

            Keyword Arguments:

                target -- the device-mapper target type (string)
                size -- the device's size (units/format TBD)
                dmUuid -- the device's device-mapper UUID
                sysfsPath -- sysfs device path
                format -- a DeviceFormat instance
                parents -- a list of required Device instances
                exists -- indicates whether this is an existing device
        """
        Device.__init__(self, name, format=format, size=size,
                        exists=exists, parents=parents, sysfsPath=sysfsPath)
        self.target = target
        self.dmUuid = dmUuid

    def __str__(self):
        s = Device.__str__(self)
        s += ("  target = %(target)s  dmUuid = %(dmUuid)s" %
              {"target": self.target, "dmUuid": self.dmUuid})
        return s

    @property
    def dict(self):
        d = super(DeviceMapper, self).dict
        d.update({"target": self.target, "dmUuid": self.dmUuid})
        return d

    @property
    def fstabSpec(self):
        """ Return the device specifier for use in /etc/fstab. """
        return self.path

    @property
    def mapName(self):
        """ This device's device-mapper map name """
        return self.name

    @property
    def status(self):
        _status = False
        for map in block.dm.maps():
            if map.name == self.mapName:
                _status = map.live_table and not map.suspended
                break

        return _status

    def updateSysfsPath(self):
        """ Update this device's sysfs path. """
        if not self.exists:
            raise DeviceMapperError("device has not been created", self.name)

        if self.status:
            dm_node = self.getDMNode()
            path = os.path.join("/sys", self.sysfsBlockDir, dm_node)
            self.sysfsPath = os.path.realpath(path)[4:]
        else:
            self.sysfsPath = ''

    def getDMNode(self):
        """ Return the dm-X (eg: dm-0) device node for this device. """
        if not self.exists:
            raise DeviceMapperError("device has not been created", self.name)

        return devicemapper.dm_node_from_name(self.name)

    def _setName(self, name):
        """ Set the device's map name. """
        if self.status:
            raise DeviceMapperError("cannot rename active device", self.name)

        self._name = name

    name = property(lambda d: d._name,
                    lambda d,n: d._setName(n))
