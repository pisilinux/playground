#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import parted
from operator import add, sub, gt, lt
import gettext

__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import yali.util
import yali.context as ctx
from yali.storage import StorageError
from yali.storage.operations import *
from yali.storage.devices.device import devicePathToName
from yali.storage.devices.partition import Partition

CLEARPART_TYPE_ALL, CLEARPART_TYPE_LINUX, CLEARPART_TYPE_NONE = range(3)

class PartitioningError(StorageError):
    pass

class PartitioningWarning(StorageError):
    pass

class Request(object):
    """ A partition request.

        Request instances are used for calculating how much to grow
        partitions.
    """
    def __init__(self, partition):
        """ Create a Request instance.

            Arguments:

                partition -- a Partition instance

        """
        self.partition = partition          # storage.devices.partition.Partition
        self.growth = 0                     # growth in sectors
        self.max_growth = 0                 # max growth in sectors
        self.done = not partition.req_grow  # can we grow this request more?
        self.base = partition.partedPartition.geometry.length   # base sectors

        sector_size = partition.partedPartition.disk.device.sectorSize

        if partition.req_grow:
            limits = filter(lambda l: l > 0,
                        [sizeToSectors(partition.req_max_size, sector_size),
                         sizeToSectors(partition.format.maxSize, sector_size),
                         partition.partedPartition.disk.maxPartitionLength])

            if limits:
                max_sectors = min(limits)
                self.max_growth = max_sectors - self.base

    @property
    def growable(self):
        """ True if this request is growable. """
        return self.partition.req_grow

    @property
    def id(self):
        """ The id of the Partition this request corresponds to. """
        return self.partition.id

    def __str__(self):
        s = ("%(type)s instance --\n"
             "id = %(id)s  name = %(name)s  growable = %(growable)s\n"
             "base = %(base)d  growth = %(growth)d  max_grow = %(max_grow)d\n"
             "done = %(done)s" %
             {"type": self.__class__.__name__, "id": self.id,
              "name": self.partition.name, "growable": self.growable,
              "base": self.base, "growth": self.growth,
              "max_grow": self.max_growth, "done": self.done})
        return s

class Chunk(object):
    """ A free region on disk from which partitions will be allocated """
    def __init__(self, geometry, requests=None):
        """ Create a Chunk instance.

            Arguments:

                geometry -- parted.Geometry instance describing the free space


            Keyword Arguments:

                requests -- list of Request instances allocated from this chunk

        """
        self.geometry = geometry            # parted.Geometry
        self.pool = self.geometry.length    # free sector count
        self.sectorSize = self.geometry.device.sectorSize
        self.base = 0                       # sum of growable requests' base
                                            # sizes, in sectors
        self.requests = []                  # list of Request instances
        if isinstance(requests, list):
            for req in requests:
                self.addRequest(req)

    def __str__(self):
        s = ("%(type)s instance --\n"
             "device = %(device)s  start = %(start)d  end = %(end)d\n"
             "length = %(length)d  size = %(size)d pool = %(pool)d\n"
             "remaining = %(rem)d  sectorSize = %(sectorSize)d" %
             {"type": self.__class__.__name__,
              "device": self.geometry.device.path,
              "start": self.geometry.start, "end": self.geometry.end,
              "length": self.geometry.length, "size": self.geometry.getSize(),
              "pool": self.pool, "rem": self.remaining,
              "sectorSize": self.sectorSize})

        return s

    def addRequest(self, req):
        """ Add a Request to this chunk. """
        ctx.logger.debug("adding request %d to chunk %s" % (req.partition.id, self))
        self.requests.append(req)
        self.pool -= req.base

        if not req.done:
            self.base += req.base

    def getRequestByID(self, id):
        """ Retrieve a request from this chunk based on its id. """
        for request in self.requests:
            if request.id == id:
                return request

    @property
    def growth(self):
        """ Sum of growth in sectors for all requests in this chunk. """
        return sum(r.growth for r in self.requests)

    @property
    def hasGrowable(self):
        """ True if this chunk contains at least one growable request. """
        for req in self.requests:
            if req.growable:
                return True
        return False

    @property
    def remaining(self):
        """ Number of requests still being grown in this chunk. """
        return len([d for d in self.requests if not d.done])

    @property
    def done(self):
        """ True if we are finished growing all requests in this chunk. """
        return self.remaining == 0

    def trimOverGrownRequest(self, req, base=None):
        """ Enforce max growth and return extra sectors to the pool. """
        if req.max_growth and req.growth >= req.max_growth:
            if req.growth > req.max_growth:
                # we've grown beyond the maximum. put some back.
                extra = req.growth - req.max_growth
                ctx.logger.debug("taking back %d (%dMB) from %d (%s)" %
                            (extra,
                             sectorsToSize(extra, self.sectorSize),
                             req.partition.id, req.partition.name))
                self.pool += extra
                req.growth = req.max_growth

            # We're done growing this partition, so it no longer
            # factors into the growable base used to determine
            # what fraction of the pool each request gets.
            if base is not None:
                base -= req.base
            req.done = True

        return base

    def growRequests(self):
        """ Calculate growth amounts for requests in this chunk. """
        ctx.logger.debug("Chunk.growRequests: %s" % self)

        # sort the partitions by start sector
        self.requests.sort(key=lambda r: r.partition.partedPartition.geometry.start)

        # we use this to hold the base for the next loop through the
        # chunk's requests since we want the base to be the same for
        # all requests in any given growth iteration
        new_base = self.base
        last_pool = 0 # used to track changes to the pool across iterations
        while not self.done and self.pool and last_pool != self.pool:
            last_pool = self.pool    # to keep from getting stuck
            self.base = new_base
            ctx.logger.debug("%d partitions and %d (%dMB) left in chunk" %
                        (self.remaining, self.pool,
                         sectorsToSize(self.pool, self.sectorSize)))
            for p in self.requests:
                if p.done:
                    continue

                # Each partition is allocated free sectors from the pool
                # based on the relative _base_ sizes of the remaining
                # growable partitions.
                share = p.base / float(self.base)
                growth = int(share * last_pool) # truncate, don't round
                p.growth += growth
                self.pool -= growth
                ctx.logger.debug("adding %d (%dMB) to %d (%s)" %
                            (growth,
                             sectorsToSize(growth, self.sectorSize),
                             p.partition.id, p.partition.name))

                new_base = self.trimOverGrownRequest(p, base=new_base)
                ctx.logger.debug("new grow amount for partition %d (%s) is %d "
                          "sectors, or %dMB" %
                            (p.partition.id, p.partition.name, p.growth,
                             sectorsToSize(p.growth, self.sectorSize)))

        if self.pool:
            # allocate any leftovers in pool to the first partition
            # that can still grow
            for p in self.requests:
                if p.done:
                    continue

                p.growth += self.pool
                self.pool = 0

                self.trimOverGrownRequest(p)
                if self.pool == 0:
                    break


