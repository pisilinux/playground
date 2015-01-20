#!/usr/bin/python
# -*- coding: utf-8 -*-

from parted import partitionFlag, PARTITION_LBA
import yali.baseudev
from devices.device import Device
from devices.partition import Partition
from formats import getFormat
from udev import udev_get_block_device, udev_device_get_uuid

OPERATION_TYPE_NONE = 0
OPERATION_TYPE_DESTROY = 1000
OPERATION_TYPE_RESIZE = 500
OPERATION_TYPE_MIGRATE = 250
OPERATION_TYPE_CREATE = 100


operation_strings = {OPERATION_TYPE_NONE: "None",
                  OPERATION_TYPE_DESTROY: "Destroy",
                  OPERATION_TYPE_RESIZE: "Resize",
                  OPERATION_TYPE_MIGRATE: "Migrate",
                  OPERATION_TYPE_CREATE: "Create"}

OPERATION_OBJECT_NONE = 0
OPERATION_OBJECT_FORMAT = 1
OPERATION_OBJECT_DEVICE = 2

object_strings = {OPERATION_OBJECT_NONE: "None",
                  OPERATION_OBJECT_FORMAT: "Format",
                  OPERATION_OBJECT_DEVICE: "Device"}

RESIZE_SHRINK = 88
RESIZE_GROW = 89

resize_strings = {RESIZE_SHRINK: "Shrink",
                  RESIZE_GROW: "Grow"}

def operation_type_from_string(type_string):
    if type_string is None:
        return None

    for (k,v) in operation_strings.items():
        if v.lower() == type_string.lower():
            return k

    return resize_type_from_string(type_string)

def operation_object_from_string(type_string):
    if type_string is None:
        return None

    for (k,v) in object_strings.items():
        if v.lower() == type_string.lower():
            return k

def resize_type_from_string(type_string):
    if type_string is None:
        return None

    for (k,v) in resize_strings.items():
        if v.lower() == type_string.lower():
            return k

class DeviceOperation(object):
    """ An operation that will be carried out in the future on a Device.

        These classes represent operations to be performed on devices or
        filesystems.

        The operand Device instance will be modified according to the
        operation, but no changes will be made to the underlying device or
        filesystem until the DeviceOperation instance's execute method is
        called. The DeviceOperation instance's cancel method should reverse
        any modifications made to the Device instance's attributes.

        If the Device instance represents a pre-existing device, the
        constructor should call any methods or set any attributes that the
        operation will eventually change. Device/Format classes should verify
        that the requested modifications are reasonable and raise an
        exception if not.

        Only one operation of any given type/object pair can exist for any
        given device at any given time. This is enforced by the
        DeviceTree.

        Basic usage:

            a = DeviceOperation(dev)
            a.execute()

            OR

            a = DeviceOperation(dev)
            a.cancel()
"""
    type = OPERATION_TYPE_NONE
    obj = OPERATION_OBJECT_NONE

    def __init__(self, device):
        if not isinstance(device, Device):
            raise ValueError("arg 1 must be a Device instance")
        self.device = device


    def execute(self, intf=None):
        """ perform the operation """
        pass

    def cancel(self):
        """ cancel the operation """
        pass

    def isDestroy(self):
        return self.type == OPERATION_TYPE_DESTROY

    def isCreate(self):
        return self.type == OPERATION_TYPE_CREATE

    def isResize(self):
        return self.type == OPERATION_TYPE_RESIZE

    def isShrink(self):
        return (self.type == OPERATION_TYPE_RESIZE and self.dir == RESIZE_SHRINK)

    def isGrow(self):
        return (self.type == OPERATION_TYPE_RESIZE and self.dir == RESIZE_GROW)

    def isDevice(self):
        return self.obj == OPERATION_OBJECT_DEVICE

    def isFormat(self):
        return self.obj == OPERATION_OBJECT_FORMAT

    @property
    def format(self):
        return self.device.format

    def __str__(self):
        s = "%s %s" % (operation_strings[self.type], object_strings[self.obj])
        if self.isFormat():
            s += " %s on" % self.format.type
        s += " %s %s (id %d)" % (self.device.type, self.device.name,
                                 self.device.id)
        return s

class OperationCreateDevice(DeviceOperation):
    """ Operation representing the creation of a new device. """
    type = OPERATION_TYPE_CREATE
    obj = OPERATION_OBJECT_DEVICE

    def __init__(self, device):
        # FIXME: assert device.fs is None
        DeviceOperation.__init__(self, device)

    def execute(self, intf=None):
        self.device.create(intf=intf)

