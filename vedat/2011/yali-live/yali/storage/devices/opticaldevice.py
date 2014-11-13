#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import parted

import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import yali.context as ctx
import yali.util
from device import Device, DeviceError

class OpticalDeviceError(DeviceError):
    pass

class OpticalDevice(Device):
    """ An optical drive, eg: cdrom, dvd+r, &c.

    """
    _type = "cdrom"

    def __init__(self, name, major=None, minor=None, exists=None,
                 format=None, parents=None, sysfsPath='', vendor="",
                 model=""):
        Device.__init__(self, name, format=format,
                        major=major, minor=minor, exists=True,
                        parents=parents, sysfsPath=sysfsPath,
                        vendor=vendor, model=model)

    @property
    def mediaPresent(self):
        """ Return a boolean indicating whether or not the device contains
            media.
        """
        if not self.exists:
            raise OpticalDeviceError("device has not been created", self.name)

        try:
            fd = os.open(self.path, os.O_RDONLY)
        except OSError as e:
            # errno 123 = No medium found
            if e.errno == 123:
                return False
            else:
                return True
        else:
            os.close(fd)
            return True

    def eject(self):
        """ Eject the drawer. """

        if not self.exists:
            raise OpticalDeviceError("device has not been created", self.name)

        #try to umount and close device before ejecting
        self.teardown()

        # Make a best effort attempt to do the eject.  If it fails, it's not
        # critical.
        fd = os.open(self.path, os.O_RDONLY | os.O_NONBLOCK)

        try:
            yali.util.ejectcdrom(fd)
        except SystemError as e:
            ctx.logger.warning("error ejecting cdrom %s: %s" % (self.name, e))

        os.close(fd)