class PartitionSpec(object):
    def __init__(self, mountpoint=None, fstype=None, size=None, maxSize=None,
                 grow=False, asVol=False, weight=0, requiredSpace=0):
        """ Create a new storage specification.  These are used to specify
            the default partitioning layout as an object before we have the
            storage system up and running.  The attributes are obvious
            except for the following:

            asVol -- Should this be allocated as a logical volume?  If not,
                     it will be allocated as a partition.
            weight -- An integer that modifies the sort algorithm for partition
                      requests.  A larger value means the partition will end up
                      closer to the front of the disk.  This is mainly used to
                      make sure /boot ends up in front, and any special (PReP,
                      appleboot, etc.) partitions end up in front of /boot.
                      This value means nothing if asVol=False.
            requiredSpace -- This value is only taken into account if
                             asVol=True, and specifies the size in MB that the
                             containing VG must be for this PartSpec to even
                             get used.  The VG's size is calculated before any
                             other LVs are created inside it.  If not enough
                             space exists, this PartSpec will never get turned
                             into an LV.
        """

        self.mountpoint = mountpoint
        self.fstype = fstype
        self.size = size
        self.maxSize = maxSize
        self.grow = grow
        self.asVol = asVol
        self.weight = weight
        self.requiredSpace = requiredSpace

    def __str__(self):
        s = ("%(type)s instance (%(id)s) -- \n"
             "  mountpoint = %(mountpoint)s  asVol = %(asVol)s\n"
             "  weight = %(weight)s  fstype = %(fstype)s\n"
             "  size = %(size)s  maxSize = %(maxSize)s  grow = %(grow)s\n" %
             {"type": self.__class__.__name__, "id": "%#x" % id(self),
              "mountpoint": self.mountpoint, "asVol": self.asVol,
              "weight": self.weight, "fstype": self.fstype, "size": self.size,
              "maxSize": self.maxSize, "grow": self.grow})

        return s


def sectorsToSize(sectors, sectorSize):
    """ Convert length in sectors to size in MB.

        Arguments:

            sectors     -   sector count
            sectorSize  -   sector size for the device, in bytes
    """
    return (sectors * sectorSize) / (1024.0 * 1024.0)

def sizeToSectors(size, sectorSize):
    """ Convert size in MB to length in sectors.

        Arguments:

            size        -   size in MB
            sectorSize  -   sector size for the device, in bytes
    """
    return (size * 1024.0 * 1024.0) / sectorSize

def clearPartitions(storage):
    """ Clear partitions and dependent devices from disks.

        Arguments:

            storage -- a storage.Storage instance

        Keyword arguments:

            None

        NOTES:

            - Needs some error handling, especially for the parted bits.

    """
    if storage.clearPartType is None or storage.clearPartType == CLEARPART_TYPE_NONE:
        # not much to do
        return

    # we are only interested in partitions that physically exist
    partitions = [p for p in storage.partitions if p.exists]
    # Sort partitions by descending partition number to minimize confusing
    # things like multiple "destroy sda5" actions due to parted renumbering
    # partitions. This can still happen through the UI but it makes sense to
    # avoid it where possible.
    partitions.sort(key=lambda p: p.partedPartition.number, reverse=True)
    for part in partitions:
        ctx.logger.debug("clearpart: looking at %s" % part.name)
        if not shouldClear(part, storage.clearPartType, storage.clearPartDisks):
            continue

        ctx.logger.debug("clearing %s" % part.name)

        # XXX is there any argument for not removing incomplete devices?
        #       -- maybe some RAID devices
        devices = storage.deviceDeps(part)
        while devices:
            ctx.logger.debug("devices to remove: %s" % ([d.name for d in devices],))
            leaves = [d for d in devices if d.isleaf]
            ctx.logger.debug("leaves to remove: %s" % ([d.name for d in leaves],))
            for leaf in leaves:
                storage.destroyDevice(leaf)
                devices.remove(leaf)

        ctx.logger.debug("partitions: %s" % [p.getDeviceNodeName() for p in part.partedPartition.disk.partitions])
        storage.destroyDevice(part)

    # now remove any empty extended partitions
    removeEmptyExtendedPartitions(storage)

    # make sure that the the boot device has the correct disklabel type if
    # we're going to completely clear it.
    for disk in storage.partitioned:
        if not storage.drives:
            break

        if disk.name != ctx.bootloader.drives[0]:
            continue

        if storage.clearPartType != CLEARPART_TYPE_ALL or \
           (storage.clearPartDisks and disk.name not in storage.clearPartDisks):
            continue

        # don't reinitialize the disklabel if the disk contains install media
        if filter(lambda p: p.dependsOn(disk), storage.protectedDevices):
            continue

        if yali.util.isEfi():
            nativeLabelType = "gpt"
        else:
            nativeLabelType = "msdos"

        if disk.format.labelType == nativeLabelType:
            continue

        if disk.format.labelType == "mac":
            for part in storage.partitions:
                if part.disk == disk and part.partedPartition.number == 1:
                    ctx.logger.debug("clearing %s" % part.name)
                    # We can't schedule the apple map partition for removal
                    # because parted will not allow us to remove it from the
                    # disk. Still, we need it out of the devicetree.
                    storage.devicetree._removeDevice(part, moddisk=False)

        destroy = OperationDestroyFormat(disk)
        newLabel = getFormat("disklabel", device=disk.path)
        create = OperationCreateFormat(disk, format=newLabel)
        storage.devicetree.addOperation(destroy)
        storage.devicetree.addOperation(create)

def removeEmptyExtendedPartitions(storage):
    for disk in storage.partitioned:
        ctx.logger.debug("checking whether disk %s has an empty extended" % disk.name)
        extended = disk.format.extendedPartition
        logical_parts = disk.format.logicalPartitions
        ctx.logger.debug("extended is %s ; logicals is %s" % (extended, [p.getDeviceNodeName() for p in logical_parts]))
        if extended and not logical_parts:
            ctx.logger.debug("removing empty extended partition from %s" % disk.name)
            extended_name = devicePathToName(extended.getDeviceNodeName())
            extended = storage.devicetree.getDeviceByName(extended_name)
            storage.destroyDevice(extended)

    for disk in [d for d in storage.disks if d not in storage.partitioned]:
        # clear any whole-disk formats that need clearing
        if shouldClear(disk, storage.clearPartType, storage.clearPartDisks):
            ctx.logger.debug("clearing %s" % disk.name)
            devices = storage.deviceDeps(disk)
            while devices:
                ctx.logger.debug("devices to remove: %s" % ([d.name for d in devices],))
                leaves = [d for d in devices if d.isleaf]
                ctx.logger.debug("leaves to remove: %s" % ([d.name for d in leaves],))
                for leaf in leaves:
                    storage.destroyDevice(leaf)
                    devices.remove(leaf)

            destroy = OperationDestroyFormat(disk)
            newLabel = getFormat("disklabel", device=disk.path)
            create = OperationCreateFormat(disk, format=newLabel)
            storage.devicetree.addOperation(destroy)
            storage.devicetree.addOperation(create)

