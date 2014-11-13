#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import parted
import block

import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import yali.baseudev
import yali.context as ctx
from yali.util import numeric_type
from yali.storage.library import devicemapper
from yali.storage.devices.device import Device, DeviceError, devicePathToName, deviceNameToDiskByPath
from yali.storage.formats import Format, getFormat
from yali.storage.formats.disklabel import DiskLabelCommitError

class PartitionError(DeviceError):
    pass

class Partition(Device):
    """ A disk partition.
    """
    _type = "partition"
    _resizable = True
    defaultSize = 500

    def __init__(self, name, format=None,
             size=None, grow=False, maxsize=None,
             major=None, minor=None, bootable=None,
             sysfsPath='', parents=None, exists=None,
             partType=None, primary=False, weight=0):

        """ Create a Partition instance.

            Arguments:

                name -- the device name (generally a device node's basename)

            Keyword Arguments:

                exists -- indicates whether this is an existing device
                format -- the device's format (DeviceFormat instance)

                For existing partitions:

                    parents -- the disk that contains this partition
                    major -- the device major
                    minor -- the device minor
                    sysfsPath -- sysfs device path

                For new partitions:

                    partType -- primary,extended,&c (as parted constant)
                    grow -- whether or not to grow the partition
                    maxsize -- max size for growable partitions (in MB)
                    size -- the device's size (in MB)
                    bootable -- whether the partition is bootable
                    parents -- a list of potential containing disks
                    weight -- an initial sorting weight to assign
        """
        self.req_disks = []
        self.req_partType = None
        self.req_primary = None
        self.req_grow = None
        self.req_bootable = None
        self.req_size = 0
        self.req_base_size = 0
        self.req_max_size = 0
        self.req_base_weight = 0

        self._bootable = False

        Device.__init__(self, name, format=format, size=size,
                        major=major, minor=minor, exists=exists,
                        sysfsPath=sysfsPath, parents=parents)
        if not exists:
            # this is a request, not a partition -- it has no parents
            self.req_disks = self.parents[:]
            for dev in self.parents:
                dev.removeChild()
            self.parents = []

        # FIXME: Validate partType, but only if this is a new partition
        #        Otherwise, overwrite it with the partition's type.
        self._partType = None
        self.partedFlags = {}
        self._partedPartition = None
        self._origPath = None
        self._currentSize = 0

        # FIXME: Validate size, but only if this is a new partition.
        #        For existing partitions we will get the size from
        #        parted.

        if self.exists:
            ctx.logger.debug("looking up parted Partition: %s" % self.path)
            self._partedPartition = self.disk.format.partedDisk.getPartitionByPath(self.path)
            if not self._partedPartition:
                raise PartitionError("cannot find parted partition instance", self.name)

            self._origPath = self.path
            self.probe()
            if self.getFlag(parted.PARTITION_PREP):
                # the only way to identify a PPC PReP Boot partition is to
                # check the partition type/flags, so do it here.
                self.format = getFormat("prepboot", device=self.path, exists=True)
        else:
            # XXX It might be worthwhile to create a shit-simple
            #     PartitionRequest class and pass one to this constructor
            #     for new partitions.
            if not self._size:
                # default size for new partition requests
                self._size = self.defaultSize
            self.req_name = name
            self.req_partType = partType
            self.req_primary = primary
            self.req_max_size = numeric_type(maxsize)
            self.req_grow = grow
            self.req_bootable = bootable

            # req_size may be manipulated in the course of partitioning
            self.req_size = self._size

            # req_base_size will always remain constant
            self.req_base_size = self._size

            self.req_base_weight = weight

    def __str__(self):
        s = Device.__str__(self)
        s += ("  grow = %(grow)s max size = %(maxsize)s  bootable = %(bootable)s\n"
              "  part type = %(partType)s  primary = %(primary)s\n"
              "  partedPartition = %(partedPart)r  disk = %(disk)r\n" %
              {"grow": self.req_grow, "maxsize": self.req_max_size,
               "bootable": self.bootable, "partType": self.partType,
               "primary": self.req_primary,
               "partedPart": self.partedPartition, "disk": self.disk})

        if self.partedPartition:
            s += ("  start = %(start)s  end = %(end)s  length = %(length)s\n"
                  "  flags = %(flags)s" %
                  {"length": self.partedPartition.geometry.length,
                   "start": self.partedPartition.geometry.start,
                   "end": self.partedPartition.geometry.end,
                   "flags": self.partedPartition.getFlagsAsString()})

        return s

    def _setTargetSize(self, newsize):
        if newsize != self.currentSize:
            # change this partition's geometry in-memory so that other
            # partitioning operations can complete (e.g., autopart)
            self._targetSize = newsize
            disk = self.disk.format.partedDisk

            # resize the partition's geometry in memory
            (constraint, geometry) = self._computeResize(self.partedPartition)
            disk.setPartitionGeometry(partition=self.partedPartition,
                                      constraint=constraint,
                                      start=geometry.start, end=geometry.end)

    @property
    def path(self):
        """ Device node representing this device. """
        if not self.parents:
            return self.name

        return "%s/%s" % (self.parents[0]._devDir, self.name)

    @property
    def partType(self):
        """ Get the partition's type (as parted constant). """
        try:
            ptype = self.partedPartition.type
        except AttributeError:
            ptype = self._partType

        if not self.exists and ptype is None:
            ptype = self.req_partType

        return ptype

    @property
    def isExtended(self):
        return (self.partType is not None and
                self.partType & parted.PARTITION_EXTENDED)

    @property
    def isLogical(self):
        return (self.partType is not None and
                self.partType & parted.PARTITION_LOGICAL)

    @property
    def isPrimary(self):
        return (self.partType is not None and
                self.partType == parted.PARTITION_NORMAL)

    @property
    def isProtected(self):
        return (self.partType is not None and
                self.partType & parted.PARTITION_PROTECTED)

    @property
    def fstabSpec(self):
        spec = self.path
        if self.disk and self.disk.type == 'dasd':
            spec = deviceNameToDiskByPath(self.name)
        elif self.format and self.format.uuid:
            spec = "UUID=%s" % self.format.uuid
        return spec

    def _getPartedPartition(self):
        return self._partedPartition

    def _setPartedPartition(self, partition):
        """ Set this Partition's parted Partition instance. """
        if partition is None:
            path = None
        elif isinstance(partition, parted.Partition):
            path = partition.path
        else:
            raise ValueError("partition must be a parted.Partition instance")

        ctx.logger.debug("device %s new partedPartition %s has path %s" % (self.name,
                                                                    partition,
                                                                    path))
        self._partedPartition = partition
        self.updateName()

    partedPartition = property(lambda d: d._getPartedPartition(),
                               lambda d,p: d._setPartedPartition(p))

    def preCommitFixup(self, *args, **kwargs):
        """ Re-get self.partedPartition from the original disklabel. """
        if not self.exists:
            return

        # find the correct partition on the original parted.Disk since the
        # name/number we're now using may no longer match
        _disklabel = self.disk.originalFormat

        if self.isExtended:
            # getPartitionBySector doesn't work on extended partitions
            _partition = _disklabel.extendedPartition
            ctx.logger.debug("extended lookup found partition %s"
                        % devicePathToName(getattr(_partition, "path", None)))
        else:
            # lookup the partition by sector to avoid the renumbering
            # nonsense entirely
            _sector = self.partedPartition.geometry.start
            _partition = _disklabel.partedDisk.getPartitionBySector(_sector)
            ctx.logger.debug("sector-based lookup found partition %s"
                        % devicePathToName(getattr(_partition, "path", None)))

        self.partedPartition = _partition

    def _getWeight(self):
        return self.req_base_weight

    def _setWeight(self, weight):
        self.req_base_weight = weight

    weight = property(lambda d: d._getWeight(),
                      lambda d,w: d._setWeight(w))

    def updateSysfsPath(self):
        """ Update this device's sysfs path. """
        if not self.parents:
            self.sysfsPath = ''

        elif self.parents[0]._devDir == "/dev/mapper":
            dm_node = devicemapper.dm_node_from_name(self.name)
            path = os.path.join("/sys", self.sysfsBlockDir, dm_node)
            self.sysfsPath = os.path.realpath(path)[4:]

        else:
            Device.updateSysfsPath(self)

    def updateName(self):
        if self.partedPartition is None:
            self._name = self.req_name
        else:
            self._name = \
                devicePathToName(self.partedPartition.getDeviceNodeName())

    def dependsOn(self, dep):
        """ Return True if this device depends on dep. """
        if isinstance(dep, Partition) and dep.isExtended and \
           self.isLogical and self.disk == dep.disk:
            return True

        return Device.dependsOn(self, dep)

    def _setFormat(self, format):
        """ Set the Device's format. """
        Device._setFormat(self, format)

    def _setBootable(self, bootable):
        """ Set the bootable flag for this partition. """
        if self.partedPartition:
            if self.flagAvailable(parted.PARTITION_BOOT):
                if bootable:
                    self.setFlag(parted.PARTITION_BOOT)
                else:
                    self.unsetFlag(parted.PARTITION_BOOT)
            else:
                raise PartitionError("boot flag not available for this partition", self.name)

            self._bootable = bootable
        else:
            self.req_bootable = bootable

    def _getBootable(self):
        return self._bootable or self.req_bootable

    bootable = property(_getBootable, _setBootable)

    def flagAvailable(self, flag):
        if not self.partedPartition:
            return

        return self.partedPartition.isFlagAvailable(flag)

    def getFlag(self, flag):
        if not self.partedPartition or not self.flagAvailable(flag):
            return

        return self.partedPartition.getFlag(flag)

    def setFlag(self, flag):
        if not self.partedPartition or not self.flagAvailable(flag):
            return

        self.partedPartition.setFlag(flag)

    def unsetFlag(self, flag):
        if not self.partedPartition or not self.flagAvailable(flag):
            return

        self.partedPartition.unsetFlag(flag)

    def probe(self):
        """ Probe for any missing information about this device.

            size, partition type, flags
        """
        if not self.exists:
            return

        # this is in MB
        self._size = self.partedPartition.getSize()
        self._currentSize = self._size
        self.targetSize = self._size

        self._partType = self.partedPartition.type

        self._bootable = self.getFlag(parted.PARTITION_BOOT)

    def create(self, intf=None):
        """ Create the device. """
        if self.exists:
            raise PartitionError("device already exists", self.name)

        w = None
        if intf:
            w = intf.progressWindow(_("Creating device %s") % (self.path,))


        try:
            self.createParents()
            self.setupParents()

            self.disk.format.addPartition(self.partedPartition)

            try:
                self.disk.format.commit()
            except DiskLabelCommitError, msg:
                part = self.disk.format.partedDisk.getPartitionByPath(self.path)
                self.disk.format.removePartition(part)
                raise PartitionError, msg

            if not self.isExtended:
                # Ensure old metadata which lived in freespace so did not get
                # explictly destroyed by a destroyformat action gets wiped
                Format(device=self.path, exists=True).destroy()
        except Exception, msg:
            raise PartitionError("Create device failed!", self.name)
        else:
            self.partedPartition = self.disk.format.partedDisk.getPartitionByPath(self.path)

            self.exists = True
            self._currentSize = self.partedPartition.getSize()
            self.setup()
        finally:
            if w:
                w.pop()

    def _computeResize(self, partition):
        # compute new size for partition
        currentGeom = partition.geometry
        currentDev = currentGeom.device
        newLen = long(self.targetSize * 1024 * 1024) / currentDev.sectorSize
        newGeometry = parted.Geometry(device=currentDev,
                                      start=currentGeom.start,
                                      length=newLen)
        # and align the end sector
        newGeometry.end = self.disk.format.endAlignment.alignDown(newGeometry,
                                                               newGeometry.end)
        constraint = parted.Constraint(exactGeom=newGeometry)

        return (constraint, newGeometry)

    def resize(self, intf=None):
        """ Resize the device.

            self.targetSize must be set to the new size.
        """
        if self.targetSize != self.currentSize:
            # partedDisk has been restored to _origPartedDisk, so
            # recalculate resize geometry because we may have new
            # partitions on the disk, which could change constraints
            partedDisk = self.disk.format.partedDisk
            partition = partedDisk.getPartitionByPath(self.path)
            (constraint, geometry) = self._computeResize(partition)

            partedDisk.setPartitionGeometry(partition=partition,
                                            constraint=constraint,
                                            start=geometry.start,
                                            end=geometry.end)

            self.disk.format.commit()
            self._currentSize = partition.getSize()

    def destroy(self):
        """ Destroy the device. """
        if not self.exists:
            raise PartitionError("device has not been created", self.name)

        if not self.sysfsPath:
            return

        if not self.isleaf:
            raise PartitionError("Cannot destroy non-leaf device", self.name)

        self.setupParents(orig=True)

        # we should have already set self.partedPartition to point to the
        # partition on the original disklabel
        self.disk.originalFormat.removePartition(self.partedPartition)
        try:
            self.disk.originalFormat.commit()
        except DiskLabelCommitError, msg:
            self.disk.originalFormat.addPartition(self.partedPartition)
            self.partedPartition = self.disk.originalFormat.partedDisk.getPartitionByPath(self.path)
            raise PartitionError, msg

        self.exists = False

    def teardown(self, recursive=None):
        """ Close, or tear down, a device. """
        if not self.exists and not recursive:
            raise PartitionError("device has not been created", self.name)

        if self.status:
            if self.originalFormat.exists:
                self.originalFormat.teardown()
            if self.format.exists:
                self.format.teardown()
            if self.parents[0].type == 'dm-multipath':
                devmap = block.getMap(major=self.major, minor=self.minor)
                if devmap:
                    try:
                        block.removeDeviceMap(devmap)
                    except Exception as e:
                        raise PartitionError("failed to tear down device-mapper partition %s: %s" % (self.name, e))
                yali.baseudev.udev_settle()

        Device.teardown(self, recursive=recursive)

    def _getSize(self):
        """ Get the device's size. """
        size = self._size
        if self.partedPartition:
            # this defaults to MB
            size = self.partedPartition.getSize()
        return size

    def _setSize(self, newsize):
        """ Set the device's size (for resize, not creation).

            Arguments:

                newsize -- the new size (in MB)

        """
        if not self.exists:
            raise PartitionError("device does not exist", self.name)

        if newsize > self.disk.size:
            raise ValueError("partition size would exceed disk size")

        # this defaults to MB
        maxAvailableSize = self.partedPartition.getMaxAvailableSize()

        if newsize > maxAvailableSize:
            raise ValueError("new size is greater than available space")

         # now convert the size to sectors and update the geometry
        geometry = self.partedPartition.geometry
        physicalSectorSize = geometry.device.physicalSectorSize

        new_length = (newsize * (1024 * 1024)) / physicalSectorSize
        geometry.length = new_length

    def _getDisk(self):
        """ The disk that contains this partition."""
        try:
            disk = self.parents[0]
        except IndexError:
            disk = None
        return disk

    def _setDisk(self, disk):
        """Change the parent.

        Setting up a disk is not trivial.  It has the potential to change
        the underlying object.  If necessary we must also change this object.
        """
        if self.disk:
            self.disk.removeChild()

        if disk:
            self.parents = [disk]
            disk.addChild()
        else:
            self.parents = []

    disk = property(lambda p: p._getDisk(), lambda p,d: p._setDisk(d))

    @property
    def maxSize(self):
        """ The maximum size this partition can be. """
        # XXX: this is MB by default
        maxPartSize = self.partedPartition.getMaxAvailableSize()

        if self.format.maxSize > maxPartSize:
            return maxPartSize
        else:
            return self.format.maxSize

    @property
    def currentSize(self):
        """ The device's actual size. """
        if self.exists:
            return self._currentSize
        else:
            return 0
    def dependsOn(self, dep):
        """ Return True if this device depends on dep. """
        if isinstance(dep, Partition) and dep.isExtended and \
           self.isLogical and self.disk == dep.disk:
            return True

        return Device.dependsOn(self, dep)
