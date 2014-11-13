# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
import copy
import parted
import gettext
_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL, QMenu, QTreeWidgetItem, QIcon

import yali.util
import yali.context as ctx
from yali.gui.YaliDialog import Dialog, QuestionDialog
from yali.gui import ScreenWidget

from yali.gui.partition_gui import PartitionEditor
from yali.gui.lvm_gui import LVMEditor
from yali.gui.raid_gui import RaidEditor
from yali.gui.Ui.manualpartwidget import Ui_ManualPartWidget
from yali.storage.library import lvm
from yali.storage import formats
from yali.storage.devices.device import devicePathToName, Device
from yali.storage.devices.partition import Partition
from yali.storage.partitioning import doPartitioning, hasFreeDiskSpace, PartitioningError, PartitioningWarning
from yali.storage.storageBackendHelpers import doDeleteDevice, doClearPartitionedDevice, checkForSwapNoMatch, getPreExistFormatWarnings, confirmResetPartitionState

class Widget(QWidget, ScreenWidget):
    name = "manualPartitioning"

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_ManualPartWidget()
        self.ui.setupUi(self)
        self.storage = ctx.storage
        self.intf = ctx.interface

        # New Device Popup Menu
        self.setupMenu()

        #self.connect(self.ui.newButton, SIGNAL("clicked()"),self.createDevice)
        self.connect(self.ui.editButton, SIGNAL("clicked()"),self.editDevice)
        self.connect(self.ui.deleteButton, SIGNAL("clicked()"),self.deleteDevice)
        self.connect(self.ui.resetButton, SIGNAL("clicked()"),self.reset)
        self.connect(self.ui.deviceTree, SIGNAL("itemClicked(QTreeWidgetItem *, int)"), self.activateButtons)
        self.connect(self.menu, SIGNAL("triggered(QAction*)"), self.createDevice)

    def shown(self):
        checkForSwapNoMatch(self.intf, self.storage)
        self.populate()
        (errors, warnings) =  self.storage.sanityCheck()
        if errors or warnings:
            ctx.mainScreen.disableNext()
        else:
            ctx.mainScreen.enableNext()
        self.update()

    def execute(self):
        ctx.logger.info("Manual Partitioning selected...")
        ctx.mainScreen.processEvents()
        check = self.nextCheck()
        if not check:
            ctx.mainScreen.enableBack()
        elif check is None:
            ctx.mainScreen.enableNext()
        return check

    def update(self):
        if self.storage.storageset.rootDevice:
            ctx.mainScreen.enableNext()
        else:
            ctx.mainScreen.disableNext()
        self.updateMenus()

    def activateButtons(self, item, index):
        if item:
            if isinstance(item.device, Device) and not isinstance(item.device, parted.partition.Partition):
                self.ui.editButton.setEnabled(True)
                self.ui.deleteButton.setEnabled(True)
            else:
                self.ui.editButton.setEnabled(False)
                self.ui.deleteButton.setEnabled(False)

    def nextCheck(self):
        (errors, warnings) = self.storage.sanityCheck()
        if errors:
            detailed =  _("The partitioning scheme you requested "
                          "caused the following critical errors."
                          "You must correct these errors before "
                          "you continue your installation of %s.") \
                         % yali.util.product_name()

            comments = "\n\n".join(errors)
            self.intf.detailedMessageWindow(_("Partitioning Errors"),
                                             detailed, comments, type="error")
            return False

        if warnings:
            detailed = _("The partitioning scheme you requested generated the "
                         "following warnings. Would you like to continue with "
                         "your requested partitioning "
                         "scheme?")

            comments = "\n\n".join(warnings)
            rc = self.intf.detailedMessageWindow(_("Partitioning Warnings"),
                                                  detailed, comments, type="custom", customIcon="warning",
                                                  customButtons=[_("Ok"), _("Cancel")], default=1)

        formatWarnings = getPreExistFormatWarnings(self.storage)
        if formatWarnings:
            detailed = _("The following pre-existing devices have "
                         "been selected to be formatted, destroying "
                         "all data.")

            comments = ""
            for (device, type, mountpoint) in formatWarnings:
                comments = comments + "%s         %s         %s\n" % (device, type, mountpoint)

            rc = self.intf.detailedMessageWindow(_("Format Warnings"),
                                                  detailed, comments, type="custom", customIcon="warning",
                                                  customButtons=[_("Format"), _("Cancel")], default=1)
            if rc:
                return False

        return True


    def backCheck(self):
        rc = self.intf.messageWindow(_("Warning"), _("All Changes that you made will be removed"),
                                      type="custom", customIcon="warning",
                                      customButtons=[_("Ok"), _("Cancel")], default=1)
        if not rc:
            self.storage.reset()
            return True
        return False

    def setupMenu(self):
        self.menu = QMenu("New")
        self.standardDevices = self.menu.addMenu(_("Standard"))
        self.lvmDevices = self.menu.addMenu(_("LVM"))
        self.raidDevices = self.menu.addMenu(_("RAID"))

        self.createPartition = self.standardDevices.addAction(_("Partition"))
        self.createPartition.setWhatsThis(_("General purpose of partition creation"))
        self.createPartition.setVisible(False)
        self.createPhysicalVolume = self.lvmDevices.addAction(_("Physical Volume"))
        self.createPhysicalVolume.setWhatsThis(_("Create LVM formatted partition"))
        self.createPhysicalVolume.setVisible(False)
        self.createVolumeGroup = self.lvmDevices.addAction(_("Volume Group"))
        self.createVolumeGroup.setWhatsThis(_("Requires at least 1 free LVM formatted partition"))
        self.createVolumeGroup.setVisible(False)
        self.createLogicalVolume = self.lvmDevices.addAction(_("Logical Volume"))
        self.createLogicalVolume.setWhatsThis(_("Create Logical Volume on selected Volume Group"))
        self.createLogicalVolume.setVisible(False)
        self.createRaidMember = self.raidDevices.addAction(_("Member"))
        self.createRaidMember.setWhatsThis(_("Create Raid formatted partition"))
        self.createRaidMember.setVisible(False)
        self.createRaidArray= self.raidDevices.addAction(_("Array"))
        self.createRaidArray.setWhatsThis(_("Requires at least 2 free Raid formatted partition"))
        self.createRaidArray.setVisible(False)

        self.ui.newButton.setMenu(self.menu)

    def addDevice(self, device, item):
        if device.format.hidden:
            return

        format = device.format

        if not format.exists:
            formatIcon = QIcon(":/gui/pics/tick.png")
        else:
            #formatIcon = QIcon(":/gui/pics/dialog-error.png")
            formatIcon = QIcon("")

        # mount point string
        if format.type == "lvmpv":
            vg = None
            for _vg in self.storage.vgs:
                if _vg.dependsOn(device):
                    vg = _vg
                    break
            mountpoint = getattr(vg, "name", "")
        elif format.type == "mdmember":
            array = None
            for _array in self.storage.raidArrays:
                if _array.dependsOn(device):
                    array = _array
                    break

            mountpoint = getattr(array, "name", "")
        else:
            mountpoint = getattr(format, "mountpoint", "")
            if mountpoint is None:
                mountpoint = ""

        # device name
        name = getattr(device, "lvname", device.name)

        # label
        label = getattr(format, "label", "")
        if label is None:
            label = ""

        item.setDevice(device)
        item.setName(name)
        item.setMountpoint(mountpoint)
        item.setLabel(label)
        item.setType(format.name)
        item.setSize("%Ld" % device.size)
        item.setFormat(formatIcon)
        item.setExpanded(True)

    def populate(self):
        # Clear device tree
        self.ui.deviceTree.clear()

        # first do LVM
        vgs = self.storage.vgs
        if vgs:
            volumeGroupsItem = DeviceTreeItem(self.ui.deviceTree)
            volumeGroupsItem.setName(_("Volume Groups"))
            volumeGroupsItem.setExpanded(True)
            for vg in vgs:
                volumeGroupItem = DeviceTreeItem(volumeGroupsItem)
                self.addDevice(vg, volumeGroupItem)
                volumeGroupItem.setType("")
                for lv in vg.lvs:
                    logicalVolumeItem = DeviceTreeItem(volumeGroupItem)
                    self.addDevice(lv, logicalVolumeItem)

                # We add a row for the VG free space.
                if vg.freeSpace > 0:
                    freeLogicalVolumeItem = DeviceTreeItem(volumeGroupItem)
                    freeLogicalVolumeItem.setName(_("Free"))
                    freeLogicalVolumeItem.setSize("%Ld" % vg.freeSpace)
                    freeLogicalVolumeItem.setDevice(None)
                    freeLogicalVolumeItem.setMountpoint("")

        # handle RAID next
        raidarrays = self.storage.raidArrays
        if raidarrays:
            raidArraysItem = DeviceTreeItem(self.ui.deviceTree)
            raidArraysItem.setName(_("Raid Arrays"))
            raidArraysItem.setExpanded(True)
            for array in raidarrays:
                raidArrayItem = DeviceTreeItem(raidArraysItem)
                self.addDevice(array, raidArrayItem)

        # now normal partitions
        disks = self.storage.partitioned
        # also include unpartitioned disks that aren't mpath or biosraid
        whole = filter(lambda d: not d.partitioned and not d.format.hidden,
                       self.storage.disks)
        disks.extend(whole)
        disks.sort(key=lambda d: d.name)
        # Disk&Partitions
        drivesItem = DeviceTreeItem(self.ui.deviceTree)
        drivesItem.setName(_("Hard Drives"))
        drivesItem.setExpanded(True)
        for disk in disks:
            diskItem = DeviceTreeItem(drivesItem)
            diskItem.setExpanded(True)
            diskItem.setName("%s - %s" % (disk.model, disk.name))
            #self.ui.deviceTree.expandItem(diskItem)
            if disk.partitioned:
                partition = disk.format.firstPartition
                extendedItem = None
                while partition:
                    if partition.type & parted.PARTITION_METADATA:
                        partition = partition.nextPartition()
                        continue

                    partName = devicePathToName(partition.getDeviceNodeName())
                    device = self.storage.devicetree.getDeviceByName(partName)

                    if not device and not partition.type & parted.PARTITION_FREESPACE:
                        ctx.logger.debug("can't find partition %s in device tree" % partName)

                    # Force partitions tree item not to be less than 12 MB
                    if partition.getSize(unit="MB") <= 12.0:
                        if not partition.active or not partition.getFlag(parted.PARTITION_BOOT):
                            partition = partition.nextPartition()
                            continue

                    if device and device.isExtended:
                        if extendedItem:
                            raise RuntimeError, _("Can't handle more than "
                                                 "one extended partition per disk")
                        extendedItem = partItem = DeviceTreeItem(diskItem)
                        partitionItem = extendedItem

                    elif device and device.isLogical:
                        if not extendedItem:
                            raise RuntimeError, _("Crossed logical partition before extended")
                        partitionItem = DeviceTreeItem(extendedItem)

                    else:
                        # Free space item
                        if partition.type & parted.PARTITION_LOGICAL:
                            partitionItem = DeviceTreeItem(extendedItem)
                        else:
                            partitionItem = DeviceTreeItem(diskItem)


                    if device and not device.isExtended:
                        self.addDevice(device, partitionItem)
                    else:
                        # either extended or freespace
                        if partition.type & parted.PARTITION_FREESPACE:
                            deviceName = _("Free")
                            device = partition
                            deviceType = ""
                        else:
                            deviceName = device.name
                            deviceType = _("Extended")

                        partitionItem.setName(deviceName)
                        partitionItem.setType(deviceType)
                        size = partition.getSize(unit="MB")
                        if size < 1.0:
                            size = "< 1"
                        else:
                            size = "%Ld" % (size)
                        partitionItem.setSize(size)
                        partitionItem.setDevice(device)

                    partition = partition.nextPartition()
            else:
                self.addDevice(disk, diskItem)

    def refresh(self, justRedraw=None):
        ctx.logger.debug("refresh: justRedraw=%s" % justRedraw)
        self.ui.deviceTree.clear()
        if justRedraw:
            rc = 0
        else:
            try:
                doPartitioning(self.storage)
                rc = 0
            except PartitioningError, msg:
                self.intf.messageWindow(_("Error Partitioning"), 
                                        _("Could not allocate requested partitions: %s.") % msg,
                                        customIcon="error")
                rc = -1
            except PartitioningWarning, msg:
                rc = self.intf.messageWindow(_("Warning Partitioning"),
                                             _("Warning: %s.") % msg,
                                             customButtons=[_("Modify Partition"), _("Continue")],
                                             customIcon="warning")
                if rc == 1:
                    rc = -1
                else:
                    rc = 0
                    all_devices = self.storage.devicetree.devices
                    bootDevs = [d for d in all_devices if d.bootable]

        if not rc == -1:
            self.populate()

        self.update()
        return rc


    def getCurrentDevice(self):
        if self.ui.deviceTree.currentItem():
            return self.ui.deviceTree.currentItem().device

    def getCurrentDeviceParent(self):
        """ Return the parent of the selected row.  Returns an item.
            None if there is no parent.
        """
        pass

    def updateMenus(self):
        self.createPartition.setVisible(True)
        activatePartition = False

        try:
            freePartition = hasFreeDiskSpace(self.storage)
        except AttributeError, msg:
            ctx.logger.debug(msg)
        else:
            if freePartition:
                activatePartition = True

        activateVolumeGroup = False
        availablePVS = len(self.storage.unusedPVS())
        if (lvm.has_lvm() and
                formats.getFormat("lvmpv").supported and
                availablePVS > 0):
            activateVolumeGroup = True

        activateRaidArray = False
        availableRaidMembers = len(self.storage.unusedRaidMembers())
        availableMinors = len(self.storage.unusedRaidMinors)
        if (availableMinors > 0
                and formats.getFormat("mdmember").supported
                and availableRaidMembers > 1):
            activateRaidArray = True


        """if (not activatePartition and not activateVolumeGroup):
            self.intf.messageWindow(_("Cannot perform any creation operation"),
                                    _("Note that the creation operation requires one of the\nfollowing:"
                                      " * Free space in one of the Hard Drives.\n"
                                      " * At least one free physical volume (LVM) partition.\n"
                                      " * At least one Volume Group with free space."),
                                    customIcon="warning")
            return"""

        freeVolumeGroupSpace = []
        for vg in self.storage.vgs:
            if vg.freeSpace > 0:
                freeVolumeGroupSpace.append(vg)

        activateLogicalVolume = False
        if len(freeVolumeGroupSpace) > 0:
            activateLogicalVolume = True

        self.createPartition.setVisible(activatePartition)
        self.createPhysicalVolume.setVisible(activatePartition)
        self.createRaidMember.setVisible(activatePartition)

        self.createVolumeGroup.setVisible(activateVolumeGroup)
        self.createLogicalVolume.setVisible(activateVolumeGroup)

        self.createRaidArray.setVisible(activateRaidArray)

        if activateLogicalVolume:
            #FIXME: find way to show only logical volume editor
            pass


    def createDevice(self, action):

        if action == self.createRaidArray:
            raidarray = self.storage.newRaidArray(fmt_type=self.storage.defaultFSType)
            self.editRaidArray(raidarray, isNew=True)
            return

        elif action == self.createVolumeGroup:
            vg = self.storage.newVolumeGroup()
            self.editVolumeGroup(vg, isNew=True)
            return
        else:
            device = self.getCurrentDevice()
            if isinstance(device, parted.partition.Partition):
                if action == self.createRaidMember:
                    raidmember = self.storage.newPartition(fmt_type="mdmember")
                    self.editPartition(raidmember, isNew=True, partedPartition=device, restricts=["mdmember"])
                    return
                elif action == self.createPhysicalVolume:
                    physicalvolume = self.storage.newPartition(fmt_type="lvmpv")
                    self.editPartition(physicalvolume, isNew=True, partedPartition=device, restricts=["lvmpv"])
                    return
                elif action == self.createPartition:
                    format = self.storage.defaultFSType
                    partition = self.storage.newPartition(fmt_type=format)
                    self.editPartition(partition, isNew=True, partedPartition=device)
                    return
            else:
                ctx.interface.messageWindow(_("Partition Selection Warning"),
                                            _("Please select free physical partition to create new device."),
                                            type="warning")


    def editDevice(self, *args):
        device = self.getCurrentDevice()
        if device and not isinstance(device, parted.partition.Partition):
            reason = self.storage.deviceImmutable(device, ignoreProtected=True)

            if reason:
                self.intf.messageWindow(_("Unable To Edit"),
                                       _("You cannot edit this device:\n\n%s")
                                        % reason,
                                        type="warning")
                return

            if device.type == "mdarray":
                self.editRaidArray(device)
            elif device.type == "lvmvg":
                self.editVolumeGroup(device)
            elif device.type == "lvmlv":
                self.editLogicalVolume(lv=device)
            elif isinstance(device, Partition):
                self.editPartition(device)



    def editVolumeGroup(self, device, isNew=False):
        volumegroupEditor =  LVMEditor(self, device, isNew=isNew)

        while True:
            origDevice = copy.copy(device)
            operations = volumegroupEditor.run()

            for operation in operations:
                self.storage.devicetree.addOperation(operation)

            if self.refresh(justRedraw=not operations):
                operations.reverse()

                for operation in operations:
                    self.storage.devicetree.removeOperation(operation)

                if not isNew:
                    device = origDevice

                if self.refresh():
                    raise RuntimeError, ("Returning partitions to state "
                                         "prior to edit failed")
            else:
                break

        volumegroupEditor.destroy()

    def editLogicalVolume(self, lv=None, vg=None):
        """Will be consistent with the state of things and use this funciton
        for creating and editing LVs.

        lv -- the logical volume to edit.  If this is set there is no need
              for the other two arguments.
        vg -- the volume group where the new lv is going to be created. This
              will only be relevant when we are createing an LV.
        """
        if lv != None:
            volumegroupEditor = LVMEditor(self, lv.vg, isNew=False)
            lv = volumegroupEditor.lvs[lv.lvname]
            isNew = False

        elif vg != None:
            volumegroupEditor = LVMEditor(self, vg, isNew=False)
            tempvg = volumegroupEditor.tmpVolumeGroup
            name = self.storage.createSuggestedLogicalVolumeName(tempvg)
            format = formats.getFormat(self.storage.defaultFSType)
            volumegroupEditor.lvs[name] = {'name': name,
                                           'size': vg.freeSpace,
                                           'format': format,
                                           'originalFormat': format,
                                           'stripes': 1,
                                           'logSize': 0,
                                           'snapshotSpace': 0,
                                           'exists': False}
            lv = volumegroupEditor.lvs[name]
            isNew = True

        else:
            return

        while True:
            #volumegroupEditor.editLogicalVolume(lv, isNew=isNew)
            operations = volumegroupEditor.run()

            for operation in operations:
                self.storage.devicetree.addOperation(operation)

            if self.refresh(justRedraw=True):
                operations.reverse()
                for operation in operations:
                    self.storage.devicetree.removeOperation(operation)

                if self.refresh():
                    raise RuntimeError, ("Returning partitions to state "
                                         "prior to edit failed")
                continue
            else:
                break

        volumegroupEditor.destroy()

    def editRaidArray(self, device, isNew=False):
        raideditor = RaidEditor(self, device, isNew)

        while True:
            operations = raideditor.run()

            for operation in operations:
                self.storage.devicetree.addOperation(operation)

            if self.refresh(justRedraw=True):
                operation.reverse()
                for operation in operation:
                    self.storage.devicetree.removeOperation(operation)
                    if self.refresh():
                        raise RuntimeError, ("Returning partitions to state "
                                             "prior to RAID edit failed")
                continue
            else:
                break

        raideditor.destroy()

    def editPartition(self, device, isNew=False, partedPartition=None, restricts=None):
        partitionEditor = PartitionEditor(self, device, isNew=isNew, partedPartition=partedPartition, restricts=restricts)

        while True:
            origDevice = copy.copy(device)
            operations = partitionEditor.run()
            for operation in operations:
                self.storage.devicetree.addOperation(operation)

            if self.refresh(justRedraw=not operations):
                operations.reverse()
                for operation in operations:
                    self.storage.devicetree.removeOperation(operation)

                if not isNew:
                    device.req_size = origDevice.req_size
                    device.req_base_size = origDevice.req_base_size
                    device.req_grow = origDevice.req_grow
                    device.req_max_size = origDevice.req_max_size
                    device.req_primary = origDevice.req_primary
                    device.req_disks = origDevice.req_disks

                if self.refresh():
                    raise RuntimeError, ("Returning partitions to state "
                                         "prior to edit failed")
            else:
                break

        partitionEditor.destroy()

    def deleteDevice(self):
        device = self.getCurrentDevice()
        if device:
            if device.partitioned:
                if doClearPartitionedDevice(self.intf, self.storage, device):
                    self.refresh()
            elif doDeleteDevice(self.intf, self.storage, device):
                if isinstance(device, Partition):
                    justRedraw = False
                else:
                    justRedraw = True
                    if device.type == "lvmlv" and device in device.vg.lvs:
                        device.vg._removeLogicalVolume(device)

                self.refresh(justRedraw=justRedraw)

    def reset(self):
        if confirmResetPartitionState(self.intf):
            return
        self.storage.reset()
        self.ui.deviceTree.clear()
        self.refresh(justRedraw=True)


class DeviceTreeItem(QTreeWidgetItem):
    def __init__(self, parent, device=None):
        QTreeWidgetItem.__init__(self, parent)
        self.device = device

    def setDevice(self, device):
        self.device = device

    def setName(self, device):
        self.setText(0, device)

    def setMountpoint(self, mountpoint):
        self.setText(1, mountpoint)

    def setLabel(self, label):
        self.setText(2, label)

    def setType(self, type):
        self.setText(3, type)

    def setFormat(self, format):
        self.setIcon(4, format)

    def setSize(self, size):
        self.setText(5, size)