def partitionCompare(part1, part2):
    """ More specifically defined partitions come first.

        < 1 => x < y
          0 => x == y
        > 1 => x > y
    """
    ret = 0

    if part1.req_base_weight:
        ret -= part1.req_base_weight

    if part2.req_base_weight:
        ret += part2.req_base_weight

    # bootable partitions to the front
    ret -= cmp(part1.req_bootable, part2.req_bootable) * 1000

    # more specific disk specs to the front of the list
    # req_disks being empty is equivalent to it being an infinitely long list
    if part1.req_disks and not part2.req_disks:
        ret -= 500
    elif not part1.req_disks and part2.req_disks:
        ret += 500
    else:
        ret += cmp(len(part1.req_disks), len(part2.req_disks)) * 500

    # primary-only to the front of the list
    ret -= cmp(part1.req_primary, part2.req_primary) * 200

    # fixed size requests to the front
    ret += cmp(part1.req_grow, part2.req_grow) * 100

    # larger requests go to the front of the list
    ret -= cmp(part1.req_base_size, part2.req_base_size) * 50

    # potentially larger growable requests go to the front
    if part1.req_grow and part2.req_grow:
        if not part1.req_max_size and part2.req_max_size:
            ret -= 25
        elif part1.req_max_size and not part2.req_max_size:
            ret += 25
        else:
            ret -= cmp(part1.req_max_size, part2.req_max_size) * 25

    # give a little bump based on mountpoint
    if hasattr(part1.format, "mountpoint") and \
       hasattr(part2.format, "mountpoint"):
        ret += cmp(part1.format.mountpoint, part2.format.mountpoint) * 10

    if ret > 0:
        ret = 1
    elif ret < 0:
        ret = -1

    return ret

def getNextPartitionType(disk, no_primary=None):
    """ Find the type of partition to create next on a disk.

        Return a parted partition type value representing the type of the
        next partition we will create on this disk.

        If there is only one free primary partition and we can create an
        extended partition, we do that.

        If there are free primary slots and an extended partition we will
        recommend creating a primary partition. This can be overridden
        with the keyword argument no_primary.

        Arguments:

            disk -- a parted.Disk instance representing the disk

        Keyword arguments:

            no_primary -- given a choice between primary and logical
                          partitions, prefer logical

    """
    partType = None
    extended = disk.getExtendedPartition()
    supportsExtended = disk.supportsFeature(parted.DISK_TYPE_EXTENDED)
    logicalCount = len(disk.getLogicalPartitions())
    maxLogicals = disk.getMaxLogicalPartitions()
    primaryCount = disk.primaryPartitionCount

    if primaryCount < disk.maxPrimaryPartitionCount:
        if primaryCount == disk.maxPrimaryPartitionCount - 1:
            # can we make an extended partition? now's our chance.
            if not extended and supportsExtended:
                partType = parted.PARTITION_EXTENDED
            elif not extended:
                # extended partitions not supported. primary or nothing.
                if not no_primary:
                    partType = parted.PARTITION_NORMAL
            else:
                # there is an extended and a free primary
                if not no_primary:
                    partType = parted.PARTITION_NORMAL
                elif logicalCount < maxLogicals:
                    # we have an extended with logical slots, so use one.
                    partType = parted.PARTITION_LOGICAL
        else:
            # there are two or more primary slots left. use one unless we're
            # not supposed to make primaries.
            if not no_primary:
                partType = parted.PARTITION_NORMAL
            elif extended and logicalCount < maxLogicals:
                partType = parted.PARTITION_LOGICAL
    elif extended and logicalCount < maxLogicals:
        partType = parted.PARTITION_LOGICAL

    return partType

def getFreeRegions(disks):
    """ Return a list of free regions on the specified disks.

        Arguments:

            disks -- list of parted.Disk instances

        Return value is a list of unaligned parted.Geometry instances.

    """
    free = []
    for disk in disks:
        for f in disk.format.partedDisk.getFreeSpaceRegions():
            if f.length > 0:
                free.append(f)

    return free

def getBestFreeSpaceRegion(disk, part_type, req_size, boot=None, best_free=None, grow=None):
    """ Return the "best" free region on the specified disk.

        Arguments:

            disk -- the disk (a parted.Disk instance)
            part_type -- the type of partition we want to allocate
                         (one of parted's partition type constants)
            req_size -- the requested size of the partition (in MB)

        Keyword arguments:

            boot -- indicates whether this will be a bootable partition
                    (boolean)
            best_free -- current best free region for this partition
            grow -- indicates whether this is a growable request
    """
    ctx.logger.debug("getBestFreeSpaceRegion: disk=%s part_type=%d"
                     "req_size=%dMB boot=%s best=%s grow=%s" %
                    (disk.device.path, part_type, req_size, boot, best_free, grow))

    extended = disk.getExtendedPartition()

    for _range in disk.getFreeSpaceRegions():
        if extended:
            ctx.logger.debug("looking for intersection between extended (%d-%d) and free (%d-%d)" %
                    (extended.geometry.start, extended.geometry.end, _range.start, _range.end))

            try:
                free_geom = extended.geometry.intersect(_range)
            except ArithmeticError, e:
                free_geom = None

            if (free_geom and part_type == parted.PARTITION_NORMAL) or \
               (not free_geom and part_type == parted.PARTITION_LOGICAL):
                ctx.logger.debug("free_geom region not suitable for request")
                continue

            if part_type == parted.PARTITION_NORMAL:
                free_geom = _range
        else:
            free_geom = _range

        if free_geom.start > disk.maxPartitionStartSector:
            ctx.logger.debug("free_geom range start sector beyond max for new partitions")
            continue

        ctx.logger.debug("current free_geom range is %d-%d (%dMB)" %
                        (free_geom.start, free_geom.end, free_geom.getSize()))
        free_size = free_geom.getSize()

        # For boot partitions, we want the first suitable region we find.
        # For growable or extended partitions, we want the largest possible
        # free_geom region.
        # For all others, we want the smallest suitable free_geom region.
        if grow or part_type == parted.PARTITION_EXTENDED:
            op = gt
        else:
            op = lt
        if req_size <= free_size:
            if not best_free or op(free_geom.length, best_free.length):
                best_free = free_geom

                if boot:
                    # if this is a bootable partition we want to
                    # use the first freespace region large enough
                    # to satisfy the request
                    break

    return best_free

def removeNewPartitions(disks, partitions):
    """ Remove newly added input partitions from input disks.

        Arguments:

            disks -- list of Device instances with DiskLabel format
            partitions -- list of Partition instances

    """
    ctx.logger.debug("removing all non-preexisting partitions %s from disk(s) %s"
                % (["%s(id %d)" % (p.name, p.id) for p in partitions
                                                    if not p.exists],
                   [d.name for d in disks]))
    for part in partitions:
        if part.partedPartition and part.disk in disks:
            if part.exists:
                # we're only removing partitions that don't physically exist
                continue

            if part.isExtended:
                # these get removed last
                continue

            part.disk.format.partedDisk.removePartition(part.partedPartition)
            part.partedPartition = None
            part.disk = None

    for disk in disks:
        # remove empty extended so it doesn't interfere
        extended = disk.format.extendedPartition
        if extended and not disk.format.logicalPartitions:
            ctx.logger.debug("removing empty extended partition from %s" % disk.name)
            disk.format.partedDisk.removePartition(extended)

