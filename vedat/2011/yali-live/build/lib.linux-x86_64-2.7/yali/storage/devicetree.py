#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import block
import parted
import gettext
_ = gettext.translation('yali', fallback=True).ugettext

import yali.context as ctx
from yali.storage import StorageError
from yali.storage.udev import *
from yali.storage.storageBackendHelpers import questionInitializeDisk, questionReinitInconsistentLVM, questionUnusedRaidMembers
from yali.storage.operations import operation_type_from_string, operation_object_from_string, OperationDestroyDevice, OperationCreateDevice, OperationDestroyFormat, OperationCreateFormat
from yali.storage.library import lvm
from yali.storage.library import raid
from yali.storage.library import devicemapper
from yali.storage.partitioning import shouldClear, CLEARPART_TYPE_ALL, CLEARPART_TYPE_LINUX, CLEARPART_TYPE_NONE
from yali.storage.devices.device import DeviceError, DeviceNotFoundError, deviceNameToDiskByPath, devicePathToName
from yali.storage.devices.nodevice import NoDevice
from yali.storage.devices.devicemapper import DeviceMapper
from yali.storage.devices.volumegroup import VolumeGroup
from yali.storage.devices.dmraidarray import DMRaidArray
from yali.storage.devices.raidarray import RaidArray
from yali.storage.devices.logicalvolume import LogicalVolume
from yali.storage.devices.disk import Disk
from yali.storage.devices.opticaldevice import OpticalDevice
from yali.storage.devices.partition import Partition
from yali.storage import formats
from yali.storage.formats.disklabel import InvalidDiskLabelError, DiskLabelCommitError
from yali.storage.formats.filesystem import FilesystemError
from yali.storage.formats.raidmember import RaidMember

class DeviceTreeError(StorageError):
    pass

