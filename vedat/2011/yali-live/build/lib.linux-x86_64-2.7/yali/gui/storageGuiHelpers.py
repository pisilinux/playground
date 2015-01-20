#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

import yali.context as ctx
from yali.storage.library import raid
from yali.storage.library import lvm
from yali.storage.formats import device_formats, get_default_filesystem_type

defaultMountPoints = ['/', '/boot', '/home', '/tmp', '/var', '/opt']


class DriveItem(QtGui.QListWidgetItem):
    def __init__(self, parent, drive):
        QtGui.QListWidgetItem.__init__(self, parent)
        size = "%8.0f MB" % drive.size
        self.setText("%s -%s" % (drive.name, size))
        self._drive = drive

    @property
    def drive(self):
        return self._drive

class PartitionItem(QtGui.QListWidgetItem):
    def __init__(self, parent, partition):
        QtGui.QListWidgetItem.__init__(self, parent)
        size = "%8.0f MB" % partition.size
        self.setText("%s -%s" % (partition.name, size))
        self._partition = partition

    @property
    def partition(self):
        return self._partition

class PhysicalVolumeListItem(QtGui.QListWidgetItem):
    def __init__(self, parent, widget):
        QtGui.QListWidgetItem.__init__(self, parent)
        self.widget = widget
        self.setSizeHint(QSize(40, 40))

class PhysicalVolumeItem(QtGui.QWidget):
    def __init__(self, parent, text, device, editor, widget):
        QtGui.QListWidgetItem.__init__(self, parent)
        self.layout = QtGui.QHBoxLayout(self)
        self.checkBox = QtGui.QCheckBox(self)
        self.layout.addWidget(self.checkBox)
        self.labelDrive = QtGui.QLabel(self)
        self.labelDrive.setText(text)
        self.layout.addWidget(self.labelDrive)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layout.addItem(spacerItem)
        self.connect(self.checkBox, SIGNAL("stateChanged(int)"), self.stateChanged)
        self.pv = device
        self.editor = editor
        self.widget = widget

    def stateChanged(self, state):
        if state == Qt.Checked and self.pv not in self.editor.pvs:
            self.editor.pvs.append(self.pv)
        elif state == Qt.Unchecked and self.pv in self.editor.pvs:
            self.editor.pvs.remove(self.pv)
            try:
                self.widget.tmpVolumeGroup
            except Exception, msg:
                self.editor.intf.messageWindow(_("Not enough space"),
                                               _("You cannot remove this physical volume because\n"
                                                 "otherwise the volume group will be too small to\n"
                                                 "hold the currently defined logical volumes."),
                                               customIcon="error")
                self.editor.pvs.append(self.pv)
        #Update spaces not only if physical volume unchecked
        self.widget.updateSpaces()

def fillResizablePartitions(widget, storage):
    biggest = -1
    i = -1
    for partition in storage.partitions:
        if not partition.exists:
            continue

        if partition.resizable and partition.format.resizable:
            entry = u"%s (%s, %d MB)" % (partition.name, partition.format.name, math.floor(partition.size))
            widget.addItem(entry, partition)

            i += 1
            if biggest == -1:
                biggest = i
            else:
                current = widget.itemData(biggest).toPyObject()
                if partition.format.targetSize > current.format.targetSize:
                    biggest = i

    if biggest > -1:
        widget.setCurrentIndex(biggest)

def fillMountpointMenu(widget, request, excludes=[]):
    mountpoints = []
    label = getattr(request.format, "label", None)
    if request.exists and label and label.startswith("/"):
        mountpoints.append(label)
        id = 0

    for mnt in defaultMountPoints:
        if mnt in excludes:
            continue

        if not (mnt in mountpoints) and (mnt[0] =="/"):
            mountpoints.append(mnt)

    if (request.format.type or request.format.migrate) and \
            request.format.mountable and request.format.mountpoint:
        if request.format.mountpoint not in mountpoints:
            mountpoints.append(request.format.mountpoint)

    for mountpoint in mountpoints:
        if mountpoint in defaultMountPoints:
            if mountpoint != "/home":
                widget.addItem(mountpoint, True)
            else:
                widget.addItem(mountpoint, False)
        else:
            widget.addItem(mountpoint, False)

    if (request.format.type or request.format.migrate) and request.format.mountable:
        mountpoint = request.format.mountpoint
        if mountpoint:
            if mountpoint in mountpoints:
               widget.setCurrentIndex(widget.findText(mountpoint))
    else:
        widget.setCurrentIndex(0)
        widget.setEnabled(False)