def addPartition(disk, free, part_type, size):
    """ Return new partition after adding it to the specified disk.

        Arguments:

            disklabel -- disklabel instance to add partition to
            free -- where to add the partition (parted.Geometry instance)
            part_type -- partition type (parted.PARTITION_* constant)
            size -- size (in MB) of the new partition

        The new partition will be aligned.

        Return value is a parted.Partition instance.

    """
    start = free.start
    if not disk.alignment.isAligned(free, start):
        start = disk.alignment.alignNearest(free, start)

    if part_type == parted.PARTITION_LOGICAL:
        # make room for logical partition's metadata
        start += disk.alignment.grainSize

    if start != free.start:
        ctx.logger.debug("adjusted start sector from %d to %d" % (free.start, start))

    if part_type == parted.PARTITION_EXTENDED:
        end = free.end
        length = end - start + 1
    else:
        # size is in MB
        length = sizeToSectors(size, disk.partedDevice.sectorSize)
        end = start + length - 1

    if not disk.endAlignment.isAligned(free, end):
        end = disk.endAlignment.alignNearest(free, end)
        ctx.logger.debug("adjusted length from %d to %d" % (length, end - start + 1))

    newGeom = parted.Geometry(device=disk.partedDevice, start=start, end=end)

    maxLength = disk.partedDisk.maxPartitionLength
    if maxLength and newGeom.length > maxLength:
        raise PartitioningError(_("requested size exceeds maximum allowed"))

    # create the partition and add it to the disk
    partition = parted.Partition(disk=disk.partedDisk,
                                 type=part_type,
                                 geometry=newGeom)
    constraint = parted.Constraint(exactGeom=newGeom)
    disk.partedDisk.addPartition(partition=partition, constraint=constraint)
    return partition

def doPartitioning(storage, exclusiveDisks=None):
    """ Allocate and grow partitions.

        When this function returns without error, all Partition
        instances must have their parents set to the disk they are
        allocated on, and their partedPartition attribute set to the
        appropriate parted.Partition instance from their containing
        disk. All req_xxxx attributes must be unchanged.

        Arguments:

            storage - Main Storage instance

        Keyword arguments:

            exclusiveDisks -- list of names of disks to use

    """
    disks = storage.partitioned
    if exclusiveDisks:
        disks = [d for d in disks if d.name in exclusiveDisks]

    for disk in disks:
        disk.setup()

    partitions = storage.partitions[:]
    for part in storage.partitions:
        part.req_bootable = False

        if part.exists or \
           (storage.deviceImmutable(part) and part.partedPartition):
            # if the partition is preexisting or part of a complex device
            # then we shouldn't modify it
            partitions.remove(part)
            continue

        if not part.exists:
            # start over with flexible-size requests
            part.req_size = part.req_base_size

    # FIXME: isn't there a better place for this to happen?
    try:
        bootDev = storage.storageset.bootDevice
    except PartitioningError:
        bootDev = None

    if bootDev:
        bootDev.req_bootable = True

    removeNewPartitions(disks, partitions)
    free = getFreeRegions(disks)
    allocatePartitions(storage, disks, partitions, free)
    growPartitions(disks, partitions, free)

    # The number and thus the name of partitions may have changed now,
    # allocatePartitions() takes care of this for new partitions, but not
    # for pre-existing ones, so we update the name of all partitions here
    for part in storage.partitions:
        # needed because of XXX hack below
        if part.isExtended:
            continue
        part.updateName()

    # XXX hack -- if we created any extended partitions we need to add
    #             them to the tree now
    for disk in disks:
        extended = disk.format.extendedPartition
        if not extended:
            # remove any obsolete extended partitions
            for part in storage.partitions:
                if part.disk == disk and part.isExtended:
                    if part.exists:
                        storage.destroyDevice(part)
                    else:
                        storage.devicetree._removeDevice(part, moddisk=False)
            continue

        extendedName = devicePathToName(extended.getDeviceNodeName())
        # remove any obsolete extended partitions
        for part in storage.partitions:
            if part.disk == disk and part.isExtended and \
               part.partedPartition not in disk.format.partitions:
                if part.exists:
                    storage.destroyDevice(part)
                else:
                    storage.devicetree._removeDevice(part, moddisk=False)

        device = storage.devicetree.getDeviceByName(extendedName)
        if device:
            if not device.exists:
                # created by us, update partedPartition
                device.partedPartition = extended
            continue

        # This is a little odd because normally instantiating a partition
        # that does not exist means leaving self.parents empty and instead
        # populating self.req_disks. In this case, we need to skip past
        # that since this partition is already defined.
        device = Partition(extendedName, parents=disk)
        device.parents = [disk]
        device.partedPartition = extended
        # just add the device for now -- we'll handle actions at the last
        # moment to simplify things
        storage.devicetree._addDevice(device)