class DeviceTree(object):
    def __init__(self, intf=None, ignored=[], exclusive=[], type=CLEARPART_TYPE_NONE,
                 clear=[],zeroMbr=None, reinitializeDisks=None, protected=[]):

        self.intf = intf
        self._devices = []
        self.operations = []
        self.exclusiveDisks = exclusive
        self.clearPartType = type
        self.clearPartDisks = clear
        self.zeroMbr = zeroMbr
        self.reinitializeDisks = reinitializeDisks

        # protected device specs as provided by the user
        self.protectedDevSpecs = protected

        # names of protected devices at the time of tree population
        self.protectedDeviceNames = []
        self.unusedRaidMembers = []

        self._ignoredDisks = []
        for disk in ignored:
            self.addIgnoredDisk(disk)
        lvm.lvm_cc_resetFilter()

        self._populated = False

    def addIgnoredDisk(self, disk):
        self._ignoredDisks.append(disk)
        lvm.lvm_cc_addFilterRejectRegexp(disk)

    def isIgnored(self, info):
        sysfs_path = udev_device_get_sysfs_path(info)
        name = udev_device_get_name(info)
        if not sysfs_path:
            return None

        if name in self._ignoredDisks:
            return True

        # Special handling for mdraid external metadata sets (mdraid BIOSRAID):
        # 1) The containers are intermediate devices which will never be
        # in exclusiveDisks
        # 2) Sets get added to exclusive disks with their dmraid set name by
        # the filter ui.  Note that making the ui use md names instead is not
        # possible as the md names are simpy md# and we cannot predict the #
        if udev_device_get_md_level(info) == "container":
            return False

        if udev_device_get_md_container(info) and \
               udev_device_get_md_name(info):
            md_name = udev_device_get_md_name(info)
            for i in range(0, len(self.exclusiveDisks)):
                if re.match("isw_[a-z]*_%s" % md_name, self.exclusiveDisks[i]):
                    self.exclusiveDisks[i] = name
                    return False

        if udev_device_is_disk(info) and \
           not udev_device_is_dmraid_partition(info) and \
           not udev_device_is_multipath_partition(info) and \
           not udev_device_is_dm_lvm(info) and \
           not udev_device_is_dm_crypt(info) and \
           not (udev_device_is_md(info) and
                not udev_device_get_md_container(info)):
            if self.exclusiveDisks and name not in self.exclusiveDisks:
                self.addIgnoredDisk(name)
                return True

        # Ignore loop and ram devices, we normally already skip these in
        # udev.py: enumerate_block_devices(), but we can still end up trying
        # to add them to the tree when they are slaves of other devices, this
        # happens for example with the livecd
        if name.startswith("loop") or name.startswith("ram"):
            return True

    def _addDevice(self, device):
        """ Add a device to the tree.

            Raise ValueError if the device's identifier is already in the list.
        """
        if device.path in [d.path for d in self._devices] and \
           not isinstance(device, NoDevice):
            raise ValueError("device is already in tree")

        # make sure this device's parent devices are in the tree already
        for parent in device.parents:
            if parent not in self._devices:
                raise DeviceTreeError("parent device not in tree")

        self._devices.append(device)
        ctx.logger.debug("added %s %s (id %d) to device tree" % (device.type, device.name, device.id))

    def _removeDevice(self, device, force=None, moddisk=True):
        """ Remove a device from the tree.

            Only leaves may be removed.
        """
        if device not in self._devices:
            raise ValueError("Device '%s' not in tree" % device.name)

        if not device.isleaf and not force:
            ctx.logger.debug("%s has %d kids" % (device.name, device.kids))
            raise ValueError("Cannot remove non-leaf device '%s'" % device.name)

        # if this is a partition we need to remove it from the parted.Disk
        if moddisk and isinstance(device, Partition) and device.disk is not None:
            # if this partition hasn't been allocated it could not have
            # a disk attribute
            if device.partedPartition.type == parted.PARTITION_EXTENDED and \
                    len(device.disk.format.logicalPartitions) > 0:
                raise ValueError("Cannot remove extended partition %s.  "
                                 "Logical partitions present." % device.name)

            device.disk.format.removePartition(device.partedPartition)

            # adjust all other Partition instances belonging to the
            # same disk so the device name matches the potentially altered
            # name of the parted.Partition
            for dev in self._devices:
                if isinstance(dev, Partition) and dev.disk == device.disk:
                    dev.updateName()

        self._devices.remove(device)
        ctx.logger.debug("removed %s %s (id %d) from device tree" % (device.type,
                                                                     device.name,
                                                                     device.id))

        for parent in device.parents:
            parent.removeChild()

    def addOperation(self, operation):
        """ Register an operation to be performed at a later time.

        """
        if (operation.isDestroy() or operation.isResize() or \
            (operation.isCreate() and operation.isFormat())) and \
           operation.device not in self._devices:
            raise DeviceTreeError("device is not in the tree")
        elif (operation.isCreate() and operation.isDevice()):
            if operation.device in self._devices:
                self._removeDevice(operation.device)
            for d in self._devices:
                if d.path == operation.device.path:
                    self._removeDevice(d)

        if operation.isCreate() and operation.isDevice():
            self._addDevice(operation.device)
        elif operation.isDestroy() and operation.isDevice():
            self._removeDevice(operation.device)
        elif operation.isCreate() and operation.isFormat():
            if isinstance(operation.device.format, formats.filesystem.Filesystem) and \
               operation.device.format.mountpoint in self.filesystems:
                raise DeviceTreeError("mountpoint already in use")

        ctx.logger.debug("registered operation: %s" % operation)
        self.operations.append(operation)

    def removeOperation(self, operation):
        """ Cancel a registered operation.

        """
        if operation.isCreate() and operation.isDevice():
            # remove the device from the tree
            self._removeDevice(operation.device)
        elif operation.isDestroy() and operation.isDevice():
            # add the device back into the tree
            self._addDevice(operation.device)
        elif operation.isFormat() and \
             (operation.isCreate() or operation.isMigrate() or operation.isResize()):
            operation.cancel()

        self.operations.remove(operation)

    def findOperations(self, device=None, type=None, object=None, path=None, devid=None):
        """ Find all operations that match all specified parameters.

            Keyword arguments:

                device -- device to match (Device, or None to match any)
                type -- operation type to match (string, or None to match any)
                object -- operand type to match (string, or None to match any)
                path -- device path to match (string, or None to match any)

        """
        if device is None and type is None and object is None and \
           path is None and devid is None:
            return self.operations[:]

        # convert the string arguments to the types used in operations
        _type = operation_type_from_string(type)
        _object = operation_object_from_string(object)

        operations = []
        for operation in self.operations:
            if device is not None and operation.device != device:
                continue

            if _type is not None and operation.type != _type:
                continue

            if _object is not None and operation.obj != _object:
                continue

            if path is not None and operation.device.path != path:
                continue

            if devid is not None and operation.device.id != devid:
                continue

            operations.append(operation)

        return operations

    def processOperations(self, dryRun=None):
        def cmpOperations(a1, a2):
            ret = 0
            if a1.isDestroy() and a2.isDestroy():
                if a1.device.path == a2.device.path:
                    # if it's the same device, destroy the format first
                    if a1.isFormat() and a2.isFormat():
                        ret = 0
                    elif a1.isFormat() and not a2.isFormat():
                        ret = -1
                    elif not a1.isFormat() and a2.isFormat():
                        ret = 1
                elif a1.device.dependsOn(a2.device):
                    ret = -1
                elif a2.device.dependsOn(a1.device):
                    ret = 1
                # generally destroy partitions after lvs, vgs, &c
                elif isinstance(a1.device, Partition) and \
                     isinstance(a2.device, Partition):
                    if a1.device.disk == a2.device.disk:
                        ret = cmp(a2.device.partedPartition.number,
                                  a1.device.partedPartition.number)
                    else:
                        ret = cmp(a2.device.name, a1.device.name)
                elif isinstance(a1.device, Partition) and \
                     a2.device.partitioned:
                    ret = -1
                elif isinstance(a2.device, Partition) and \
                     a1.device.partitioned:
                    ret = 1
                # remove partitions before unpartitioned non-partition
                # devices
                elif isinstance(a1.device, Partition) and \
                     not isinstance(a2.device, Partition):
                    ret = 1
                elif isinstance(a2.device, Partition) and \
                     not isinstance(a1.device, Partition):
                    ret = -1
                else:
                    ret = 0
            elif a1.isDestroy():
                ret = -1
            elif a2.isDestroy():
                ret = 1
            elif a1.isResize() and a2.isResize():
                if a1.device.path == a2.device.path:
                    if a1.obj == a2.obj:
                        ret = 0
                    elif a1.isFormat() and not a2.isFormat():
                        # same path, one device, one format
                        if a1.isGrow():
                            ret = 1
                        else:
                            ret = -1
                    elif not a1.isFormat() and a2.isFormat():
                        # same path, one device, one format
                        if a1.isGrow():
                            ret = -1
                        else:
                            ret = 1
                    else:
                        ret = cmp(a1.device.name, a2.device.name)
                elif a1.device.dependsOn(a2.device):
                    if a1.isGrow():
                        ret = 1
                    else:
                        ret = -1
                elif a2.device.dependsOn(a1.device):
                    if a1.isGrow():
                        ret = -1
                    else:
                        ret = 1
                elif isinstance(a1.device, Partition) and \
                     isinstance(a2.device, Partition):
                    ret = cmp(a1.device.name, a2.device.name)
                else:
                    ret = 0
            elif a1.isResize():
                ret = -1
            elif a2.isResize():
                ret = 1
            elif a1.isCreate() and a2.isCreate():
                if a1.device.path == a2.device.path:
                    if a1.obj == a2.obj:
                        ret = 0
                    if a1.isFormat():
                        ret = 1
                    elif a2.isFormat():
                        ret = -1
                    else:
                        ret = 0
                elif a1.device.dependsOn(a2.device):
                    ret = 1
                elif a2.device.dependsOn(a1.device):
                    ret = -1
                # generally create partitions before other device types
                elif isinstance(a1.device, Partition) and \
                     isinstance(a2.device, Partition):
                    if a1.device.disk == a2.device.disk:
                        ret = cmp(a1.device.partedPartition.number,
                                  a2.device.partedPartition.number)
                    else:
                        ret = cmp(a1.device.name, a2.device.name)
                elif isinstance(a1.device, Partition) and \
                     a2.device.partitioned:
                    ret = 1
                elif isinstance(a2.device, Partition) and \
                     a1.device.partitioned:
                    ret = -1
                elif isinstance(a1.device, Partition) and \
                     not isinstance(a2.device, Partition):
                    ret = -1
                elif isinstance(a2.device, Partition) and \
                     not isinstance(a1.device, Partition):
                    ret = 1
                else:
                    ret = 0
            elif a1.isCreate():
                ret = -1
            elif a2.isCreate():
                ret = 1
            elif a1.isMigrate() and a2.isMigrate():
                if a1.device.path == a2.device.path:
                    ret = 0
                elif a1.device.dependsOn(a2.device):
                    ret = 1
                elif a2.device.dependsOn(a1.device):
                    ret = -1
                elif isinstance(a1.device, Partition) and \
                     isinstance(a2.device, Partition):
                    if a1.device.disk == a2.device.disk:
                        ret = cmp(a1.device.partedPartition.number,
                                  a2.device.partedPartition.number)
                    else:
                        ret = cmp(a1.device.name, a2.device.name)
                else:
                    ret = 0
            else:
                ret = 0

            ctx.logger.debug("cmp: %d -- %s | %s" % (ret, a1, a2))
            return ret

        ctx.logger.debug("resetting parted disks...")
        for device in self.devices:
            if device.partitioned:
                device.format.resetPartedDisk()
                if device.originalFormat.type == "disklabel" and \
                   device.originalFormat != device.format:
                    device.originalFormat.resetPartedDisk()
        ctx.logger.debug("resetting parted disks...")
        for device in self.devices:
            if device.partitioned:
                device.format.resetPartedDisk()
                if device.originalFormat.type == "disklabel" and \
                   device.originalFormat != device.format:
                    device.originalFormat.resetPartedDisk()

        # Call preCommitFixup on all devices
        mpoints = [getattr(d.format, 'mountpoint', "") for d in self.devices]
        for device in self.devices:
            device.preCommitFixup(mountpoints=mpoints)

        # Also call preCommitFixup on any devices we're going to
        # destroy (these are already removed from the tree)
        for operation in self.operations:
            if isinstance(operation, OperationDestroyDevice):
                operation.device.preCommitFixup(mountpoints=mpoints)

        # setup operations to create any extended partitions we added
        #
        # XXX At this point there can be duplicate partition paths in the
        #     tree (eg: non-existent sda6 and previous sda6 that will become
        #     sda5 in the course of partitioning), so we access the list
        #     directly here.
        for device in self._devices:
            if isinstance(device, Partition) and \
               device.isExtended and not device.exists:
                # don't properly register the operation since the device is
                # already in the tree
                self.operations.append(OperationCreateDevice(device))

        for operation in self.operations:
            ctx.logger.debug("operation: %s" % operation)

        ctx.logger.debug("pruning operation queue...")
        self.pruneOperations()
        for operation in self.operations:
            ctx.logger.debug("operation: %s" % operation)

        ctx.logger.debug("sorting operations...")
        self.operations.sort(cmp=cmpOperations)
        for operation in self.operations:
            ctx.logger.debug("operation: %s" % operation)

        for operation in self.operations:
            ctx.logger.info("executing operation: %s" % operation)
            if not dryRun:
                try:
                    operation.execute(intf=self.intf)
                except DiskLabelCommitError:
                    # it's likely that a previous format destroy operation
                    # triggered setup of an lvm or md device.
                    self.teardownAll()
                    operation.execute(intf=self.intf)

                else:
                    udev_settle()
                    for device in self._devices:
                        # make sure we catch any renumbering parted does
                        if device.exists and isinstance(device, Partition):
                            device.updateName()
                            device.format.device = device.path

    def pruneOperations(self):
        """ Prune loops and redundant operations from the queue. """
        # handle device destroy operations
        operations = self.findOperations(type="destroy", object="device")
        for a in operations:
            if a not in self.operations:
                # we may have removed some of the operations in a previous
                # iteration of this loop
                continue

            ctx.logger.debug("operation '%s' (%s)" % (a, id(a)))
            destroys = self.findOperations(devid=a.device.id,
                                        type="destroy",
                                        object="device")

            creates = self.findOperations(devid=a.device.id,
                                       type="create",
                                       object="device")
            ctx.logger.debug("found %d create and %d destroy operations for device id %d"
                        % (len(creates), len(destroys), a.device.id))

            # If the device is not preexisting, we remove all operations up
            # to and including the last destroy operation.
            # If the device is preexisting, we remove all operations from
            # after the first destroy operation up to and including the last
            # destroy operation.
            # If the device is preexisting and there is only one device
            # destroy operation we remove all resize and format create/migrate
            # operations on that device that precede the destroy operation.
            loops = []
            first_destroy_idx = None
            first_create_idx = None
            stop_operation = None
            start = None
            if len(destroys) > 1:
                # there are multiple destroy operations for this device
                loops = destroys
                first_destroy_idx = self.operations.index(loops[0])
                start = self.operations.index(a) + 1
                stop_operation = destroys[-1]

            if creates:
                first_create_idx = self.operations.index(creates[0])
                if not loops or first_destroy_idx > first_create_idx:
                    # this device is not preexisting
                    start = first_create_idx
                    stop_operation = destroys[-1]

            dev_operations = self.findOperations(devid=a.device.id)
            if start is None:
                # only one device destroy, so prune preceding resizes and
                # format creates and migrates
                for _a in dev_operations[:]:
                    if _a.isResize() or (_a.isFormat() and not _a.isDestroy()):
                        continue

                    dev_operations.remove(_a)

                if not dev_operations:
                    # nothing to prune
                    continue

                start = self.operations.index(dev_operations[0])
                stop_operation = dev_operations[-1]

            # now we remove all operations on this device between the start
            # index (into self.operations) and stop_operation.
            for rem in dev_operations:
                end = self.operations.index(stop_operation)
                if start <= self.operations.index(rem) <= end:
                    ctx.logger.debug(" removing operation '%s' (%s)" % (rem, id(rem)))
                    self.operations.remove(rem)

                if rem == stop_operation:
                    break

        # device create operations
        operations = self.findOperations(type="create", object="device")
        for a in operations:
            if a not in self.operations:
                # we may have removed some of the operations in a previous
                # iteration of this loop
                continue

            ctx.logger.debug("operation '%s' (%s)" % (a, id(a)))
            creates = self.findOperations(devid=a.device.id,
                                       type="create",
                                       object="device")

            destroys = self.findOperations(devid=a.device.id,
                                        type="destroy",
                                        object="device")

            # If the device is preexisting, we remove everything between
            # the first destroy and the last create.
            # If the device is not preexisting, we remove everything up to
            # the last create.
            loops = []
            first_destroy_idx = None
            first_create_idx = None
            stop_operation = None
            start = None
            if len(creates) > 1:
                # there are multiple create operations for this device
                loops = creates
                first_create_idx = self.operations.index(loops[0])
                start = 0
                stop_operation = creates[-1]

            if destroys:
                first_destroy_idx = self.operations.index(destroys[0])
                if not loops or first_create_idx > first_destroy_idx:
                    # this device is preexisting
                    start = first_destroy_idx + 1
                    stop_operation = creates[-1]

            if start is None:
                continue

            # remove all operations on this from after the first destroy up
            # to the last create
            dev_operations = self.findOperations(devid=a.device.id)
            for rem in dev_operations:
                if rem == stop_operation:
                    break

                end = self.operations.index(stop_operation)
                if start <= self.operations.index(rem) < end:
                    ctx.logger.debug(" removing operation '%s' (%s)" % (rem, id(rem)))
                    self.operations.remove(rem)

        # device resize operations
        operations = self.findOperations(type="resize", object="device")
        for a in operations:
            if a not in self.operations:
                # we may have removed some of the operations in a previous
                # iteration of this loop
                continue

            ctx.logger.debug("operation '%s' (%s)" % (a, id(a)))
            loops = self.findOperations(devid=a.device.id,
                                     type="resize",
                                     object="device")

            if len(loops) == 1:
                continue

            # remove all but the last resize operation on this device
            for rem in loops[:-1]:
                ctx.logger.debug(" removing operation '%s' (%s)" % (rem, id(rem)))
                self.operations.remove(rem)

        # format destroy
        # XXX I don't think there's a way for these loops to happen
        operations = self.findOperations(type="destroy", object="format")
        for a in operations:
            if a not in self.operations:
                # we may have removed some of the operations in a previous
                # iteration of this loop
                continue

            ctx.logger.debug("operation '%s' (%s)" % (a, id(a)))
            destroys = self.findOperations(devid=a.device.id,
                                        type="destroy",
                                        object="format")

            creates = self.findOperations(devid=a.device.id,
                                       type="create",
                                       object="format")

            # If the format is not preexisting, we remove all operations up
            # to and including the last destroy operation.
            # If the format is preexisting, we remove all operations from
            # after the first destroy operation up to and including the last
            # destroy operation.
            loops = []
            first_destroy_idx = None
            first_create_idx = None
            stop_operation = None
            start = None
            if len(destroys) > 1:
                # there are multiple destroy operations for this format
                loops = destroys
                first_destroy_idx = self.operations.index(loops[0])
                start = self.operations.index(a) + 1
                stop_operation = destroys[-1]

            if creates:
                first_create_idx = self.operations.index(creates[0])
                if not loops or first_destroy_idx > first_create_idx:
                    # this format is not preexisting
                    start = first_create_idx
                    stop_operation = destroys[-1]

            if start is None:
                continue

            # now we remove all operations on this device's format between
            # the start index (into self.operations) and stop_operation.
            dev_operations = self.findOperations(devid=a.device.id,
                                           object="format")
            for rem in dev_operations:
                end = self.operations.index(stop_operation)
                if start <= self.operations.index(rem) <= end:
                    ctx.logger.debug(" removing operation '%s' (%s)" % (rem, id(rem)))
                    self.operations.remove(rem)

                if rem == stop_operation:
                    break

        # format create
        # XXX I don't think there's a way for these loops to happen
        operations = self.findOperations(type="create", object="format")
        for a in operations:
            if a not in self.operations:
                # we may have removed some of the operations in a previous
                # iteration of this loop
                continue

            ctx.logger.debug("operation '%s' (%s)" % (a, id(a)))
            creates = self.findOperations(devid=a.device.id,
                                       type="create",
                                       object="format")

            destroys = self.findOperations(devid=a.device.id,
                                        type="destroy",
                                        object="format")

            # If the format is preexisting, we remove everything between
            # the first destroy and the last create.
            # If the format is not preexisting, we remove everything up to
            # the last create.
            loops = []
            first_destroy_idx = None
            first_create_idx = None
            stop_operation = None
            start = None
            if len(creates) > 1:
                # there are multiple create operations for this format
                loops = creates
                first_create_idx = self.operations.index(loops[0])
                start = 0
                stop_operation = creates[-1]

            if destroys:
                first_destroy_idx = self.operations.index(destroys[0])
                if not loops or first_create_idx > first_destroy_idx:
                    # this format is preexisting
                    start = first_destroy_idx + 1
                    stop_operation = creates[-1]

            if start is None:
                continue

            # remove all operations on this from after the first destroy up
            # to the last create
            dev_operations = self.findOperations(devid=a.device.id,
                                           object="format")
            for rem in dev_operations:
                if rem == stop_operation:
                    break

                end = self.operations.index(stop_operation)
                if start <= self.operations.index(rem) < end:
                    ctx.logger.debug(" removing operation '%s' (%s)" % (rem, id(rem)))
                    self.operations.remove(rem)

        # format resize
        operations = self.findOperations(type="resize", object="format")
        for a in operations:
            if a not in self.operations:
                # we may have removed some of the operations in a previous
                # iteration of this loop
                continue

            ctx.logger.debug("operation '%s' (%s)" % (a, id(a)))
            loops = self.findOperations(devid=a.device.id,
                                     type="resize",
                                     object="format")

            if len(loops) == 1:
                continue

            # remove all but the last resize operation on this format
            for rem in loops[:-1]:
                ctx.logger.debug(" removing operation '%s' (%s)" % (rem, id(rem)))
                self.operations.remove(rem)

        # format migrate
        # XXX I don't think there's away for these loops to occur
        operations = self.findOperations(type="migrate", object="format")
        for a in operations:
            if a not in self.operations:
                # we may have removed some of the operations in a previous
                # iteration of this loop
                continue

            ctx.logger.debug("operation '%s' (%s)" % (a, id(a)))
            loops = self.findOperations(devid=a.device.id,
                                     type="migrate",
                                     object="format")

            if len(loops) == 1:
                continue

            # remove all but the last migrate operation on this format
            for rem in loops[:-1]:
                ctx.logger.debug(" removing operation '%s' (%s)" % (rem, id(rem)))
                self.operations.remove(rem)

    def addRaidArray(self, info):
        name = udev_device_get_name(info)
        uuid = udev_device_get_uuid(info)
        sysfs_path = udev_device_get_sysfs_path(info)
        device = None
        slaves = []
        dir = os.path.normpath("/sys/%s/slaves" % sysfs_path)
        slave_names = os.listdir(dir)
        for slave_name in slave_names:
            # if it's a dm-X name, resolve it to a map name
            if slave_name.startswith("dm-"):
                dev_name = devicemapper.name_from_dm_node(slave_name)
            else:
                dev_name = slave_name
            slave_dev = self.getDeviceByName(dev_name)
            if slave_dev:
                slaves.append(slave_dev)
            else:
                # we haven't scanned the slave yet, so do it now
                path = os.path.normpath("%s/%s" % (dir, slave_name))
                new_info = udev_get_block_device(os.path.realpath(path)[4:])
                if new_info:
                    self.addDevice(new_info)
                    if self.getDeviceByName(dev_name) is None:
                        # if the current slave is still not in
                        # the tree, something has gone wrong
                        ctx.logger.error("failure scanning device %s: could not add slave %s" % (name, dev_name))
                        return

        # try to get the device again now that we've got all the slaves
        device = self.getDeviceByName(name)

        if device is None:
            device = self.getDeviceByUUID(info.get("MD_UUID"))
            if device:
                raise DeviceTreeError("RAID device %s already in "
                                      "devicetree as %s" % (name, device.name))

        # if we get here, we found all of the slave devices and
        # something must be wrong -- if all of the slaves we in
        # the tree, this device should be as well
        if device is None:
            raise DeviceTreeError("MD RAID device %s not in devicetree after "
                                  "scanning all slaves" % name)
        return device

    def addDeviceMapper(self, info):
        name = udev_device_get_name(info)
        uuid = udev_device_get_uuid(info)
        sysfs_path = udev_device_get_sysfs_path(info)
        device = None

        for devicemapperdevice in self.devices:
            if not isinstance(devicemapperdevice, DeviceMapper):
                continue

            try:
                # there is a device in the tree already with the same
                # major/minor as this one but with a different name
                # XXX this is kind of racy
                if devicemapperdevice.getDMNode() == os.path.basename(sysfs_path):
                    # XXX should we take the name already in use?
                    device = devicemapperdevice
                    break
            except devicemapper.DeviceMapperError:
                # This is a little lame, but the VG device is a DMDevice
                # and it won't have a dm node. At any rate, this is not
                # important enough to crash the install.
                ctx.logger.debug("failed to find dm node for %s" % devicemapperdevice.name)
                continue

        if device is None:
            # we couldn't find it, so create it
            # first, get a list of the slave devs and look them up
            slaves = []
            dir = os.path.normpath("/sys/%s/slaves" % sysfs_path)
            slave_names = os.listdir(dir)
            for slave_name in slave_names:
                # if it's a dm-X name, resolve it to a map name first
                if slave_name.startswith("dm-"):
                    dev_name = devicemapper.name_from_dm_node(slave_name)
                else:
                    dev_name = slave_name
                slave_dev = self.getDeviceByName(dev_name)
                if slave_dev:
                    slaves.append(slave_dev)
                else:
                    # we haven't scanned the slave yet, so do it now
                    path = os.path.normpath("%s/%s" % (dir, slave_name))
                    new_info = udev_get_block_device(os.path.realpath(path)[4:])
                    if new_info:
                        self.addDevice(new_info)
                        if self.getDeviceByName(dev_name) is None:
                            # if the current slave is still not in
                            # the tree, something has gone wrong
                            ctx.logger.error("failure scanning device %s: could not add slave %s" % (name, dev_name))
                            return

            # try to get the device again now that we've got all the slaves
            device = self.getDeviceByName(name)

            if device is None:
                if udev_device_is_multipath_partition(info):
                    diskname = udev_device_get_dm_partition_disk(info)
                    disk = self.getDeviceByName(diskname)
                    return self.addPartition(info, disk=disk)
                elif udev_device_is_dmraid_partition(info):
                    diskname = udev_device_get_dm_partition_disk(info)
                    disk = self.getDeviceByName(diskname)
                    return self.addPartition(info, disk=disk)

            # if we get here, we found all of the slave devices and
            # something must be wrong -- if all of the slaves are in
            # the tree, this device should be as well
            if device is None:
                lvm.lvm_cc_addFilterRejectRegexp(name)
                ctx.logger.warning("ignoring dm device %s" % name)

        return device

    def addPartition(self, info, disk=None):
        name = udev_device_get_name(info)
        uuid = udev_device_get_uuid(info)
        sysfs_path = udev_device_get_sysfs_path(info)
        device = None

        if disk is None:
            disk_name = os.path.basename(os.path.dirname(sysfs_path))
            disk_name = disk_name.replace('!','/')
            disk = self.getDeviceByName(disk_name)

        if disk is None:
            # create a device instance for the disk
            new_info = udev_get_block_device(os.path.dirname(sysfs_path))
            if new_info:
                self.addDevice(new_info)
                disk = self.getDeviceByName(disk_name)

            if disk is None:
                # if the current device is still not in
                # the tree, something has gone wrong
                ctx.logger.error("failure scanning device %s" % disk_name)
                lvm.lvm_cc_addFilterRejectRegexp(name)
                return

        # Check that the disk has partitions. If it does not, we must have
        # reinitialized the disklabel.
        #
        # Also ignore partitions on devices we do not support partitioning
        # of, like logical volumes.
        if not getattr(disk.format, "partitions", None) or \
           not disk.partitionable:
            # When we got here because the disk does not have a disklabel
            # format (ie a biosraid member), or because it is not
            # partitionable we want LVM to ignore this partition too
            if disk.format.type != "disklabel" or not disk.partitionable:
                lvm.lvm_cc_addFilterRejectRegexp(name)
            ctx.logger.debug("ignoring partition %s" % name)
            return

        try:
            device = Partition(name, sysfsPath=sysfs_path,
                               major=udev_device_get_major(info),
                               minor=udev_device_get_minor(info),
                               exists=True, parents=[disk])
        except DeviceTreeError:
            # corner case sometime the kernel accepts a partition table
            # which gets rejected by parted, in this case we will
            # prompt to re-initialize the disk, so simply skip the
            # faulty partitions.
            return

        self._addDevice(device)
        return device

    def addDisk(self, info):
        name = udev_device_get_name(info)
        uuid = udev_device_get_uuid(info)
        sysfs_path = udev_device_get_sysfs_path(info)
        serial = udev_device_get_serial(info)
        bus = udev_device_get_bus(info)

        # udev doesn't always provide a vendor.
        vendor = udev_device_get_vendor(info)
        if not vendor:
            vendor = ""

        device = None

        kwargs = { "serial": serial, "vendor": vendor, "bus": bus }
        if udev_device_get_md_container(info):
            diskType = RaidArray
            parentName = devicePathToName(udev_device_get_md_container(info))
            kwargs["parents"] = [ self.getDeviceByName(parentName) ]
            kwargs["level"]  = udev_device_get_md_level(info)
            kwargs["memberDevices"] = int(udev_device_get_md_devices(info))
            kwargs["uuid"] = udev_device_get_md_uuid(info)
            kwargs["exists"]  = True
            del kwargs["serial"]
            del kwargs["vendor"]
            del kwargs["bus"]
            ctx.logger.debug("%s is a raid array" % name)
        else:
            diskType = Disk
            ctx.logger.debug("%s is a disk" % name)


        device = diskType(name,
                          major=udev_device_get_major(info),
                          minor=udev_device_get_minor(info),
                          sysfsPath=sysfs_path, **kwargs)

        self._addDevice(device)
        return device

    def addOpticalDevice(self, info):
        # XXX should this be RemovableDevice instead?
        #
        # Looks like if it has ID_INSTANCE=0:1 we can ignore it.
        device = OpticalDevice(udev_device_get_name(info),
                               major=udev_device_get_major(info),
                               minor=udev_device_get_minor(info),
                               sysfsPath=udev_device_get_sysfs_path(info),
                               vendor=udev_device_get_vendor(info),
                               model=udev_device_get_model(info))
        self._addDevice(device)
        return device

    def addDevice(self, info):
        name = udev_device_get_name(info)
        uuid = udev_device_get_uuid(info)
        sysfs_path = udev_device_get_sysfs_path(info)

        if self.isIgnored(info):
            ctx.logger.debug("ignoring %s (%s)" % (name, sysfs_path))
            return

        ctx.logger.debug("scanning %s (%s)..." % (name, sysfs_path))
        device = self.getDeviceByName(name)

        if udev_device_is_dm(info):
            ctx.logger.debug("%s is a device-mapper device" % name)
            # try to look up the device
            if device is None and uuid:
                # try to find the device by uuid
                device = self.getDeviceByUUID(uuid)

            if device is None:
                device = self.addDeviceMapper(info)
        elif udev_device_is_md(info):
            ctx.logger.debug("%s is an md device" % name)
            if device is None and uuid:
                # try to find the device by uuid
                device = self.getDeviceByUUID(uuid)
            if device is None:
                device = self.addRaidArray(info)
        elif udev_device_is_cdrom(info):
            ctx.logger.debug("%s is a cdrom" % name)
            if device is None:
                device = self.addOpticalDevice(info)
        elif udev_device_is_biosraid_member(info) and udev_device_is_disk(info):
            ctx.logger.debug("%s is part of a biosraid" % name)
            if device is None:
                device = Disk(name,
                              major=udev_device_get_major(info),
                              minor=udev_device_get_minor(info),
                              sysfsPath=sysfs_path, exists=True)
                self._addDevice(device)
        elif udev_device_is_disk(info):
            if device is None:
                device = self.addDisk(info)
        elif udev_device_is_partition(info):
            ctx.logger.debug("%s is a partition" % name)
            if device is None:
                device = self.addPartition(info)
        else:
            ctx.logger.error("Unknown block device type for: %s" % name)
            return

        if device and device.name in self.protectedDeviceNames:
            device.protected = True

        if not device or not device.mediaPresent:
            return

        ctx.logger.debug("%s is created as : %s" % (name, device))
        self.handleFormat(info, device)
        ctx.logger.debug("got device: %s" % device)
        if device.format.type:
            ctx.logger.debug("%s device has format: %s" % (name, device.format))
        device.originalFormat = device.format

    def handleFormat(self, info, device):
        name = udev_device_get_name(info)
        sysfs_path = udev_device_get_sysfs_path(info)
        uuid = udev_device_get_uuid(info)
        label = udev_device_get_label(info)
        format_type = udev_device_get_format(info)
        serial = udev_device_get_serial(info)

        if not udev_device_is_biosraid_member(info) and \
           not udev_device_is_multipath_member(info):
            self.handleDiskLabelFormat(info, device)
            if device.partitioned or self.isIgnored(info) or \
               (not device.partitionable and
                device.format.type == "disklabel"):
                # If the device has a disklabel, or the user chose not to
                # create one, we are finished with this device. Otherwise
                # it must have some non-disklabel formatting, in which case
                # we fall through to handle that.
                return

        if not isinstance(device, OpticalDevice) and device.removable and format_type == "iso9660":
            ctx.logger.debug("Removable device %s is iso9660 format. We have to remove from devices index" % device.name)
            if ctx.bootloader:
                ctx.bootloader.removableExists = True
            self._removeDevice(device)

        format = None
        if (not device) or (not format_type) or device.format.type:
            # this device has no formatting or it has already been set up
            # FIXME: this probably needs something special for disklabels
            ctx.logger.debug("no type or existing type for %s, bailing" % (name,))
            return

        # set up the common arguments for the format constructor
        args = [format_type]
        kwargs = {"uuid": uuid,
                  "label": label,
                  "device": device.path,
                  "serial": serial,
                  "exists": True}
        if format_type == "LVM2_member":
            # lvm
            try:
                kwargs["vgName"] = udev_device_get_vg_name(info)
            except KeyError as e:
                ctx.logger.debug("PV %s has no vg_name" % name)
            try:
                kwargs["vgUuid"] = udev_device_get_vg_uuid(info)
            except KeyError:
                ctx.logger.debug("PV %s has no vg_uuid" % name)
            try:
                kwargs["peStart"] = udev_device_get_pv_pe_start(info)
            except KeyError:
                ctx.logger.debug("PV %s has no pe_start" % name)
        elif format_type in RaidMember._udevTypes:
            try:
                kwargs["mdUuid"] = udev_device_get_md_uuid(info)
            except KeyError:
                ctx.logger.debug("mdraid member %s has no md uuid" % name)
            kwargs["biosraid"] = udev_device_is_biosraid_member(info)
        if format_type == "vfat":
            if isinstance(device, Partition) and device.bootable:
                efi = formats.getFormat("efi")
                if efi.minSize <= device.size <= efi.maxSize:
                    args[0] = "efi"

        elif format_type == "hfs":
            # apple bootstrap magic
            if isinstance(device, Partition) and device.bootable:
                apple = formats.getFormat("appleboot")
                if apple.minSize <= device.size <= apple.maxSize:
                    args[0] = "appleboot"
        try:
            ctx.logger.debug("type detected on '%s' is '%s'" % (name, format_type,))
            device.format = formats.getFormat(*args, **kwargs)
        except FilesystemError:
            ctx.logger.debug("type '%s' on '%s' invalid, assuming no format" %
                      (format_type, name,))
            device.format = formats.Format()
            return

        if shouldClear(device, self.clearPartType, clearPartDisks=self.clearPartDisks):
            # if this is a device that will be cleared by clearpart,
            # don't bother with format-specific processing
            return

        if device.format.type == "lvmpv":
            self.handlePhysicalVolumeFormat(info, device)
        elif device.format.type == "mdmember":
            self.handleRaidMemberFormat(info, device)
        elif device.format.type == "dmraidmember":
            self.handleDMRaidMemberFormat(info, device)

    def handleDiskLabelFormat(self, info, device):
        if udev_device_get_format(info):
            ctx.logger.debug("device %s does not contain a disklabel" % device.name)
            return

        if device.partitioned:
            # this device is already set up
            ctx.logger.debug("disklabel format on %s already set up" % device.name)
            return

        try:
            device.setup()
        except Exception as e:
            ctx.logger.debug("setup of %s failed: %s" % (device.name, e))
            ctx.logger.warning("aborting disklabel handler for %s" % device.name)
            return

        # special handling for unsupported partitioned devices
        if not device.partitionable:
            try:
                format = formats.getFormat("disklabel",
                                   device=device.path,
                                   exists=True)
            except InvalidDiskLabelError:
                pass
            else:
                if format.partitions:
                    # parted's checks for disklabel presence are less than
                    # rigorous, so we will assume that detected disklabels
                    # with no partitions are spurious
                    device.format = format
            return

        # if the disk contains protected partitions we will not wipe the
        # disklabel even if clearpart --initlabel was specified
        if not self.clearPartDisks or device.name in self.clearPartDisks:
            initlabel = self.reinitializeDisks
            sysfs_path = udev_device_get_sysfs_path(info)
            for protected in self.protectedDeviceNames:
                # check for protected partition
                _p = "/sys/%s/%s" % (sysfs_path, protected)
                if os.path.exists(os.path.normpath(_p)):
                    initlabel = False
                    break

                # check for protected partition on a device-mapper disk
                disk_name = re.sub(r'p\d+$', '', protected)
                if disk_name != protected and disk_name == device.name:
                    initlabel = False
                    break
        else:
            initlabel = False

        if self.zeroMbr:
            initcb = lambda: True
        else:
            bypath = None
            details = None
            description = device.description or device.model
            try:
                bypath = os.path.basename(deviceNameToDiskByPath(device.name))
            except DeviceNotFoundError:
                # some devices don't have a /dev/disk/by-path/ #!@#@!@#
                bypath = device.name


            initcb = lambda: questionInitializeDisk(ctx.interface, bypath, description,
                                                    device.size, device.name)

        try:
            format = formats.getFormat("disklabel",
                               device=device.path,
                               exists=not initlabel)
        except InvalidDiskLabelError:
            # if there is preexisting formatting on the device we will
            # use it instead of ignoring the device
            if not self.zeroMbr and \
               formats.getFormat(udev_device_get_format(info)).type is not None:
                return
            # if we have a cb function use it. else we ignore the device.
            if initcb is not None and initcb():
                format = formats.getFormat("disklabel",
                                   device=device.path,
                                   exists=False)
            else:
                self._removeDevice(device)
                self.addIgnoredDisk(device.name)
                return

        if not format.exists:
            # if we just initialized a disklabel we should schedule
            # operations for destruction of the previous format and creation
            # of the new one
            self.addOperation(OperationDestroyFormat(device))
            self.addOperation(OperationCreateFormat(device, format))

            # If this is a mac-formatted disk we just initialized, make
            # sure the partition table partition gets added to the device
            # tree.
            if device.format.partedDisk.type == "mac" and \
               len(device.format.partitions) == 1:
                name = device.format.partitions[0].getDeviceNodeName()
                if not self.getDeviceByName(name):
                    partition = Partition(name, exists=True, parents=[device])
                    self._addDevice(partition)

        else:
            device.format = format

    def handlePhysicalVolumeFormat(self, info, device):
        # lookup/create the VG and LVs
        try:
            vg_name = udev_device_get_vg_name(info)
        except KeyError:
            # no vg name means no vg -- we're done with this pv
            return

        vg_device = self.getDeviceByName(vg_name)
        if vg_device:
            vg_device._addDevice(device)
        else:
            try:
                vg_uuid = udev_device_get_vg_uuid(info)
                vg_size = udev_device_get_vg_size(info)
                vg_free = udev_device_get_vg_free(info)
                pe_size = udev_device_get_vg_extent_size(info)
                pe_count = udev_device_get_vg_extent_count(info)
                pe_free = udev_device_get_vg_free_extents(info)
                pv_count = udev_device_get_vg_pv_count(info)
            except (KeyError, ValueError) as e:
                ctx.logger.warning("invalid data for %s: %s" % (device.name, e))
                return

            vg_device = VolumeGroup(vg_name, device, uuid=vg_uuid,
                                    size=vg_size, free=vg_free,
                                    peSize=pe_size, peCount=pe_count,
                                    peFree=pe_free, pvCount=pv_count,
                                    exists=True)
            self._addDevice(vg_device)

        # Now we add any lv info found in this pv to the vg_device, we
        # do this for all pvs as pvs only contain lv info for lvs which they
        # contain themselves
        try:
            lv_names = udev_device_get_lv_names(info)
            lv_uuids = udev_device_get_lv_uuids(info)
            lv_sizes = udev_device_get_lv_sizes(info)
            lv_attr = udev_device_get_lv_attr(info)
        except KeyError as e:
            ctx.logger.warning("invalid data for %s: %s" % (device.name, e))
            return

        if not lv_names:
            ctx.logger.debug("no logical volumes listed for Volume Group %s" %
                            device.name)
            return

        for i in range(len(lv_names)):
            # Skip empty and already added lvs
            if not lv_names[i] or lv_names[i] in vg_device.lv_names:
                continue

            vg_device.lv_names.append(lv_names[i])
            vg_device.lv_uuids.append(lv_uuids[i])
            vg_device.lv_sizes.append(lv_sizes[i])
            vg_device.lv_attr.append(lv_attr[i])

        return self.handleLogicalVolumes(vg_device)

    def handleRaidMemberFormat(self, info, device):
        # either look up or create the array device
        name = udev_device_get_name(info)
        sysfs_path = udev_device_get_sysfs_path(info)

        md_array = self.getDeviceByUUID(device.format.mdUuid)
        if device.format.mdUuid and md_array:
            md_array._addDevice(device)
        else:
            # create the array with just this one member
            # FIXME: why does this exact block appear twice?
            try:
                # level is reported as, eg: "raid1"
                md_level = udev_device_get_md_level(info)
                md_devices = int(udev_device_get_md_devices(info))
                md_uuid = udev_device_get_md_uuid(info)
            except (KeyError, ValueError) as e:
                ctx.logger.warning("invalid data for %s: %s" % (name, e))
                return

            # try to name the array based on the preferred minor
            md_info = raid.mdexamine(device.path)
            md_path = md_info.get("device", "")
            md_name = devicePathToName(md_info.get("device", ""))
            if md_name:
                try:
                    # md_name can be either md# or md/#
                    if md_name.startswith("md/"):
                        minor = int(md_name[3:])     # strip off leading "md/"
                        md_name = "md%d" % minor     # use a regular md# name
                    else:
                        minor = int(md_name[2:])     # strip off leading "md"
                except (IndexError, ValueError):
                    minor = None
                    md_name = None
                else:
                    array = self.getDeviceByName(md_name)
                    if array and array.uuid != md_uuid:
                        md_name = None

            if not md_name:
                # if we don't have a name yet, find the first unused minor
                minor = 0
                while True:
                    if self.getDeviceByName("md%d" % minor):
                        minor += 1
                    else:
                        break

                md_name = "md%d" % minor

            ctx.logger.debug("using name %s for md array containing member %s"
                             % (md_name, device.name))
            md_array = RaidArray(md_name,
                                 level=md_level,
                                 minor=minor,
                                 memberDevices=md_devices,
                                 uuid=md_uuid,
                                 sysfsPath=sysfs_path,
                                 exists=True)
            md_array._addDevice(device)
            self._addDevice(md_array)

    def handleDMRaidMemberFormat(self, info, device):
        """ Handle device mapper raid member disk. """
        name = udev_device_get_name(info)
        sysfs_path = udev_device_get_sysfs_path(info)
        uuid = udev_device_get_uuid(info)
        major = udev_device_get_major(info)
        minor = udev_device_get_minor(info)

        def _all_ignored(rss):
            retval = True
            for rs in rss:
                if rs.name not in self._ignoredDisks:
                    retval = False
                    break
            return retval

        # Have we already created the DMRaidArray?
        rss = block.getRaidSetFromRelatedMem(uuid=uuid, name=name,
                                            major=major, minor=minor)
        if len(rss) == 0:
            # we ignore the device in the hope that all the devices
            # from this set will be ignored.
            self.unusedRaidMembers.append(device.name)
            self.addIgnoredDisk(device.name)
            return

        # We ignore the device if all the rss are in self._ignoredDisks
        if _all_ignored(rss):
            self.addIgnoredDisk(device.name)
            return

        for rs in rss:
            dm_array = self.getDeviceByName(rs.name)
            if dm_array is not None:
                # We add the new device.
                dm_array._addDevice(device)
            else:
                # Activate the Raid set.
                rs.activate(mknod=True)
                dm_array = DMRaidArray(rs.name,
                                                 raidSet=rs,
                                                 parents=[device])

                self._addDevice(dm_array)

                # Wait for udev to scan the just created nodes, to avoid a race
                # with the udev_get_block_device() call below.
                udev_settle()

                # Get the DMRaidArray a DiskLabel format *now*, in case
                # its partitions get scanned before it does.
                dm_array.updateSysfsPath()
                dm_array_info = udev_get_block_device(dm_array.sysfsPath)
                self.handleDiskLabelFormat(dm_array_info, dm_array)

                # Use the rs's object on the device.
                # pyblock can return the memebers of a set and the
                # device has the attribute to hold it.  But ATM we
                # are not really using it. Commenting this out until
                # we really need it.
                #device.format.raidmem = block.getMemFromRaidSet(dm_array,
                #        major=major, minor=minor, uuid=uuid, name=name)

    def handleLogicalVolumes(self, vg_device):
        ret = False
        vg_name = vg_device.name
        lv_names = vg_device.lv_names
        lv_uuids = vg_device.lv_uuids
        lv_sizes = vg_device.lv_sizes
        lv_attr = vg_device.lv_attr

        if not vg_device.complete:
            ctx.logger.warning("Skipping LVs for incomplete VG %s" % vg_name)
            return False

        if not lv_names:
            ctx.logger.debug("no LVs listed for VG %s" % vg_name)
            return False

        # make a list of indices with snapshots at the end
        indices = range(len(lv_names))
        indices.sort(key=lambda i: lv_attr[i][0] in 'Ss')
        for index in indices:
            lv_name = lv_names[index]
            name = "%s-%s" % (vg_name, lv_name)
            if lv_attr[index][0] in 'Ss':
                ctx.logger.debug("found lvm snapshot volume '%s'" % name)
                origin_name = lvm.lvorigin(vg_name, lv_name)
                if not origin_name:
                    ctx.logger.error("lvm snapshot '%s-%s' has unknown origin" %
                                    (vg_name, lv_name))
                    continue

                origin = self.getDeviceByName("%s-%s" % (vg_name, origin_name))
                if not origin:
                    ctx.logger.warning("snapshot lv '%s' origin lv '%s-%s not found" %
                                      (name, vg_name, origin_name))
                    continue

                ctx.logger.debug("adding %dMB to %s snapshot total" %
                                (lv_sizes[index], origin.name))
                origin.snapshotSpace += lv_sizes[index]
                continue
            elif lv_attr[index][0] in 'Iil':
                # skip mirror images and log volumes
                continue

            log_size = 0
            if lv_attr[index][0] in 'Mm':
                stripes = 0
                # identify mirror stripes/copies and mirror logs
                for (j, _lvname) in enumerate(lv_names):
                    if lv_attr[j][0] not in 'Iil':
                        continue

                    if _lvname == "[%s_mlog]" % lv_name:
                        log_size = lv_sizes[j]
                    elif _lvname.startswith("[%s_mimage_" % lv_name):
                        stripes += 1
            else:
                stripes = 1

            lv_dev = self.getDeviceByName(name)
            if lv_dev is None:
                lv_uuid = lv_uuids[index]
                lv_size = lv_sizes[index]
                lv_device = LogicalVolume(lv_name, vg_device, uuid=lv_uuid,
                                          size=lv_size, stripes=stripes,
                                          logSize=log_size, exists=True)
                self._addDevice(lv_device)
                try:
                    lv_device.setup()
                except DeviceError as (msg, name):
                    ctx.logger.info("setup of %s failed: %s" % (lv_device.name, msg))

        return ret

    def handleInconsistencies(self):
        def reinitializeVG(vg):
            # First we remove VG data
            try:
                vg.destroy()
            except DeviceError:
                # the pvremoves will finish the job.
                ctx.logger.debug("There was an error destroying the VG %s." % vg.name)

            # remove VG device from list.
            self._removeDevice(vg)

            for parent in vg.parents:
                parent.format.destroy()

                # Give the vg the a default format
                kwargs = {"device": parent.path,
                          "exists": parent.exists}
                parent.format = formats.getFormat(*[""], **kwargs)

        def leafInconsistencies(device):
            if device.type == "lvmvg":
                if device.complete:
                    return

                paths = []
                for parent in device.parents:
                    paths.append(parent.path)

                # if zeroMbr is true don't ask.
                if (self.zeroMbr or questionReinitInconsistentLVM(ctx.interface, pv_names=paths, vg_name=device.name)):
                    reinitializeVG(device)
                else:
                    # The user chose not to reinitialize.
                    # hopefully this will ignore the vg components too.
                    self._removeDevice(device)
                    lvm.lvm_cc_addFilterRejectRegexp(device.name)
                    lvm.blacklistVG(device.name)
                    for parent in device.parents:
                        if parent.type == "partition":
                            parent.immutable = \
                                _("This partition is part of an inconsistent LVM Volume Group.")
                        else:
                            self._removeDevice(parent, moddisk=False)
                            self.addIgnoredDisk(parent.name)
                        lvm.lvm_cc_addFilterRejectRegexp(parent.name)

        # Address the inconsistencies present in the tree leaves.
        for leaf in self.leaves:
            leafInconsistencies(leaf)

        # Check for unused BIOS raid members, unused dmraid members are added
        # to self.unusedRaidMembers as they are processed, extend this list
        # with unused mdraid BIOS raid members
        for container in self.getDevicesByType("mdcontainer"):
            if container.kids == 0:
                self.unusedRaidMembers.extend(map(lambda m: m.name, container.devices))

        questionUnusedRaidMembers(ctx.interface, self.unusedRaidMembers)

    def getDependentDevices(self, dep):
        """Return list of devices that depend on.

           The list includes both direct and indirect dependents.
        """
        dependents = []
        logicals = []
        if isinstance(dep, Partition) and dep.partType and dep.isExtended:
            for partition in self.getDevicesByInstance(Partition):
                if partition.partType and partition.isLogical and partition.disk == dep.disk:
                    logicals.append(partition)

        for device in self.devices:
            if device.dependsOn(dep):
                dependents.append(device)
            else:
                for logical in logicals:
                    if device.dependsOn(logical):
                        dependents.append(device)
                        break

        return dependents

    def populate(self):
        """Locate all storage devices."""
        self._populated = False

        devices = udev_get_block_devices()
        for device in devices:
            self.addDevice(device)

        # First iteration - let's just look for disks.
        old_devices = {}
        for device in devices:
            old_devices[device['name']] = device
        while True:
            devices = []
            new_devices = udev_get_block_devices()

            for new_device in new_devices:
                if not old_devices.has_key(new_device['name']):
                    old_devices[new_device['name']] = new_device
                    devices.append(new_device)

            if len(devices) == 0:
                # nothing is changing -- time to setup lvm lvs and scan them
                # we delay this till all other devices are scanned so that
                # 1) the lvm filter for ignored disks is completely setup
                # 2) we have checked all devs for duplicate vg names
                if self.setupLogicalVolumes():
                    continue
                # nothing is changing -- we are finished building devices
                break

            ctx.logger.info("devices to scan: %s" % [d['name'] for d in devices])
            for device in devices:
                self.addDevice(device)

        self._populated = True
        # After having the complete tree we make sure that the system
        # inconsistencies are ignored or resolved.
        self.handleInconsistencies()
        self.teardownAll()

    def teardownAll(self):
        """ Run teardown methods on all devices. """
        for device in self.leaves:
            try:
                device.teardown(recursive=True)
            except DeviceTreeError as e:
                ctx.logger.info("teardown of %s failed: %s" % (device.name, e))

    def setupAll(self):
        """ Run setup methods on all devices. """
        for device in self.leaves:
            try:
                device.setup(recursive=True)
            except DeviceTreeError as e:
                ctx.logger.info("setup of %s failed: %s" % (device.name, e))

    def setupLogicalVolumes(self):
        ret = False

        for device in self.getDevicesByType("lvmvg"):
            if self.handleLogicalVolumes(device):
                ret = True

        return ret

    def getDeviceByName(self, name):
        if not name:
            return None

        ctx.logger.debug("looking for device by name '%s'..." % name)

        found = None
        for device in self._devices:
            if device.name == name:
                found = device
                break
            elif (device.type == "lvmlv" or device.type == "lvmvg") and \
                    device.name == name.replace("--","-"):
                found = device
                break

        ctx.logger.debug("%s found by name is %s" % (name, found))
        return found

    def getDeviceByUUID(self, uuid):
        if not uuid:
            return None

        ctx.logger.debug("looking for device by uuid '%s'..." % uuid)

        found = None
        for device in self._devices:
            if device.uuid == uuid:
                found = device
                break
            elif device.format.uuid == uuid:
                found = device
                break

        ctx.logger.debug("%s found by uuid is %s" % (uuid, found))
        return found

    def getDevicesBySerial(self, serial):
        devices = []
        ctx.logger.debug("looking for device by serial '%s'..." % serial)
        for device in self._devices:
            if not hasattr(device, "serial"):
                ctx.logger.warning("device %s has no serial attr" % device.name)
                continue
            if device.serial == serial:
                devices.append(device)
        return devices

    def getDeviceByLabel(self, label):
        if not label:
            return None

        ctx.logger.debug("looking for device by label '%s'..." % label)

        found = None
        for device in self._devices:
            _label = getattr(device.format, "label", None)
            if not _label:
                continue

            if _label == label:
                found = device
                break

        ctx.logger.debug("%s found by label is %s" % (label, found))
        return found

    def getDeviceByPath(self, path):
        if not path:
            return None

        ctx.logger.debug("looking for device by path '%s'..." % path)

        found = None
        for device in self._devices:
            if device.path ==  path:
                found = device
                break
            elif (device.type == "lvmlv" or device.type == "lvmvg") and \
                    device.path == path.replace("--","-"):
                found = device
                break

        ctx.logger.debug("%s found by path is %s" % (path, found))
        return found

    def getDeviceBySysPath(self, sysfsPath):
        if not sysfsPath:
            return None

        ctx.logger.debug("looking for device '%s'..." % sysfsPath)
        found = None
        for device in self._devices:
            if device.sysfsPath == sysfsPath:
                found = device
                break

        ctx.logger.debug("%s found by syspath is %s" % (sysfsPath, found))
        return found

    def getDevicesByType(self, type):
        return [d for d in self._devices if d.type == type]

    def getDevicesByInstance(self, device):
        return [d for d in self._devices if isinstance(d, device)]

    def getChildren(self, device):
        """ Return a list of a device's children. """
        return [c for c in self._devices if device in c.parents]

    @property
    def devices(self):
        """ List of device instances """
        devices = []
        for device in self._devices:
            if device.path in [d.path for d in devices] and \
               not isinstance(device, NoDevice):
                raise DeviceTreeError("duplicate paths in device tree")
            devices.append(device)

        return devices

    @property
    def uuids(self):
        """ Dict with uuid keys and Device values. """
        uuids = {}
        for dev in self._devices:
            try:
                uuid = dev.uuid
            except AttributeError:
                uuid = None
            if uuid:
                uuids[uuid] = dev
            try:
                uuid = dev.format.uuid
            except AttributeError:
                uuid = None
            if uuid:
                uuids[uuid] = dev
        return uuids

    @property
    def labels(self):
        labels = {}
        for dev in self._devices:
            if dev.format and getattr(dev.format, "label", None):
                labels[dev.format.label] = dev

        return labels

    @property
    def leaves(self):
        """ List of all devices upon which no other devices exist. """
        leaves = [d for d in self._devices if d.isleaf]
        return leaves

    @property
    def filesystems(self):
        """ List of filesystems. """
        filesystems = []
        for dev in self.leaves:
            if dev.format and getattr(dev.format, 'mountpoint', None):
                filesystems.append(dev.format)

        return filesystems


    def resolveDevice(self, devspec, blkidTab=None, cryptTab=None):
        # find device in the tree
        device = None
        if devspec.startswith("UUID="):
            # device-by-uuid
            uuid = devspec.split("=")[-1]
            device = self.uuids.get(uuid)
            if device is None:
                ctx.logger.error("failed to resolve device %s" % devspec)
        elif devspec.startswith("LABEL="):
            # device-by-label
            label = devspec.split("=")[-1]
            device = self.labels.get(label)
            if device is None:
                ctx.logger.error("failed to resolve device %s" % devspec)
        elif devspec.startswith("/dev/"):
            if devspec.startswith("/dev/disk/"):
                devspec = os.path.realpath(devspec)

                if devspec.startswith("/dev/dm-"):
                    dm_name = devicemapper.name_from_dm_node(devspec[5:])
                    if dm_name:
                        devspec = "/dev/mapper/" + dm_name

            # device path
            device = self.getDeviceByPath(devspec)
            if device is None:
                if blkidTab:
                    # try to use the blkid.tab to correlate the device
                    # path with a UUID
                    blkidTabEnt = blkidTab.get(devspec)
                    if blkidTabEnt:
                        ctx.logger.debug("found blkid.tab entry for '%s'" % devspec)
                        uuid = blkidTabEnt.get("UUID")
                        if uuid:
                            device = self.getDeviceByUuid(uuid)
                            if device:
                                devstr = device.name
                            else:
                                devstr = "None"
                            ctx.logger.debug("found device '%s' in tree" % devstr)
                        if device and device.format and \
                           device.format.type == "luks":
                            map_name = device.format.mapName
                            ctx.logger.debug("luks device; map name is '%s'" % map_name)
                            mapped_dev = self.getDeviceByName(map_name)
                            if mapped_dev:
                                device = mapped_dev

                if device is None and cryptTab and \
                   devspec.startswith("/dev/mapper/"):
                    # try to use a dm-crypt mapping name to 
                    # obtain the underlying device, possibly
                    # using blkid.tab
                    cryptTabEnt = cryptTab.get(devspec.split("/")[-1])
                    if cryptTabEnt:
                        luks_dev = cryptTabEnt['device']
                        try:
                            device = self.getChildren(luks_dev)[0]
                        except IndexError as e:
                            pass
                elif device is None:
                    name = devspec[5:]      # strip off leading "/dev/"
                    (vg_name, slash, lv_name) = name.partition("/")
                    if lv_name and not "/" in lv_name:
                        # looks like we may have one
                        lv = "%s-%s" % (vg_name, lv_name)
                        device = self.getDeviceByName(lv)

        if device:
            ctx.logger.debug("resolved '%s' to '%s' (%s)" % (devspec, device.name, device.type))
        else:
            ctx.logger.debug("failed to resolve '%s'" % devspec)
        return device
