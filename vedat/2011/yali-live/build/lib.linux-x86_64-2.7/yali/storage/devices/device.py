#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import _ped
import parted
import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import yali.baseudev
import yali.context as ctx
import yali.util
from yali.storage.udev import *
from yali.storage.devices import AbstractDevice, AbstractDeviceError
from yali.storage.formats import getFormat

class DeviceError(AbstractDeviceError):
    pass

class DeviceNotFoundError(AbstractDeviceError):
    pass

def devicePathToName(devicePath):
    if devicePath.startswith("/dev/"):
        name = devicePath[5:]
    else:
        name = devicePath

    if name.startswith("mapper/"):
        name = name[7:]

    return name

def deviceNameToDiskByPath(deviceName=None):
    if not deviceName:
        return ""

    ret = None
    for dev in udev_get_block_devices():
        if udev_device_get_name(dev) == deviceName:
            ret = udev_device_get_by_path(dev)
            break

    if ret:
        return ret
    raise DeviceNotFoundError(deviceName)

class Device(AbstractDevice):
    _type = "device"
    _devDir = "/dev"
    _resizable = False
    _partitionable = False
    _isDisk = False
    sysfsBlockDir = "class/block"

    def __init__(self, device, parents=None, format=None,
                 exists=False, size=None, major=None, minor=None,
                 serial=None, model="", vendor="", bus="", sysfsPath = ''):
        """ Create a Device instance.

            Arguments:

                device  -- the device (generally device node base name)

            Keyword Arguments:


                size -- the device's size (units/format TBD)
                major -- the device major
                minor -- the device minor
                serial -- the ID_SERIAL_SHORT for this device
                vendor -- the manufacturer of this Device
                model -- manufacturer's device model string
                bus -- the interconnect this device uses
                sysfsPath -- sysfs device path
                parents -- a list of required Device instances
                format  -- a Format instance
                exists  -- is existing?
        """
        if isinstance(parents, Device):
            parents = [parents]

        self.exists = exists
        AbstractDevice.__init__(self, device, parents=parents)

        self.uuid = None
        self._format = None
        self._size = yali.util.numeric_type(size)
        self.major = yali.util.numeric_type(major)
        self.minor = yali.util.numeric_type(minor)
        self._serial = serial
        self._vendor = vendor
        self._model = model
        self.sysfsPath = sysfsPath

        self.protected = False
        self.immutable = None

        self.format = format
        self.originalFormat = self.format
        self.fstabComment = ""
        self._targetSize = self._size

        self._partedDevice = None

    def __str__(self):
        s = AbstractDevice.__str__(self)
        s += ("  uuid = %(uuid)s  format = %(format)r  size = %(size)s\n"
              "  major = %(major)s  minor = %(minor)r  exists = %(exists)s\n"
              "  sysfs path = %(sysfs)s  partedDevice = %(partedDevice)r\n"
              "  target size = %(targetSize)s  path = %(path)s\n"
              "  format args = %(formatArgs)s  originalFormat = %(origFmt)s" %
              {"uuid": self.uuid, "format": self.format, "size": self.size,
               "major": self.major, "minor": self.minor, "exists": self.exists,
               "sysfs": self.sysfsPath, "partedDevice": self.partedDevice,
               "targetSize": self.targetSize, "path": self.path,
               "formatArgs": self.formatArgs, "origFmt": self.originalFormat})
        return s

    @property
    def partedDevice(self):
        if self.exists and self.status and not self._partedDevice:
            ctx.logger.debug("looking up parted Device: %s" % self.path)

            try:
                self._partedDevice = parted.Device(path=self.path)
            except (_ped.IOException, _ped.DeviceException):
                pass

        return self._partedDevice

    def _getTargetSize(self):
        return self._targetSize

    def _setTargetSize(self, newsize):
        self._targetSize = newsize

    targetSize = property(lambda s: s._getTargetSize(),
                          lambda s, v: s._setTargetSize(v),
                          doc="Target size of this device")

    @property
    def path(self):
        """ Device node representing this device. """
        return "%s/%s" % (self._devDir, self.name)

    def updateSysfsPath(self):
        """ Update this device's sysfs path. """
        sysfsName = self.name.replace("/", "!")
        path = os.path.join("/sys", self.sysfsBlockDir, sysfsName)
        self.sysfsPath = os.path.realpath(path)[4:]
        ctx.logger.debug("%s sysfsPath set to %s" % (self.name, self.sysfsPath))

    @property
    def formatArgs(self):
        """ Device-specific arguments to format creation program. """
        return []

    @property
    def resizable(self):
        """ Can this type of device be resized? """
        return self._resizable and self.exists and \
               ((self.format and self.format.resizable) or not self.format)

    def notifyKernel(self):
        """ Send a 'change' uevent to the kernel for this device. """
        if not self.exists:
            ctx.logger.debug("not sending change uevent for non-existent device")
            return

        if not self.status:
            ctx.logger.debug("not sending change uevent for inactive device")
            return

        path = os.path.normpath("/sys/%s" % self.sysfsPath)
        try:
            yali.util.notify_kernel(path, action="change")
        except Exception, e:
            ctx.logger.warning("failed to notify kernel of change: %s" % e)

    @property
    def fstabSpec(self):
        spec = self.path
        if self.format and self.format.uuid:
            spec = "UUID=%s" % self.format.uuid
        return spec

    def resize(self, intf=None):
        """ Resize the device.

            New size should already be set.
        """
        raise NotImplementedError("resize method not defined for Device")

    def setup(self, intf=None, orig=False):
        """ Open, or set up, a device. """
        if not self.exists:
            raise DeviceError("device has not been created", self.name)

        self.setupParents(orig=orig)
        for parent in self.parents:
            if orig:
                parent.originalFormat.setup()
            else:
                parent.format.setup()

    def teardown(self, recursive=None):
        """ Close, or tear down, a device. """
        if not self.exists and not recursive:
            raise DeviceError("device has not been created", self.name)

        if self.status:
            if self.originalFormat.exists:
                self.originalFormat.teardown()
            if self.format.exists:
                self.format.teardown()
            yali.baseudev.udev_settle()

        if recursive:
            self.teardownParents(recursive=recursive)

    def _getSize(self):
        """ Get the device's size in MB, accounting for pending changes. """
        if self.exists and not self.mediaPresent:
            return 0

        if self.exists and self.partedDevice:
            self._size = self.currentSize

        size = self._size
        if self.exists and self.resizable and self.targetSize != size:
            size = self.targetSize

        return size

    def _setSize(self, newsize):
        """ Set the device's size to a new value. """
        if newsize > self.maxSize:
            raise DeviceError("device cannot be larger than %s MB" %
                              (self.maxSize(),), self.name)
        self._size = newsize

    size = property(lambda x: x._getSize(),
                    lambda x, y: x._setSize(y),
                    doc="The device's size in MB, accounting for pending changes")

    @property
    def currentSize(self):
        """ The device's actual size. """
        size = 0
        if self.exists and self.partedDevice:
            size = self.partedDevice.getSize()
        elif self.exists:
            size = self._size
        return size

    @property
    def minSize(self):
        """ The minimum size this device can be. """
        if self.format.minSize:
            return self.format.minSize
        else:
            return self.size

    @property
    def maxSize(self):
        """ The maximum size this device can be. """
        if self.format.maxSize > self.currentSize:
            return self.currentSize
        else:
            return self.format.maxSize

    @property
    def status(self):
        """ This device's status.

            For now, this should return a boolean:
                True    the device is open and ready for use
                False   the device is not open
        """
        if not self.exists:
            return False
        return os.access(self.path, os.W_OK)

    def _setFormat(self, format):
        """ Set the Device's format. """
        if not format:
            format = getFormat(None, device=self.path, exists=self.exists)
            ctx.logger.debug("Setting abstract format to %s" % self.path)
        if self._format and self._format.status:
            raise DeviceError("cannot replace active format", self.name)

        self._format = format

    def _getFormat(self):
        return self._format

    format = property(lambda d: d._getFormat(),
                      lambda d,f: d._setFormat(f),
                      doc="The device's formatting.")

    def preCommitFixup(self, *args, **kwargs):
        """ Do any necessary pre-commit fixups."""
        pass

    def create(self, intf=None):
        """ Create the device. """
        if self.exists:
            raise DeviceError("device has already been created", self.name)

        self.createParents()
        self.setupParents()
        self.exists = True
        self.setup()

    def destroy(self):
        """ Destroy the device. """
        if not self.exists:
            raise DeviceError("device has not been created", self.name)

        if not self.isleaf:
            raise DeviceError("Cannot destroy non-leaf device", self.name)

        self.exists = False

    @property
    def removable(self):
        devpath = os.path.normpath("/sys/%s" % self.sysfsPath)
        remfile = os.path.normpath("%s/removable" % devpath)
        return (self.sysfsPath and os.path.exists(devpath) and
                os.access(remfile, os.R_OK) and
                open(remfile).readline().strip() == "1")

    @property
    def isDisk(self):
        return self._isDisk

    @property
    def partitionable(self):
        return self._partitionable

    @property
    def partitioned(self):
        return self.format.type == "disklabel" and self.partitionable

    @property
    def vendor(self):
        return self._vendor

    @property
    def serial(self):
        return self._serial

    @property
    def model(self):
        if not self._model:
            self._model = getattr(self.partedDevice, "model", "")
        return self._model