def allocatePartitions(storage, disks, partitions, freespace):
    """ Allocate partitions based on requested features.

        Non-existing partitions are sorted according to their requested
        attributes, and then allocated.

        The basic approach to sorting is that the more specifically-
        defined a request is, the earlier it will be allocated. See
        the function partitionCompare for details on the sorting
        criteria.

        The Partition instances will have their name and parents
        attributes set once they have been allocated.
    """
    ctx.logger.debug("allocatePartitions: disks=%s ; partitions=%s" %
                ([d.name for d in disks],
                 ["%s(id %d)" % (p.name, p.id) for p in partitions]))

    new_partitions = [p for p in partitions if not p.exists]
    new_partitions.sort(cmp=partitionCompare)

    # the following dicts all use device path strings as keys
    disklabels = {}     # DiskLabel instances for each disk
    all_disks = {}      # Device for each disk
    for disk in disks:
        if disk.path not in disklabels.keys():
            disklabels[disk.path] = disk.format
            all_disks[disk.path] = disk

    removeNewPartitions(disks, new_partitions)

    for _part in new_partitions:
        if _part.partedPartition and _part.isExtended:
            # ignore new extendeds as they are implicit requests
            continue

        # obtain the set of candidate disks
        req_disks = []
        if _part.disk:
            # we have a already selected a disk for this request
            req_disks = [_part.disk]
        elif _part.req_disks:
            # use the requested disk set
            req_disks = _part.req_disks
        else:
            # no disks specified means any disk will do
            req_disks = disks

        # sort the disks, making sure the boot disk is first
        req_disks.sort(key=lambda d: d.name, cmp=storage.compareDisks)
        boot_index = None
        for disk in req_disks:
            if disk.name == storage.drives[0]:
                boot_index = req_disks.index(disk)

        if boot_index is not None and len(req_disks) > 1:
            boot_disk = req_disks.pop(boot_index)
            req_disks.insert(0, boot_disk)

        ctx.logger.debug("allocating partition: %s ; id: %d ; disks: %s ;\n"
                         "boot: %s ; primary: %s ; size: %dMB ; grow:%s; max_size: %s" %
                        (_part.name, _part.id, [d.name for d in req_disks],
                        _part.req_bootable, _part.req_primary,_part.req_size,
                        _part.req_grow, _part.req_max_size))
        free = None
        use_disk = None
        part_type = None
        growth = 0
        # loop through disks
        for _disk in req_disks:
            disklabel = disklabels[_disk.path]
            sectorSize = disklabel.partedDevice.sectorSize
            best = None
            current_free = free

            # for growable requests, we don't want to pass the current free
            # geometry to getBestFreeRegion -- this allows us to try the
            # best region from each disk and choose one based on the total
            # growth it allows
            if _part.req_grow:
                current_free = None

            problem = None
            if _part.format.maxSize and _part.req_size > _part.format.maxSize:
                problem = "large"
            elif (_part.format.minSize and
                  (not _part.req_grow and
                   _part.req_size < _part.format.minSize) or
                  (_part.req_grow and _part.req_max_size and
                   _part.req_max_size < _part.format.minSize)):
                problem = "small"

            if problem:
                raise PartitioningError(_("partition is too %(problem)s for %(format)s formatting")
                                        % {"problem":problem, "format":_part.format.name})

            ctx.logger.debug("checking freespace on %s" % _disk.name)

            new_part_type = getNextPartitionType(disklabel.partedDisk)
            if new_part_type is None:
                # can't allocate any more partitions on this disk
                ctx.logger.debug("no free partition slots on %s" % _disk.name)
                continue

            if _part.req_primary and new_part_type != parted.PARTITION_NORMAL:
                if (disklabel.partedDisk.primaryPartitionCount <
                    disklabel.partedDisk.maxPrimaryPartitionCount):
                    # don't fail to create a primary if there are only three
                    # primary partitions on the disk (#505269)
                    new_part_type = parted.PARTITION_NORMAL
                else:
                    # we need a primary slot and none are free on this disk
                    ctx.logger.debug("no primary slots available on %s" % _disk.name)
                    continue

            best = getBestFreeSpaceRegion(disklabel.partedDisk,
                                          new_part_type,
                                          _part.req_size,
                                          best_free=current_free,
                                          boot=_part.req_bootable,
                                          grow=_part.req_grow)

            if best == free and not _part.req_primary and \
               new_part_type == parted.PARTITION_NORMAL:
                # see if we can do better with a logical partition
                ctx.logger.debug("not enough free space for primary -- trying logical")
                new_part_type = getNextPartitionType(disklabel.partedDisk, no_primary=True)
                if new_part_type:
                    best = getBestFreeSpaceRegion(disklabel.partedDisk,
                                                  new_part_type,
                                                  _part.req_size,
                                                  best_free=current_free,
                                                  boot=_part.req_bootable,
                                                  grow=_part.req_grow)

            if best and free != best:
                update = True
                if _part.req_grow:
                    ctx.logger.debug("evaluating growth potential for new layout")
                    new_growth = 0
                    for disk_path in disklabels.keys():
                        ctx.logger.debug("calculating growth for disk %s" % disk_path)
                        # Now we check, for growable requests, which of the two
                        # free regions will allow for more growth.

                        # set up chunks representing the disks' layouts
                        temp_parts = []
                        for _p in new_partitions[:new_partitions.index(_part)]:
                            if _p.disk.path == disk_path:
                                temp_parts.append(_p)

                        # add the current request to the temp disk to set up
                        # its partedPartition attribute with a base geometry
                        if disk_path == _disk.path:
                            temp_part = addPartition(disklabel,
                                                     best,
                                                     new_part_type,
                                                     _part.req_size)
                            _part.partedPartition = temp_part
                            _part.disk = _disk
                            temp_parts.append(_part)

                        chunks = getDiskChunks(all_disks[disk_path],
                                               temp_parts, freespace)

                        # grow all growable requests
                        disk_growth = 0
                        disk_sector_size = disklabels[disk_path].partedDevice.sectorSize
                        for chunk in chunks:
                            chunk.growRequests()
                            # record the growth for this layout
                            new_growth += chunk.growth
                            disk_growth += chunk.growth
                            for req in chunk.requests:
                                ctx.logger.debug("request %d (%s) growth: %d (%dMB) "
                                          "size: %dMB" %
                                          (req.partition.id,
                                           req.partition.name,
                                           req.growth,
                                           sectorsToSize(req.growth,
                                                         disk_sector_size),
                                           sectorsToSize(req.growth + req.base,
                                                         disk_sector_size)))
                        ctx.logger.debug("disk %s growth: %d (%dMB)" %
                                        (disk_path, disk_growth,
                                         sectorsToSize(disk_growth,
                                                       disk_sector_size)))

                    disklabel.partedDisk.removePartition(temp_part)
                    _part.partedPartition = None
                    _part.disk = None

                    ctx.logger.debug("total growth: %d sectors" % new_growth)

                    # update the chosen free region unless the previous
                    # choice yielded greater total growth
                    if new_growth < growth:
                        ctx.logger.debug("keeping old free: %d < %d" % (new_growth,
                                                                 growth))
                        update = False
                    else:
                        growth = new_growth

                if update:
                    # now we know we are choosing a new free space,
                    # so update the disk and part type
                    ctx.logger.debug("updating use_disk to %s (%s), type: %s"
                                % (_disk, _disk.name, new_part_type))
                    part_type = new_part_type
                    use_disk = _disk
                    ctx.logger.debug("new free: %s (%d-%d / %dMB)" % (best,
                                                               best.start,
                                                               best.end,
                                                               best.getSize()))
                    ctx.logger.debug("new free allows for %d sectors of growth" %
                                growth)
                    free = best

            # For platforms with a fake boot partition (like Apple Bootstrap or
            # PReP) and multiple disks, we need to ensure the /boot partition
            # ends up on the same disk as the fake one.
            mountpoint = getattr(_part.format, "mountpoint", "")
            if not mountpoint:
                mountpoint = ""

            if free and (_part.req_bootable or mountpoint.startswith("/boot")):
                # if this is a bootable partition we want to
                # use the first freespace region large enough
                # to satisfy the request
                ctx.logger.debug("found free space for bootable request")
                break

        if free is None:
            raise PartitioningError(_("not enough free space on disks"))

        _disk = use_disk
        disklabel = _disk.format

        # create the extended partition if needed
        if part_type == parted.PARTITION_EXTENDED:
            ctx.logger.debug("creating extended partition")
            addPartition(disklabel, free, part_type, None)

            # now the extended partition exists, so set type to logical
            part_type = parted.PARTITION_LOGICAL

            # recalculate freespace
            ctx.logger.debug("recalculating free space")
            free = getBestFreeSpaceRegion(disklabel.partedDisk,
                                          part_type,
                                          _part.req_size,
                                          boot=_part.req_bootable,
                                          grow=_part.req_grow)
            if not free:
                raise PartitioningError(_("not enough free space after "
                                        "creating extended partition"))

        partition = addPartition(disklabel, free, part_type, _part.req_size)
        ctx.logger.debug("created partition %s of %dMB and added it to %s" %
                (partition.getDeviceNodeName(), partition.getSize(),
                 disklabel.device))

        # this one sets the name
        _part.partedPartition = partition
        _part.disk = _disk

        # parted modifies the partition in the process of adding it to
        # the disk, so we need to grab the latest version...
        _part.partedPartition = disklabel.partedDisk.getPartitionByPath(_part.path)

