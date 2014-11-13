#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import gettext
from parted import PARTITION_RAID

__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

from yali.storage.library import raid
from yali.storage.formats import Format, FormatError, register_device_format

class DMRaidMemberError(FormatError):
    pass

class DMRaidMember(Format):
    """ A dmraid member disk. """
    _type = "dmraidmember"
    _name = _("dm-raid member device")
    # XXX This looks like trouble.
    #
    #     Maybe a better approach is a RaidMember format with subclass
    #     for RaidMember, letting all *_raid_member types fall through
    #     to the generic RaidMember format, which is basically read-only.
    #
    #     One problem that presents is the possibility of someone passing
    #     a dmraid member to the RaidArray constructor.
    _udevTypes = ["adaptec_raid_member", "ddf_raid_member",
                 "hpt37x_raid_member", "hpt45x_raid_member",
                 "isw_raid_member",
                 "jmicron_raid_member", "lsi_mega_raid_member",
                 "nvidia_raid_member", "promise_fasttrack_raid_member",
                 "silicon_medley_raid_member", "via_raid_member"]
    _formattable = False                # can be formatted
    _supported = True                   # is supported
    _linuxNative = False                # for clearpart
    _packages = ["dmraid"]              # required packages
    _resizable = False                  # can be resized
    _bootable = False                   # can be used as boot 
    _maxSize = 0                        # maximum size in MB
    _minSize = 0                        # minimum size in MB
    _hidden = True                      # hide devices with this formatting?

    def __init__(self, *args, **kwargs):
        """ Create a Format instance.

            Keyword Arguments:

                device -- path to the underlying device
                uuid -- this format's UUID
                exists -- indicates whether this is an existing format

            On initialization this format is like Format

        """
        Format.__init__(self, *args, **kwargs)

        # Initialize the attribute that will hold the block object.
        self._raidmem = None

    def __str__(self):
        s = Format.__str__(self)
        s += ("  raidmem = %(raidmem)r" % {"raidmem": self.raidmem})
        return s

    def _getRaidmem(self):
        return self._raidmem

    def _setRaidmem(self, raidmem):
        self._raidmem = raidmem

    raidmem = property(lambda d: d._getRaidmem(),
                       lambda d,r: d._setRaidmem(r))

    def create(self, *args, **kwargs):
        raise DMRaidMemberError("creation of dmraid members is non-sense")

    def destroy(self, *args, **kwargs):
        raise DMRaidMemberError("destruction of dmraid members is non-sense")

register_device_format(DMRaidMember)