class OperationDestroyDevice(DeviceOperation):
    """ An operation representing the deletion of an existing device. """
    type = OPERATION_TYPE_DESTROY
    obj = OPERATION_OBJECT_DEVICE

    def __init__(self, device):
        DeviceOperation.__init__(self, device)
        if device.exists:
            device.teardown()

    def execute(self, intf=None):
        self.device.destroy()

        # Make sure libparted does not keep cached info for this device
        # and returns it when we create a new device with the same name
        if self.device.partedDevice:
            self.device.partedDevice.removeFromCache()


class OperationResizeDevice(DeviceOperation):
    """ An operation representing the resizing of an existing device. """
    type = OPERATION_TYPE_RESIZE
    obj = OPERATION_OBJECT_DEVICE

    def __init__(self, device, newsize):
        if device.currentSize == newsize:
            raise ValueError("new size same as old size")

        if not device.resizable:
            raise ValueError("device is not resizable")

        DeviceOperation.__init__(self, device)
        if newsize > device.currentSize:
            self.dir = RESIZE_GROW
        else:
            self.dir = RESIZE_SHRINK
        self.origsize = device.targetSize
        self.device.targetSize = newsize

    def execute(self, intf=None):
        self.device.resize(intf=intf)

    def cancel(self):
        self.device.targetSize = self.origsize


class OperationCreateFormat(DeviceOperation):
    """ An operation representing creation of a new filesystem. """
    type = OPERATION_TYPE_CREATE
    obj = OPERATION_OBJECT_FORMAT

    def __init__(self, device, format=None):
        DeviceOperation.__init__(self, device)
        if format:
            self.origFormat = device.format
            if self.device.format.exists:
                self.device.format.teardown()
            self.device.format = format
        else:
            self.origFormat = getFormat(None)

    def execute(self, intf=None):
        self.device.setup()

        if isinstance(self.device, Partition):
            for flag in partitionFlag.keys():
                # Keep the LBA flag on pre-existing partitions
                if flag in [ PARTITION_LBA, self.format.partedFlag ]:
                    continue
                self.device.unsetFlag(flag)

            if self.format.partedFlag is not None:
                self.device.setFlag(self.format.partedFlag)

            if self.format.partedSystem is not None:
                self.device.partedPartition.system = self.format.partedSystem

            self.device.disk.format.commitToDisk()

        self.device.format.create(intf=intf,
                                  device=self.device.path,
                                  options=self.device.formatArgs)

        # Get the UUID now that the format is created
        yali.baseudev.udev_settle()
        self.device.updateSysfsPath()
        info = udev_get_block_device(self.device.sysfsPath)
        self.device.format.uuid = udev_device_get_uuid(info)

    def cancel(self):
        self.device.format = self.origFormat


class OperationDestroyFormat(DeviceOperation):
    """ An operation representing the removal of an existing filesystem.

    """
    type = OPERATION_TYPE_DESTROY
    obj = OPERATION_OBJECT_FORMAT

    def __init__(self, device):
        DeviceOperation.__init__(self, device)
        self.origFormat = self.device.format
        if device.format.exists:
            device.format.teardown()
        self.device.format = None

    def execute(self, intf=None):
        """ wipe the filesystem signature from the device """
        if self.origFormat:
            self.device.setup(orig=True)
            self.origFormat.destroy()
            yali.baseudev.udev_settle()
            self.device.teardown()

    def cancel(self):
        self.device.format = self.origFormat

    @property
    def format(self):
        return self.origFormat


class OperationResizeFormat(DeviceOperation):
    """ An operation representing the resizing of an existing filesystem.

        XXX Do we even want to support resizing of a filesystem without
            also resizing the device it resides on?
    """
    type = OPERATION_TYPE_RESIZE
    obj = OPERATION_OBJECT_FORMAT

    def __init__(self, device, newsize):
        if device.format.targetSize == newsize:
            raise ValueError("new size same as old size")

        DeviceOperation.__init__(self, device)
        if newsize > device.format.currentSize:
            self.dir = RESIZE_GROW
        else:
            self.dir = RESIZE_SHRINK
        self.origSize = self.device.format.targetSize
        self.device.format.targetSize = newsize

    def execute(self, intf=None):
        self.device.setup(orig=True)
        self.device.format.doResize(intf=intf)

    def cancel(self):
        self.device.format.targetSize = self.origSize

class OperationMigrateFormat(DeviceOperation):
    """ An operation representing the migration of an existing filesystem. """
    type = OPERATION_TYPE_MIGRATE
    obj = OPERATION_OBJECT_FORMAT

    def __init__(self, device):
        if not device.format.migratable or not device.format.exists:
            raise ValueError("device format is not migratable")

        DeviceOperation.__init__(self, device)
        self.device.format.migrate = True

    def execute(self, intf=None):
        self.device.setup(orig=True)
        self.device.format.doMigrate(intf=intf)

    def cancel(self):
        self.device.format.migrate = False