def growPartitions(disks, partitions, free):
    """ Grow all growable partition requests.

        Partitions have already been allocated from chunks of free space on
        the disks. This function does not modify the ordering of partitions
        or the free chunks from which they are allocated.

        Free space within a given chunk is allocated to each growable
        partition allocated from that chunk in an amount corresponding to
        the ratio of that partition's base size to the sum of the base sizes
        of all growable partitions allocated from the chunk.

        Arguments:

            disks -- a list of all usable disks (Disk instances)
            partitions -- a list of all partitions (Partition instances)
            free -- a list of all free regions (parted.Geometry instances)
    """
    ctx.logger.debug("growPartitions: disks=%s, partitions=%s" %
            ([d.name for d in disks],
             ["%s(id %d)" % (p.name, p.id) for p in partitions]))
    all_growable = [p for p in partitions if p.req_grow]
    if not all_growable:
        ctx.logger.debug("no growable partitions")
        return

    ctx.logger.debug("growable partitions are %s" % [p.name for p in all_growable])

    for disk in disks:
        ctx.logger.debug("growing partitions on %s" % disk.name)
        sector_size = disk.format.partedDevice.sectorSize

        # find any extended partition on this disk
        extended_geometry = getattr(disk.format.extendedPartition,
                                    "geometry",
                                    None)  # parted.Geometry

        # list of free space regions on this disk prior to partition allocation
        disk_free = [f for f in free if f.device.path == disk.path]
        if not disk_free:
            ctx.logger.debug("no free space on %s" % disk.name)
            continue

        chunks = getDiskChunks(disk, partitions, disk_free)
        ctx.logger.debug("disk %s has %d chunks" % (disk.name, len(chunks)))
        # grow the partitions in each chunk as a group
        for chunk in chunks:
            if not chunk.hasGrowable:
                # no growable partitions in this chunk
                continue

            chunk.growRequests()

            # recalculate partition geometries
            disklabel = disk.format
            start = chunk.geometry.start
            # align start sector as needed
            if not disklabel.alignment.isAligned(chunk.geometry, start):
                start = disklabel.alignment.alignUp(chunk.geometry, start)
            new_partitions = []
            for p in chunk.requests:
                ptype = p.partition.partedPartition.type
                ctx.logger.debug("partition %s (%d): %s" % (p.partition.name,
                                                     p.partition.id, ptype))
                if ptype == parted.PARTITION_EXTENDED:
                    continue

                # XXX since we need one metadata sector before each
                #     logical partition we burn one logical block to
                #     safely align the start of each logical partition
                if ptype == parted.PARTITION_LOGICAL:
                    start += disklabel.alignment.grainSize

                old_geometry = p.partition.partedPartition.geometry
                new_length = p.base + p.growth
                end = start + new_length - 1
                # align end sector as needed
                if not disklabel.endAlignment.isAligned(chunk.geometry, end):
                    end = disklabel.endAlignment.alignDown(chunk.geometry, end)
                new_geometry = parted.Geometry(device=disklabel.partedDevice,
                                               start=start,
                                               end=end)
                ctx.logger.debug("new geometry for %s: %s" % (p.partition.name,
                                                       new_geometry))
                start = end + 1
                new_partition = parted.Partition(disk=disklabel.partedDisk,
                                                 type=ptype,
                                                 geometry=new_geometry)
                new_partitions.append((new_partition, p.partition))

            # remove all new partitions from this chunk
            removeNewPartitions([disk], [r.partition for r in chunk.requests])
            ctx.logger.debug("back from removeNewPartitions")

            # adjust the extended partition as needed
            # we will ony resize an extended partition that we created
            ctx.logger.debug("extended: %s" % extended_geometry)
            if extended_geometry and \
               chunk.geometry.contains(extended_geometry):
                ctx.logger.debug("setting up new geometry for extended on %s" % disk.name)
                ext_start = 0
                ext_end = 0
                for (partition, device) in new_partitions:
                    if partition.type != parted.PARTITION_LOGICAL:
                        continue

                    if not ext_start or partition.geometry.start < ext_start:
                        # account for the logical block difference in start
                        # sector for the extended -v- first logical
                        # (partition.geometry.start is already aligned)
                        ext_start = partition.geometry.start - disklabel.alignment.grainSize

                    if not ext_end or partition.geometry.end > ext_end:
                        ext_end = partition.geometry.end

                new_geometry = parted.Geometry(device=disklabel.partedDevice,
                                               start=ext_start,
                                               end=ext_end)
                ctx.logger.debug("new geometry for extended: %s" % new_geometry)
                new_extended = parted.Partition(disk=disklabel.partedDisk,
                                                type=parted.PARTITION_EXTENDED,
                                                geometry=new_geometry)
                ptypes = [p.type for (p, d) in new_partitions]
                for pt_idx, ptype in enumerate(ptypes):
                    if ptype == parted.PARTITION_LOGICAL:
                        new_partitions.insert(pt_idx, (new_extended, None))
                        break

            # add the partitions with their new geometries to the disk
            for (partition, device) in new_partitions:
                if device:
                    name = device.name
                else:
                    # If there was no extended partition on this disk when
                    # doPartitioning was called we won't have a
                    # Partition instance for it.
                    name = partition.getDeviceNodeName()

                ctx.logger.debug("setting %s new geometry: %s" % (name,
                                                           partition.geometry))
                constraint = parted.Constraint(exactGeom=partition.geometry)
                disklabel.partedDisk.addPartition(partition=partition,
                                                  constraint=constraint)
                path = partition.path
                if device:
                    # set the device's name
                    device.partedPartition = partition
                    # without this, the path attr will be a basename. eek.
                    device.disk = disk

                    # make sure we store the disk's version of the partition
                    newpart = disklabel.partedDisk.getPartitionByPath(path)
                    device.partedPartition = newpart
