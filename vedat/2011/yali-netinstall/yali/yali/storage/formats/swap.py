#!/usr/bin/python
# -*- coding: utf-8 -*-
from parted import PARTITION_SWAP, fileSystemType
import gettext

__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

from yali.storage.library.swap import swapon, swap_off, swap_status, mkswap, SwapError
from yali.storage.formats import Format, FormatError, register_device_format

class SwapSpaceError(FormatError):
    pass

class SwapSpace(Format):
    """ Swap space """
    _type = "swap"
    _name = None
    _udevTypes = ["swap"]
    partedFlag = PARTITION_SWAP
    partedSystem = fileSystemType["linux-swap(v1)"]
    _formattable = True                # can be formatted
    _supported = True                  # is supported
    _linuxNative = True                # for clearpart

    def __init__(self, *args, **kwargs):
        """ Create a SwapSpace instance.

            Keyword Arguments:

                device -- path to the underlying device
                uuid -- this swap space's uuid
                label -- this swap space's label
                priority -- this swap space's priority
                exists -- indicates whether this is an existing format

        """
        Format.__init__(self, *args, **kwargs)

        self.priority = kwargs.get("priority")
        self.label = kwargs.get("label")

    def __str__(self):
        s = Format.__str__(self)
        s += ("  priority = %(priority)s  label = %(label)s" %
              {"priority": self.priority, "label": self.label})
        return s

    @property
    def dict(self):
        d = super(SwapSpace, self).dict
        d.update({"priority": self.priority, "label": self.label})
        return d

    def _setPriority(self, priority):
        if priority is None:
            self._priority = None
            return

        if not isinstance(priority, int) or not 0 <= priority <= 32767:
            raise ValueError("swap priority must be an integer between 0 and 32767")

        self._priority = priority

    def _getPriority(self):
        return self._priority

    priority = property(_getPriority, _setPriority,
                        doc="The priority of the swap device")

    def _getOptions(self):
        opts = ""
        if self.priority is not None:
            opts += "pri=%d" % self.priority

        return opts

    def _setOptions(self, opts):
        if not opts:
            self.priority = None
            return

        for option in opts.split(","):
            (opt, equals, arg) = option.partition("=")
            if equals and opt == "pri":
                try:
                    self.priority = int(arg)
                except ValueError:
                    ctx.logger.info("invalid value for swap priority: %s" % arg)

    options = property(_getOptions, _setOptions,
                       doc="The swap device's fstab options string")

    @property
    def status(self):
        """ Device status. """
        return self.exists and swap_status(self.device)

    def setup(self, *args, **kwargs):
        """ Open, or set up, a device. """
        if not self.exists:
            raise SwapSpaceError("format has not been created", self.device)

        if self.status:
            return

        Format.setup(self, *args, **kwargs)
        swapon(self.device, priority=self.priority)

    def teardown(self, *args, **kwargs):
        """ Close, or tear down, a device. """
        if not self.exists:
            raise SwapSpaceError("format has not been created", self.device)

        if self.status:
            try:
                swap_off(self.device)
            except SwapError, msg:
                raise SwapSpaceError, msg

    def create(self, *args, **kwargs):
        """ Create the device. """
        force = kwargs.get("force")
        if not force and self.exists:
            raise SwapSpaceError("format already exists", self.device)

        if force:
            self.teardown()
        elif self.status:
            raise SwapError("device exists and is active", self.device)

        try:
            Format.create(self, *args, **kwargs)
            mkswap(self.device, label=self.label)
        except Exception, msg:
            raise SwapSpaceError, msg
        else:
            self.exists = True

register_device_format(SwapSpace)
