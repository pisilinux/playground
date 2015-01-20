#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import yali.context as ctx
from device import Device, DeviceError

class FileDeviceError(DeviceError):
    pass

class FileDevice(Device):
    """ A file on a filesystem.

        This exists because of swap files.
    """
    _type = "file"
    _devDir = ""

    def __init__(self, path, format=None, size=None,
                 exists=None, parents=None):
        """ Create a FileDevice instance.

            Arguments:

                path -- full path to the file

            Keyword Arguments:

                format -- a DeviceFormat instance
                size -- the file size (units TBD)
                parents -- a list of required devices (Device instances)
                exists -- indicates whether this is an existing device
        """
        Device.__init__(self, path, format=format, size=size,
                        exists=exists, parents=parents)

    def probe(self):
        """ Probe for any missing information about this device. """
        pass

    @property
    def fstabSpec(self):
        return self.name

    @property
    def path(self):
        path = self.name
        root = ""
        try:
            status = self.parents[0].format.status
        except (AttributeError, IndexError):
            status = False

        if status: 
            # this is the actual active mountpoint
            root = self.parents[0].format._mountpoint
            # trim the mountpoint down to the chroot since we already have
            # the otherwise fully-qualified path
            mountpoint = self.parents[0].format.mountpoint
            if mountpoint.endswith("/"):
                mountpoint = mountpoint[:-1]
            if mountpoint:
                root = root[:-len(mountpoint)]

        return os.path.normpath("%s/%s" % (root, path))

    def setup(self, intf=None, orig=False):
        Device.setup(self, orig=orig)
        if self.format and self.format.exists and not self.format.status:
            self.format.device = self.path

        for parent in self.parents:
            if orig:
                parent.originalFormat.setup()
            else:
                parent.format.setup()

    def teardown(self, recursive=None):
        Device.teardown(self)
        if self.format and self.format.exists and not self.format.status:
            self.format.device = self.path

    def create(self, intf=None):
        """ Create the device. """
        if self.exists:
            raise FileDeviceError("device already exists", self.name)

        w = None
        if intf:
            w = intf.progressWindow(_("Creating file %s") % (self.path,))

        try:
            # this only checks that parents exist
            self.createParents()
            self.setupParents()

            fd = os.open(self.path, os.O_RDWR)
            buf = '\0' * 1024 * 1024 * self.size
            os.write(fd, buf)
        except (OSError, TypeError) as e:
            ctx.logger.error("error writing out %s: %s" % (self.path, e))
            raise FileDeviceError(e, self.name)
        else:
            self.exists = True
        finally:
            os.close(fd)
            if w:
                w.pop()

    def destroy(self):
        """ Destroy the device. """
        if not self.exists:
            raise FileDeviceError("device has not been created", self.name)

        os.unlink(self.path)
        self.exists = False