def growLVM(storage):
    """ Grow LVs according to the sizes of the PVs. """
    for vg in storage.vgs:
        total_free = vg.freeSpace
        if total_free < 0:
            # by now we have allocated the PVs so if there isn't enough
            # space in the VG we have a real problem
            raise PartitioningError(_("not enough space for LVM requests"))
        elif not total_free:
            ctx.logger.debug("vg %s has no free space" % vg.name)
            continue

        ctx.logger.debug("vg %s: %dMB free ; lvs: %s" % (vg.name, vg.freeSpace,
                                                        [l.lvname for l in vg.lvs]))

        # figure out how much to grow each LV
        grow_amounts = {}
        lv_total = vg.size - total_free
        ctx.logger.debug("used: %dMB ; vg.size: %dMB" % (lv_total, vg.size))

        # This first loop is to calculate percentage-based growth
        # amounts. These are based on total free space.
        lvs = vg.lvs
        lvs.sort(cmp=logicalVolumeCompare)
        for lv in lvs:
            if not lv.req_grow or not lv.req_percent:
                continue

            portion = (lv.req_percent * 0.01)
            grow = portion * vg.vgFree
            new_size = lv.req_size + grow
            if lv.req_max_size and new_size > lv.req_max_size:
                grow -= (new_size - lv.req_max_size)

            if lv.format.maxSize and lv.format.maxSize < new_size:
                grow -= (new_size - lv.format.maxSize)

            # clamp growth amount to a multiple of vg extent size
            grow_amounts[lv.name] = vg.align(grow)
            total_free -= grow
            lv_total += grow

        # This second loop is to calculate non-percentage-based growth
        # amounts. These are based on free space remaining after
        # calculating percentage-based growth amounts.

        # keep a tab on space not allocated due to format or requested
        # maximums -- we'll dole it out to subsequent requests
        leftover = 0
        for lv in lvs:
            ctx.logger.debug("checking lv %s: req_grow: %s ; req_percent: %s"
                            % (lv.name, lv.req_grow, lv.req_percent))
            if not lv.req_grow or lv.req_percent:
                continue

            portion = float(lv.req_size) / float(lv_total)
            grow = portion * total_free
            ctx.logger.debug("grow is %dMB" % grow)

            todo = lvs[lvs.index(lv):]
            unallocated = reduce(lambda x,y: x+y,
                                 [l.req_size for l in todo
                                  if l.req_grow and not l.req_percent])
            extra_portion = float(lv.req_size) / float(unallocated)
            extra = extra_portion * leftover
            ctx.logger.debug("%s getting %dMB (%d%%) of %dMB leftover space"
                      % (lv.name, extra, extra_portion * 100, leftover))
            leftover -= extra
            grow += extra
            ctx.logger.debug("grow is now %dMB" % grow)
            max_size = lv.req_size + grow
            if lv.req_max_size and max_size > lv.req_max_size:
                max_size = lv.req_max_size

            if lv.format.maxSize and max_size > lv.format.maxSize:
                max_size = lv.format.maxSize

            ctx.logger.debug("max size is %dMB" % max_size)
            max_size = max_size
            leftover += (lv.req_size + grow) - max_size
            grow = max_size - lv.req_size
            ctx.logger.debug("lv %s gets %dMB" % (lv.name, vg.align(grow)))
            grow_amounts[lv.name] = vg.align(grow)

        if not grow_amounts:
            ctx.logger.debug("no growable lvs in vg %s" % vg.name)
            continue

        # now grow the lvs by the amounts we've calculated above
        for lv in lvs:
            if lv.name not in grow_amounts.keys():
                continue
            lv.size += grow_amounts[lv.name]

        # now there shouldn't be any free space left, but if there is we
        # should allocate it to one of the LVs
        vg_free = vg.freeSpace
        ctx.logger.debug("vg %s has %dMB free" % (vg.name, vg_free))
        if vg_free:
            for lv in lvs:
                if not lv.req_grow:
                    continue

                if lv.req_max_size and lv.size == lv.req_max_size:
                    continue

                if lv.format.maxSize and lv.size == lv.format.maxSize:
                    continue

                # first come, first served
                projected = lv.size + vg.freeSpace
                if lv.req_max_size and projected > lv.req_max_size:
                    projected = lv.req_max_size

                if lv.format.maxSize and projected > lv.format.maxSize:
                    projected = lv.format.maxSize

                ctx.logger.debug("giving leftover %dMB to %s" % (projected - lv.size,
                                                                lv.name))
                lv.size = projected

def getDiskChunks(disk, partitions, free):
    """ Return a list of Chunk instances representing a disk.

        Arguments:

            disk -- a Device with a DiskLabel format
            partitions -- list of Partition instances
            free -- list of parted.Geometry instances representing free space

        Partitions and free regions not on the specified disk are ignored.

    """
    # list of all new partitions on this disk
    disk_parts = [p for p in partitions if p.disk == disk and not p.exists]
    disk_free = [f for f in free if f.device.path == disk.path]


    chunks = [Chunk(f) for f in disk_free]

    for p in disk_parts:
        if p.isExtended:
            # handle extended partitions specially since they are
            # indeed very special
            continue

        for i, f in enumerate(disk_free):
            if f.contains(p.partedPartition.geometry):
                chunks[i].addRequest(Request(p))
                break

    return chunks

def hasFreeDiskSpace(storage, exclusiveDisks=None):
    """Returns True if there is at least 100Mb of free usable space in any of
       the disks.  False otherwise.

    """
    freeSpaces = False

    disks = storage.partitioned
    # also include unpartitioned disks that aren't mpath or biosraid
    whole = filter(lambda d: not d.partitioned and not d.format.hidden, storage.disks)
    disks.extend(whole)
    disks.sort(key=lambda d: d.name)
    for disk in disks:
        for partition in disk.format.freePartitions:
            if partition.getSize(unit="MB") > 1:
                freeSpaces = True
                break

    return freeSpaces

def shouldClear(device, clearPartType, clearPartDisks=None):
    if clearPartType not in [CLEARPART_TYPE_LINUX, CLEARPART_TYPE_ALL]:
        return False

    if isinstance(device, Partition):
        # Never clear the special first partition on a Mac disk label, as that
        # holds the partition table itself.
        if device.disk.format.partedDisk.type == "mac" and \
           device.partedPartition.number == 1 and \
           device.partedPartition.name == "Apple":
            return False

        # If we got a list of disks to clear, make sure this one's on it
        if clearPartDisks and device.disk.name not in clearPartDisks:
            return False

        # We don't want to fool with extended partitions, freespace, &c
        if device.partType not in [parted.PARTITION_NORMAL,
                                   parted.PARTITION_LOGICAL]:
            return False

        if clearPartType == CLEARPART_TYPE_LINUX and \
           not device.format.linuxNative and \
           not device.getFlag(parted.PARTITION_LVM) and \
           not device.getFlag(parted.PARTITION_RAID) and \
           not device.getFlag(parted.PARTITION_SWAP):
            return False
    elif device.isDisk and not device.partitioned:
        # If we got a list of disks to clear, make sure this one's on it
        if clearPartDisks and device.name not in clearPartDisks:
            return False

        # Never clear disks with hidden formats
        if device.format.hidden:
            return False

        if clearPartType == CLEARPART_TYPE_LINUX and \
           not device.format.linuxNative:
            return False

    # Don't clear devices holding install media.
    if device.protected:
        return False

    # Don't clear immutable devices.
    if device.immutable:
        return False

    return True

def logicalVolumeCompare(lv1, lv2):
    """ More specifically defined lvs come first.

        < 1 => x < y
          0 => x == y
        > 1 => x > y
    """
    ret = 0

    # larger requests go to the front of the list
    ret -= cmp(lv1.size, lv2.size) * 100

    # fixed size requests to the front
    ret += cmp(lv1.req_grow, lv2.req_grow) * 50

    # potentially larger growable requests go to the front
    if lv1.req_grow and lv2.req_grow:
        if not lv1.req_max_size and lv2.req_max_size:
            ret -= 25
        elif lv1.req_max_size and not lv2.req_max_size:
            ret += 25
        else:
            ret -= cmp(lv1.req_max_size, lv2.req_max_size) * 25

    if ret > 0:
        ret = 1
    elif ret < 0:
        ret = -1

    return ret

