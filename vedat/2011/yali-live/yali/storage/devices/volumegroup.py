#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import math
import gettext

__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import yali.context as ctx
from yali.util import numeric_type
from devicemapper import DeviceMapper
from device import DeviceError
from yali.storage.library import lvm
from yali.storage.formats import get_device_format

class VolumeGroupError(DeviceError):
    pass

class VolumeGroup(DeviceMapper):
    """ An LVM Volume Group

        XXX Maybe this should inherit from Device instead of
            DeviceMapper since there's no actual device.
    """
    _type = "lvmvg"

    def __init__(self, name, parents, size=None, free=None,
                 peSize=None, peCount=None, peFree=None, pvCount=None,
                 uuid=None, exists=None, sysfsPath=''):
        """ Create a VolumeGroup instance.

            Arguments:

                name -- the device name (generally a device node's basename)
                parents -- a list of physical volumes (Device)

            Keyword Arguments:

                peSize -- physical extent size (in MB)
                exists -- indicates whether this is an existing device
                sysfsPath -- sysfs device path

                For existing VG's only:

                    size -- the VG's size (in MB)
                    free -- amount of free space in the VG
                    peFree -- number of free extents
                    peCount -- total number of extents
                    pvCount -- number of PVs in this VG
                    uuid -- the VG's UUID

        """
        self.pvClass = get_device_format("lvmpv")
        if not self.pvClass:
            raise VolumeGroupError("cannot find 'lvmpv' class")

        if isinstance(parents, list):
            for dev in parents:
                if not isinstance(dev.format, self.pvClass):
                    raise ValueError("constructor requires a list of PVs")
        elif not isinstance(parents.format, self.pvClass):
            raise ValueError("constructor requires a list of PVs")

        DeviceMapper.__init__(self, name, parents=parents,
                              exists=exists, sysfsPath=sysfsPath)

        self.uuid = uuid
        self.free = numeric_type(free)
        self.peSize = numeric_type(peSize)
        self.peCount = numeric_type(peCount)
        self.peFree = numeric_type(peFree)
        self.pvCount = numeric_type(pvCount)
        self.lv_names = []
        self.lv_uuids = []
        self.lv_sizes = []
        self.lv_attr = []
        self.hasDuplicate = False

        # circular references, here I come
        self._lvs = []

        # TODO: validate peSize if given
        if not self.peSize:
            self.peSize = 32.0   # MB

        if not self.exists:
            self.pvCount = len(self.parents)

        #self.probe()

    def __str__(self):
        s = DeviceMapper.__str__(self)
        s += ("  free = %(free)s  PE Size = %(peSize)s  PE Count = %(peCount)s\n"
              "  PE Free = %(peFree)s  PV Count = %(pvCount)s\n"
              "  LV Names = %(lv_names)s  modified = %(modified)s\n"
              "  extents = %(extents)s  free space = %(freeSpace)s\n"
              "  free extents = %(freeExtents)s\n"
              "  PVs = %(pvs)s\n"
              "  LVs = %(lvs)s" %
              {"free": self.free, "peSize": self.peSize, "peCount": self.peCount,
               "peFree": self.peFree, "pvCount": self.pvCount,
               "lv_names": self.lv_names, "modified": self.isModified,
               "extents": self.extents, "freeSpace": self.freeSpace,
               "freeExtents": self.freeExtents, "pvs": self.pvs, "lvs": self.lvs})
        return s

    @property
    def dict(self):
        d = super(VolumeGroup, self).dict
        d.update({"free": self.free, "peSize": self.peSize,
                  "peCount": self.peCount, "peFree": self.peFree,
                  "pvCount": self.pvCount, "extents": self.extents,
                  "freeSpace": self.freeSpace,
                  "freeExtents": self.freeExtents,
                  "lv_names": self.lv_names,
                  "lv_uuids": self.lv_uuids,
                  "lv_sizes": self.lv_sizes,
                  "lv_attr": self.lv_attr,
                  "lvNames": [lv.name for lv in self.lvs]})
        return d

    def probe(self):
        """ Probe for any information about this device. """
        if not self.exists:
            raise VolumeGroupError("device has not been created", self.name)

    @property
    def mapName(self):
        """ This device's device-mapper map name """
        # Thank you lvm for this lovely hack.
        return self.name.replace("-","--")

    @property
    def path(self):
        """ Device node representing this device. """
        return "%s/%s" % (self._devDir, self.mapName)

    def updateSysfsPath(self):
        """ Update this device's sysfs path. """
        if not self.exists:
            raise VolumeGroupError("device has not been created", self.name)

        self.sysfsPath = ''

    @property
    def status(self):
        """ The device's status (True means active). """
        if not self.exists:
            return False

        # certainly if any of this VG's LVs are active then so are we
        for lv in self.lvs:
            if lv.status:
                return True

        # if any of our PVs are not active then we cannot be
        for pv in self.pvs:
            if not pv.status:
                return False

        # if we are missing some of our PVs we cannot be active
        if not self.complete:
            return False

        return True

    def _addDevice(self, device):
        """ Add a new physical volume device to the volume group.

            XXX This is for use by device probing routines and is not
                intended for modification of the VG.
        """
        if not self.exists:
            raise VolumeGroupError("device does not exist", self.name)

        if not isinstance(device.format, self.pvClass):
            raise ValueError("addDevice requires a PV arg")

        if self.uuid and device.format.vgUuid != self.uuid:
            # this means there is another vg with the same name on the system
            # set hasDuplicate which will make complete return False
            # and let devicetree._handleInconsistencies() further handle this.
            # Note we still add the device to our parents for use by
            # devicetree._handleInconsistencies()
            self.hasDuplicate = True

        if device in self.pvs:
            raise ValueError("device is already a member of this VG")

        self.parents.append(device)
        device.addChild()

        # now see if the VG can be activated
        if self.complete:
            self.setup()

    def _removeDevice(self, device):
        """ Remove a physical volume from the volume group.

            This is for cases like clearing of preexisting partitions.
        """
        try:
            self.parents.remove(device)
        except ValueError, e:
            raise ValueError("cannot remove non-member PV device from VG")

        device.removeChild()

    def setup(self, intf=None, orig=False):
        """ Open, or set up, a device.

            XXX we don't do anything like "vgchange -ay" because we don't
                want all of the LVs activated, just the VG itself.
        """
        if not self.exists:
            raise VolumeGroupError(_("device has not been created"), self.name)

        if self.status:
            return

        if not self.complete:
            raise VolumeGroupError(_("cannot activate VG with missing PV(s)"), self.name)

        self.setupParents(orig=orig)

    def teardown(self, recursive=None):
        """ Close, or tear down, a device. """
        if not self.exists and not recursive:
            raise VolumeGroupError("device has not been created", self.name)

        if self.status:
            lvm.vgdeactivate(self.name)

        if recursive:
            self.teardownParents(recursive=recursive)

    def create(self, intf=None):
        """ Create the device. """
        if self.exists:
            raise VolumeGroupError("device already exists", self.name)

        w = None
        if intf:
            w = intf.progressWindow(_("Creating device %s") % (self.path,))

        try:
            self.createParents()
            self.setupParents()

            pv_list = [pv.path for pv in self.parents]
            lvm.vgcreate(self.name, pv_list, self.peSize)
        except Exception, msg:
            raise VolumeGroupError, msg
        else:
            # FIXME set / update self.uuid here
            self.exists = True
            self.setup()
        finally:
            if w:
                w.pop()

    def destroy(self):
        """ Destroy the device. """
        if not self.exists:
            raise VolumeGroupError("device has not been created", self.name)

        # set up the pvs since lvm needs access to them to do the vgremove
        self.setupParents(orig=True)

        # this sometimes fails for some reason.
        try:
            lvm.vgreduce(self.name, [], rm=True)
            lvm.vgremove(self.name)
        except lvm.LVMError:
            raise VolumeGroupError("Could not completely remove VG", self.name)
        finally:
            self.exists = False

    def reduce(self, pv_list):
        """ Remove the listed PVs from the VG. """
        if not self.exists:
            raise VolumeGroupError("device has not been created", self.name)

        lvm.vgreduce(self.name, pv_list)
        # XXX do we need to notify the kernel?

    def _addLogicalVolume(self, lv):
        """ Add an LV to this VG. """
        if lv in self._lvs:
            raise ValueError("lv is already part of this vg")

        # verify we have the space, then add it
        # do not verify for growing vg (because of ks)
        if not lv.exists and \
           not [pv for pv in self.pvs if getattr(pv, "req_grow", None)] and \
           lv.size > self.freeSpace:
            raise VolumeGroupError("new lv is too large to fit in free space", self.name)

        ctx.logger.debug("Adding %s/%dMB to %s" % (lv.name, lv.size, self.name))
        self._lvs.append(lv)

    def _removeLogicalVolume(self, lv):
        """ Remove an LV from this VG. """
        if lv not in self.lvs:
            raise ValueError("specified lv is not part of this vg")

        self._lvs.remove(lv)

    def _addPhysicalVolume(self, pv):
        """ Add a PV to this VG. """
        if pv in self.pvs:
            raise ValueError("pv is already part of this vg")

        # for the time being we will not allow vgextend
        if self.exists:
            raise VolumeGroupError("cannot add pv to existing vg", self.name)

        self.parents.append(pv)
        pv.addChild()

        # and update our pv count
        self.pvCount = len(self.parents)

    def _removePhysicalVolume(self, pv):
        """ Remove an PV from this VG. """
        if not pv in self.pvs:
            raise ValueError("specified pv is not part of this vg")

        # for the time being we will not allow vgreduce
        if self.exists:
            raise VolumeGroupError("cannot remove pv from existing vg", self.name)

        self.parents.remove(pv)
        pv.removeChild()

        # and update our pv count
        self.pvCount = len(self.parents)

    # We can't rely on lvm to tell us about our size, free space, &c
    # since we could have modifications queued, unless the VG and all of
    # its PVs already exist.
    #
    #        -- liblvm may contain support for in-memory devices

    @property
    def isModified(self):
        """ Return True if the VG has changes queued that LVM is unaware of. """
        modified = True
        if self.exists and not filter(lambda d: not d.exists, self.pvs):
            modified = False

        return modified

    @property
    def size(self):
        """ The size of this VG """
        # TODO: just ask lvm if isModified returns False

        # sum up the sizes of the PVs and align to pesize
        size = 0
        for pv in self.pvs:
            ctx.logger.debug("PV size == %s" % pv.size)
            size += max(0, self.align(pv.size - pv.format.peStart))

        return size

    @property
    def extents(self):
        """ Number of extents in this VG """
        # TODO: just ask lvm if isModified returns False

        return self.size / self.peSize

    @property
    def freeSpace(self):
        """ The amount of free space in this VG (in MB). """
        # TODO: just ask lvm if isModified returns False

        # total the sizes of any LVs
        used = 0
        size = self.size
        ctx.logger.debug("%s size is %dMB" % (self.name, size))
        for lv in self.lvs:
            ctx.logger.debug("lv %s uses %dMB" % (lv.name, lv.vgSpaceUsed))
            used += self.align(lv.vgSpaceUsed, roundup=True)

        free = self.size - used
        ctx.logger.debug("vg %s has %dMB free" % (self.name, free))
        return free

    @property
    def freeExtents(self):
        """ The number of free extents in this VG. """
        # TODO: just ask lvm if isModified returns False
        return self.freeSpace / self.peSize

    def align(self, size, roundup=None):
        """ Align a size to a multiple of physical extent size. """
        size = numeric_type(size)

        if roundup:
            round = math.ceil
        else:
            round = math.floor

        # we want Kbytes as a float for our math
        size *= 1024.0
        pesize = self.peSize * 1024.0
        return long((round(size / pesize) * pesize) / 1024)

    @property
    def pvs(self):
        """ A list of this VG's PVs """
        return self.parents[:]  # we don't want folks changing our list

    @property
    def lvs(self):
        """ A list of this VG's LVs """
        return self._lvs[:]     # we don't want folks changing our list

    @property
    def complete(self):
        """Check if the vg has all its pvs in the system
        Return True if complete.
        """
        # vgs with duplicate names are overcomplete, which is not what we want
        if self.hasDuplicate:
            return False

        return len(self.pvs) == self.pvCount or not self.exists