def fillFilesystemMenu(widget, format, availables=None, ignores=None):
    if availables:
        names =availables
    else:
        names = device_formats.keys()

    if format and format.supported and format.formattable:
        default = format.type
    else:
        default = get_default_filesystem_type()

    index = 0
    i = 0
    for name in names:
        format = device_formats[name]()
        if not format.supported:
            continue

        if ignores and name in ignores:
            continue

        if format.formattable:
            widget.addItem(name)
            if default == name:
                index = i
            i += 1

    widget.setCurrentIndex(index)

def fillPhysicalExtends(widget, default=4096):
    def prettyFormatSize(value):
        """ Pretty print for PhysicalExtends size in KB """
        if value < 1024:
            return "%d KB" % value
        elif value < 1024*1024:
            return "%d MB" % (value/1024)
        else:
            return "%d GB" % (value/1024/1024)

    actualPhysicalExtends = []
    for curpe in lvm.getPossiblePhysicalExtents(floor=1024):
        if curpe > 131072 and curpe != default:
            continue

        actualPhysicalExtends.append(curpe)
        value = prettyFormatSize(curpe)

        widget.addItem(value, curpe)

    try:
        widget.setCurrentIndex(actualPhysicalExtends.index(default))
    except ValueError:
        widget.setCurrentIndex(0)


def fillLvmPhysicals(widget):

    def calculateSize(value):
        if value[1] == "KB":
            return value[0]
        elif value[1] == "MB":
            return value[0] * 1024
        else:
            return value[0] * 1024 * 1024

    originalpvs = widget.parent().parent.pvs[:]
    peCombo = widget.parent().physicalExtends
    for device in widget.parent().parent.availlvmparts:
        peSize = peCombo.itemData(peCombo.currentIndex()).toFloat()[0] / 1024.0
        size = "%10.2f MB" % lvm.clampSize(device.size, peSize)
        include = True
        selected = False

        if device in originalpvs:
            selected = True
            include = True
        else:
            for vg in widget.parent().parent.storage.vgs:
                if vg.name == widget.parent().origrequest.name:
                    continue

                if device in vg.pvs:
                    include = False
                    break

            if include and not originalpvs:
                selected = True

        if include:
            physicalVolume = PhysicalVolumeItem(widget, "%s (%s)" % (device.name, size), device, widget.parent().parent, widget.parent())
            listItem = PhysicalVolumeListItem(widget, physicalVolume)
            widget.setItemWidget(listItem, physicalVolume)
            if selected:
                physicalVolume.checkBox.setCheckState(Qt.Checked)
            if selected and device not in widget.parent().parent.pvs:
                widget.parent().parent.pvs.append(device)

def fillRaidMembers(widget, raidPartitions, requestRaidPartition, preexist):
    tmpDevices = []
    if not widget.parent().isNew:
        for device in requestRaidPartition:
            tmpDevices.append(device)

    for partition in raidPartitions:
            if partition in tmpDevices:
                partitionItem = PartitionItem(widget, partition)
                partitionItem.setCheckState(2)
            else:
                if not widget.parent().origrequest.exists:
                    partitionItem = PartitionItem(widget, partition)
                    partitionItem.setCheckState(0)

def fillRaidMinors(widget, raidMinors, requestedMinor):
    index = 0
    i = 0
    for minor in raidMinors:
        widget.addItem("md%d" % minor, minor)
        if requestedMinor and minor == requestedMinor:
            index = i
        i = i + 1

    widget.setCurrentIndex(index)

def fillRaidLevels(widget, raidLevels, requestedLevel):
    index = 0
    if raid.RAID1 in raidLevels:
        index = raidLevels.index(raid.RAID1)
    i = 0
    for level in raidLevels:
        widget.addItem("RAID%d" % level, level)
        if requestedLevel is not None and level == requestedLevel:
            index = i
        i = i + 1

    widget.setCurrentIndex(index)


def fillAllowedDrives(widget, disks, requestDrives, selectDrives=True, disallowes=[]):
    widget.clear()
    for disk in disks:
        selected = 0
        if selectDrives:
            if requestDrives:
                if disk.name in requestDrives:
                    selected = 2
            else:
                if disk not in disallowes:
                    selected = 2

        driveItem = DriveItem(widget, disk)
        driveItem.setCheckState(selected)
        if len(disks) < 2:
            widget.setEnabled(False)
        else:
            widget.setEnabled(True)