def weight(fstype=None, mountpoint=None):
    """ Given an fstype (as a string) or a mountpoint, return an integer
        for the base sorting weight.  This is used to modify the sort
        algorithm for partition requests, mainly to make sure bootable
        partitions and /boot are placed where they need to be."""
    if fstype and fstype == "efi" or mountpoint and mountpoint == "/boot/efi":
        return 5000
    elif mountpoint and mountpoint == "/boot":
        return 2000
    else:
        return 0

def defaultPartitioning(storage, quiet=0, asVol=True):
    """Return the default partitioning information."""
    autorequests = [PartitionSpec(mountpoint="/", fstype=storage.defaultFSType,
                                  size=1024, maxSize=50*1024,
                                  grow=True, asVol=asVol),
                    PartitionSpec(mountpoint="/home", fstype=storage.defaultFSType,
                                  size=100, grow=True,
                                  asVol=asVol, requiredSpace=50*1024)]

    bootreq = PartitionSpec(mountpoint="/boot", fstype=storage.defaultFSType,
                            size=500, weight=weight(mountpoint="/boot"))
    autorequests.append(bootreq)

    (minswap, maxswap) = yali.util.swap_suggestion(quiet=quiet)
    swapreq = PartitionSpec(fstype="swap", size=minswap, maxSize=maxswap, grow=True, asVol=asVol)
    autorequests.append(swapreq)

    return autorequests

def _createFreeSpacePartitions(storage):
    # get a list of disks that have at least one free space region of at
    # least the default size for new partitions
    disks = []
    for disk in storage.partitioned:
        if storage.clearPartDisks and \
           (disk.name not in storage.clearPartDisks):
            continue

        part = disk.format.firstPartition
        while part:
            if not part.type & parted.PARTITION_FREESPACE:
                part = part.nextPartition()
                continue

            if part.getSize(unit="MB") > Partition.defaultSize:
                disks.append(disk)
                break

            part = part.nextPartition()

    devs = []
    if ctx.flags.partitioning_lvm:
        # create a separate pv partition for each disk with free space
        for disk in disks:
            fmt_type = "lvmpv"
            fmt_args = {}
            part = storage.newPartition(fmt_type=fmt_type,
                                        fmt_args=fmt_args,
                                        grow=True,
                                        disks=[disk])
            storage.createDevice(part)
            devs.append(part)

    return (disks, devs)

def _schedulePartitions(storage, disks):
    #
    # Convert storage.autoPartitionRequests into Device instances and
    # schedule them for creation
    #
    # First pass is for partitions only. We'll do LVs later.
    #
    for request in storage.autoPartitionRequests:
        if request.asVol:
            continue

        if request.fstype is None:
            request.fstype = storage.defaultFSType
        elif request.fstype == "prepboot" and storage.bootDevice():
            # there should never be a need for more than one PReP partition
            continue

        dev = storage.newPartition(fmt_type=request.fstype,
                                   size=request.size,
                                   grow=request.grow,
                                   maxsize=request.maxSize,
                                   mountpoint=request.mountpoint,
                                   disks=disks,
                                   weight=request.weight)

        # schedule the device for creation
        storage.createDevice(dev)

    # make sure preexisting broken lvm/raid configs get out of the way
    return

def _scheduleLogicalVolumes(storage, devices):
    pvs = devices
    # create a vg containing all of the autopart pvs
    vg = storage.newVolumeGroup(pvs=pvs)
    storage.createDevice(vg)

    initialVGSize = vg.size

    #
    # Convert storage.autoPartitionRequests into Device instances and
    # schedule them for creation.
    #
    # Second pass, for LVs only.
    for request in storage.autoPartitionRequests:
        if not request.asVol:
            continue

        if request.requiredSpace and request.requiredSpace > initialVGSize:
            continue

        if request.fstype is None:
            request.fstype = storage.defaultFSType

        # FIXME: move this to a function and handle exceptions
        device = storage.newLogicalVolume(vg=vg, fmt_type=request.fstype,
                                          mountpoint=request.mountpoint,
                                          grow=request.grow,
                                          maxsize=request.maxSize,
                                          size=request.size)

        # schedule the device for creation
        storage.createDevice(device)

def doAutoPartition(storage):
    ctx.logger.debug("doAutoPartition")
    ctx.logger.debug("doAutoPart: %s" % storage.doAutoPart)
    ctx.logger.debug("clearPartType: %s" % storage.clearPartType)
    ctx.logger.debug("clearPartDisks: %s" % storage.clearPartDisks)
    ctx.logger.debug("storage.disks: %s" % [d.name for d in storage.disks])
    ctx.logger.debug("storage.partitioned: %s" % [d.name for d in storage.partitioned])
    ctx.logger.debug("all names: %s" % [d.name for d in storage.devices])

    disks = []
    devs = []

    if storage.doAutoPart:
        clearPartitions(storage)

    if storage.doAutoPart:
        (disks, devs) = _createFreeSpacePartitions(storage)

        if disks == []:
            msg = _("Could not find enough free space for automatic\n"
                    "partitioning, please use another partitioning method.")

            ctx.interface.messageWindow(_("Error Partitioning"), msg, type='error')

            storage.reset()
            return False

        _schedulePartitions(storage, disks)

    # sanity check the individual devices
    #ctx.logger.warning("not sanity checking devices because I don't know how yet")

    # run the autopart function to allocate and grow partitions
    try:
        doPartitioning(storage, exclusiveDisks=storage.clearPartDisks)

        if storage.doAutoPart and ctx.flags.partitioning_lvm:
            _scheduleLogicalVolumes(storage, devs)

        # grow LVs
        growLVM(storage)

    except PartitioningWarning as msg:
        ctx.interface.messageWindow(_("Warnings During Automatic Partitioning"),
                                    _("Following warnings occurred during automatic "
                                      "partitioning:\n\n%s") % msg,
                                    type='warning')
        ctx.logger.warning(msg)
        return False

    except PartitioningError as msg:
        # restore drives to original state
        storage.reset()
        extra = _("\n\nPress 'OK' to exit the installer.")
        ctx.interface.messageWindow(_("Error Partitioning"),
                                    _("Could not allocate requested partitions: \n"
                                      "%(msg)s.%(extra)s") %
                                    {'msg': msg, 'extra': extra},
                                    type='error')
        ctx.logger.warning(msg)
        return None

    else:
        # sanity check the collection of devices
        #ctx.logger.warning("not sanity checking storage config because I don't know how yet")
        # now do a full check of the requests
        (errors, warnings) = storage.sanityCheck()
        if warnings:
            for warning in warnings:
                ctx.logger.warning(warning)

        if errors:
            errortxt = "\n".join(errors)
            extra = _("\n\nPress 'OK' to exit the installer.")
            ctx.interface.messageWindow(_("Automatic Partitioning Errors"),
                                        _("The following errors occurred with your "
                                          "partitioning:\n\n%(errortxt)s\n\n"
                                          "This can happen if there is not enough "
                                          "space on your hard drive(s) for the "
                                          "installation. %(extra)s") %
                                        {'errortxt': errortxt, 'extra': extra},
                                        type='error')

            storage.reset()
            return None

        return True
