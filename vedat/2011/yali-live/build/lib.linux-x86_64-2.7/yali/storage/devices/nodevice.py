#!/usr/bin/python
# -*- coding: utf-8 -*-


import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

from yali.storage.devices.device  import Device

class NoDevice(Device):
    """ A nodev device for nodev filesystems like tmpfs. """
    _type = "nodev"

    def __init__(self, format=None):
        """ Create a NoDevice instance.

            Arguments:

            Keyword Arguments:

                format -- a DeviceFormat instance
        """
        if format:
            name = format.type
        else:
            name = "none"

        Device.__init__(self, name, format=format)

    @property
    def path(self):
        """ Device node representing this device. """
        return self.name

    def probe(self):
        """ Probe for any missing information about this device. """
        pass

    def setup(self, intf=None, orig=False):
        """ Open, or set up, a device. """
        pass

    def teardown(self, recursive=False):
        """ Close, or tear down, a device. """
        pass

    def create(self, intf=None):
        """ Create the device. """
        self.setupParents()

    def destroy(self):
        """ Destroy the device. """
        pass
