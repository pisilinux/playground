#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import gettext
from parted import PARTITION_LVM

__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

from yali.storage.library import lvm
from yali.storage.formats import Format, FormatError, register_device_format

class PhysicalVolumeError(FormatError):
    pass

class PhysicalVolume(Format):
    """ An LVM physical volume. """
    _type = "lvmpv"
    _name = _("physical volume (LVM)")
    _udevTypes = ["LVM2_member"]
    partedFlag = PARTITION_LVM
    _formattable = True                 # can be formatted
    _supported = True                   # is supported
    _linuxNative = True                 # for clearpart

    def __init__(self, *args, **kwargs):
        """ Create an PhysicalVolume instance.

            Keyword Arguments:

                device -- path to the underlying device
                uuid -- this PV's uuid (not the VG uuid)
                vgName -- the name of the VG this PV belongs to
                vgUuid -- the UUID of the VG this PV belongs to
                peStart -- offset of first physical extent
                exists -- indicates whether this is an existing format

        """
        Format.__init__(self, *args, **kwargs)
        self.vgName = kwargs.get("vgName")
        self.vgUuid = kwargs.get("vgUuid")
        self.peStart = kwargs.get("peStart", 0.1875)    # in MB

    def __str__(self):
        s = Format.__str__(self)
        s += ("  vgName = %(vgName)s  vgUUID = %(vgUUID)s"
              "  peStart = %(peStart)s" %
              {"vgName": self.vgName, "vgUUID": self.vgUuid,
               "peStart": self.peStart})
        return s

    @property
    def dict(self):
        d = super(PhysicalVolume, self).dict
        d.update({"vgName": self.vgName,
                  "vgUUID": self.vgUuid,
                  "peStart": self.peStart})
        return d

    def probe(self):
        """ Probe for any missing information about this device. """
        if not self.exists:
            raise PhysicalVolumeError("format has not been created", self.device)

    def create(self, *args, **kwargs):
        """ Create the format. """
        try:
            Format.create(self, *args, **kwargs)
            # Consider use of -Z|--zero
            # -f|--force or -y|--yes may be required

            # lvm has issues with persistence of metadata, so here comes the
            # hammer...
            Format.destroy(self, *args, **kwargs)

            lvm.pvcreate(self.device)
        except Exception, msg:
            raise PhysicalVolumeError("Create device failed!", self.device)
        else:
            self.exists = True
            self.notifyKernel()

    def destroy(self, *args, **kwargs):
        """ Destroy the format. """
        if not self.exists:
            raise PhysicalVolumeError("format has not been created", self.device)

        if self.status:
            raise PhysicalVolumeError("device is active", self.device)

        # FIXME: verify path exists?
        try:
            lvm.pvremove(self.device)
        except lvm.LVMError:
            Format.destroy(self, *args, **kwargs)

        self.exists = False
        self.notifyKernel()

    @property
    def status(self):
        # XXX hack
        return (self.exists and self.vgName and
                os.path.isdir("/dev/mapper/%s" % self.vgName))

register_device_format(PhysicalVolume)

