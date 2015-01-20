#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import gettext
from parted import PARTITION_RAID

__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

from yali.storage.library import raid
from yali.storage.formats import Format, FormatError, register_device_format

class RaidMemberError(FormatError):
    pass

class RaidMember(Format):
    """ An raid member disk. """
    _type = "mdmember"
    _name = _("software RAID")
    _udevTypes = ["linux_raid_member"]
    partedFlag = PARTITION_RAID
    _formattable = True                 # can be formatted
    _supported = True                   # is supported
    _linuxNative = True                 # for clearpart
    _packages = ["mdadm"]               # required packages

    def __init__(self, *args, **kwargs):
        """ Create a RaidMember instance.

            Keyword Arguments:

                device -- path to underlying device
                uuid -- this member device's uuid
                mdUuid -- the uuid of the array this device belongs to
                exists -- indicates whether this is an existing format

        """
        Format.__init__(self, *args, **kwargs)
        self.mdUuid = kwargs.get("mdUuid")
        self.raidMinor = None

        self.biosraid = kwargs.get("biosraid")

    def __str__(self):
        s = Format.__str__(self)
        s += ("  mdUUID = %(mdUUID)s  biosraid = %(biosraid)s" %
              {"mdUUID": self.mdUuid, "biosraid": self.biosraid})
        return s

    @property
    def dict(self):
        d = super(RaidMember, self).dict
        d.update({"mdUUID": self.mdUuid, "biosraid": self.biosraid})
        return d

    def probe(self):
        """ Probe for any missing information about this format. """
        if not self.exists:
            raise RaidMemberError("format does not exist", self.device)

        info = raid.mdexamine(self.device)
        if self.uuid is None:
            self.uuid = info['uuid']
        if self.raidMinor is None:
            self.raidMinor = info['mdMinor']

    def destroy(self, *args, **kwargs):
        if not self.exists:
            raise RaidMemberError("format does not exist", self.device)

        if not os.access(self.device, os.W_OK):
            raise RaidMemberError("device path does not exist", self.device)

        raid.mddestroy(self.device)
        self.exists = False

    @property
    def status(self):
        # XXX hack -- we don't have a nice way to see if the array is active
        return False

    @property
    def hidden(self):
        return (self._hidden or self.biosraid)

register_device_format(RaidMember)
