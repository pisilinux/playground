#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import copy
import parted
import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext


from PyQt4 import QtGui
from PyQt4.QtCore import *

import yali.util
import yali.context as ctx
from yali.gui.YaliDialog import Dialog
from yali.gui.Ui.partition import Ui_PartitionWidget
from yali.gui import storageGuiHelpers
from yali.storage import formats
from yali.storage import partitioning
from yali.storage.operations import *
from yali.storage.storageBackendHelpers import queryNoFormatPreExisting, sanityCheckMountPoint, doUIRAIDLVMChecks

class PartitionEditor:
    def __init__(self, parent, origrequest, isNew=False, partedPartition=None, restricts=None):
        self.storage = parent.storage
        self.intf = parent.intf
        self.origrequest = origrequest
        self.isNew = isNew
        self.parent = parent
        self.partedPartition = partedPartition

        if isNew:
            title = _("Create Partition on %(path)s (%(model)s)") %  {"path":os.path.basename(partedPartition.disk.device.path),
                                                                      "model":partedPartition.disk.device.model}
        else:
            try:
                title = _("Edit Partition %s") % origrequest.path
            except:
                title = _("Edit Partition")

        self.dialog = Dialog(title, closeButton=False)
        self.dialog.addWidget(PartitionWidget(self, origrequest, isNew, restricts))
        self.dialog.resize(QSize(350, 175))

    def run(self):
        if self.dialog is None:
            return []

        while 1:
            rc = self.dialog.exec_()
            operations = []

            if not rc:
                self.destroy()
                return []

            widget = self.dialog.content

            mountpoint = unicode(widget.mountpointMenu.currentText())
            active = widget.mountpointMenu.isEnabled()
            if active and mountpoint:
                msg = sanityCheckMountPoint(mountpoint)
                if msg:
                    ctx.interface.messageWindow(_("Mount Point Error"), msg,
                                                type="warning")
                    continue

                used = False
                for (mp, dev) in self.storage.mountpoints.iteritems():
                    if mp == mountpoint and \
                       dev.id != self.origrequest.id and \
                       not (self.origrequest.format.type == "luks" and
                            self.origrequest in dev.parents):
                        used = True
                        break

                if used:
                    ctx.interface.messageWindow(_("Mount point in use"),
                                                _("The mount point \"%s\" is in "
                                                  "use. Please pick another.") %
                                                (mountpoint,),
                                                type="warning")
                    continue

            if not self.origrequest.exists:
                if widget.primaryCheck.isChecked():
                    primary = True
                else:
                    primary = None

                size = widget.sizeSpin.value()

                formatType = str(widget.filesystemMenu.currentText())
                format = formats.getFormat(formatType, mountpoint=mountpoint)
                if self.isNew:
                    disk = self.storage.devicetree.getDeviceByPath(self.partedPartition.disk.device.path)
                else:
                    disk = self.origrequest.disk

                err = doUIRAIDLVMChecks(format, [disk.name], self.storage)
                if err:
                    self.intf.messageWindow(_("Error With Request"),
                                            err, type="error")
                    continue

                weight = partitioning.weight(mountpoint=mountpoint, fstype=format.type)

                if self.isNew:
                    request = self.storage.newPartition(size=size,
                                                        grow=None,
                                                        maxsize=0,
                                                        primary=primary,
                                                        format=format,
                                                        parents=disk)
                else:
                    request = self.origrequest
                    request.weight = weight

                usedev = request

                if self.isNew:
                    operations.append(OperationCreateDevice(request))
                else:
                    request.req_size = size
                    request.req_base_size = size
                    request.req_grow = None
                    request.req_max_size = 0
                    request.req_primary = primary
                    request.req_disks = [disk]

                operations.append(OperationCreateFormat(usedev, format))

            else:
                # preexisting partition
                request = self.origrequest
                usedev = request

                origformat = usedev.format
                devicetree = self.storage.devicetree

                if widget.formatRadio.isChecked():
                    formatType = str(widget.formatCombo.currentText())
                    format = formats.getFormat(formatType, mountpoint=mountpoint, device=usedev.path)

                    operations.append(OperationCreateFormat(usedev, format))
                else:
                    cancel = []
                    cancel.extend(devicetree.findOperations(type="destroy",
                                                            object="format",
                                                            devid=request.id))
                    cancel.extend(devicetree.findOperations(type="create",
                                                            object="format",
                                                            devid=request.id))
                    cancel.reverse()
                    for operation in cancel:
                        devicetree.removeOperation(operation)

                    request.format = request.originalFormat
                    usedev = request

                    if usedev.format.mountable:
                        usedev.format.mountpoint = mountpoint

                if self.origrequest.protected and usedev.format.mountable:
                    # users can set a mountpoint for protected partitions
                    usedev.format.mountpoint = mountpoint

                request.weight = partitioning.weight(mountpoint=mountpoint, fstype=request.format.type)

                if widget.migrateRadio.isChecked():
                    operations.append(OperationMigrateFormat(usedev))

                if widget.resizeRadio.isChecked():
                    size = widget.resizeSpin.value()
                    try:
                        operations.append(OperationResizeDevice(request, size))
                        if request.format.type and request.format.exists:
                            operations.append(OperationResizeFormat(request, size))
                    except ValueError:
                        pass

                if request.format.exists and \
                   getattr(request, "mountpoint", None) and \
                   self.storage.formatByDefault(request):
                    if not queryNoFormatPreExisting(self.intf):
                        continue

            # everything ok, fall out of loop
            break

        return operations

    def destroy(self):
        if self.dialog:
            self.dialog = None


class PartitionWidget(QtGui.QWidget, Ui_PartitionWidget):
    def __init__(self, parent, request, isNew, restricts=None):
        QtGui.QWidget.__init__(self, parent.parent)
        self.setupUi(self)
        self.parent = parent
        self.origrequest = request
        self.isNew = isNew

        if not self.origrequest.exists:
            if self.parent.partedPartition and self.parent.partedPartition.type & parted.PARTITION_LOGICAL:
                self.primaryCheck.hide()

        # Mount Point entry
        storageGuiHelpers.fillMountpointMenu(self.mountpointMenu, self.origrequest)
        QObject.connect(self.mountpointMenu, SIGNAL("currentIndexChanged(int)"), self.mountPointChanged)

        # This empty radioButton is hack about enabling autoExclusive formatRadio according to mountpoint.(#16446)
        self.radioButton.hide()
        if not self.origrequest.exists:
            #Nont existing partition filesystem type
            storageGuiHelpers.fillFilesystemMenu(self.filesystemMenu, self.origrequest.format,
                                                 availables=restricts)
            QObject.connect(self.filesystemMenu, SIGNAL("currentIndexChanged(int)"), self.formatTypeChanged)
            self.resizeRadio.hide()
            self.resizeSlider.hide()
            self.resizeSpin.hide()
            self.formatRadio.hide()
            self.formatCombo.hide()
            self.migrateRadio.hide()
            self.migrateCombo.hide()
        else:
            self.primaryCheck.hide()
            self.filesystemLabel.hide()
            self.filesystemMenu.hide()
            #To format existing partition
            if self.origrequest.format.formattable or not self.origrequest.format.type:
                storageGuiHelpers.fillFilesystemMenu(self.formatCombo, self.origrequest.format)
                self.formatRadio.setChecked(self.origrequest.format.formattable and not self.origrequest.format.exists)
                QObject.connect(self.formatRadio, SIGNAL("toggled(bool)"), self.formatRadioToggled)
                QObject.connect(self.formatCombo, SIGNAL("currentIndexChanged(int)"), self.formatTypeChanged)
            else:
                self.formatRadio.hide()
                self.formatCombo.hide()

            if self.origrequest.format.migratable and self.origrequest.format.exists:
                storageGuiHelpers.fillFilesystemMenu(self.migrateCombo, self.origrequest.format,
                                                     availables=[self.origrequest.format.migrationTarget])
                self.migrateRadio.setChecked(self.origrequest.format.migrate and not self.formatRadio.isChecked())
                QObject.connect(self.migrateCombo, SIGNAL("currentIndexChanged(int)"), self.formatTypeChanged)
            else:
                self.migrateRadio.hide()
                self.migrateCombo.hide()

            if self.origrequest.resizable and self.origrequest.format.exists:
                if self.origrequest.targetSize is not None:
                    value = self.origrequest.targetSize
                else:
                    value = self.origrequest.size

                reqlower = 1
                requpper = self.origrequest.maxSize
                if self.origrequest.format.exists:
                    reqlower = self.origrequest.minSize

                    if self.origrequest.type == "partition":
                        geomsize = self.origrequest.partedPartition.geometry.getSize(unit="MB")
                        if (geomsize != 0) and (requpper > geomsize):
                            requpper = geomsize

                self.resizeSpin.setMinimum(reqlower)
                self.resizeSpin.setMaximum(requpper)
                self.resizeSpin.setValue(value)
                self.resizeSlider.setMinimum(reqlower)
                self.resizeSlider.setMaximum(requpper)
                self.resizeSlider.setValue(value)
            else:
                self.resizeRadio.hide()
                self.resizeSpin.hide()
                self.resizeSlider.hide()

        #Size
        if not self.origrequest.exists:
            if self.parent.isNew:
                maxsize = self.parent.partedPartition.getSize(unit="MB")
                self.sizeSpin.setMaximum(maxsize)
                self.sizeSlider.setMaximum(maxsize)
            elif not self.parent.isNew and self.origrequest.req_size:
                self.sizeSpin.setMaximum(self.origrequest.req_size)
                self.sizeSpin.setValue(self.origrequest.req_size)
                self.sizeSlider.setMaximum(self.origrequest.req_size)
                self.sizeSlider.setValue(self.origrequest.req_size)
        else:
            self.sizeLabel.hide()
            self.sizeSpin.hide()
            self.sizeSlider.hide()

        #create only as primary
        if not self.origrequest.exists and \
        self.parent.storage.extendedPartitionsSupported:
            self.primaryCheck.setChecked(False)
            if self.origrequest.req_primary:
                self.primaryCheck.setChecked(True)

        self.connect(self.buttonBox, SIGNAL("accepted()"), self.parent.dialog.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.parent.dialog.reject)

    def enableMountpoint(self, format):
        if format.mountable:
            self.mountpointMenu.setEnabled(True)
        else:
            self.mountpointMenu.setEnabled(False)
            self.mountpointMenu.setCurrentIndex(0)

    def formatRadioToggled(self, checked):
        if checked:
            format  = formats.getFormat(str(self.formatCombo.currentText()))
            self.enableMountpoint(format)

    def formatTypeChanged(self, index):
        format  = formats.getFormat(str(self.sender().itemText(index)))
        self.enableMountpoint(format)

    def mountPointChanged(self, index):
        if yali.util.isEfi() and self.mountpointMenu.itemText(index) == "/boot/efi":
            self.filesystemMenu.setCurrentIndex(self.filesystemMenu.findText(formats.getFormat("efi").name))
        elif self.mountpointMenu.itemText(index) == "/boot":
            self.filesystemMenu.setCurrentIndex(self.filesystemMenu.findText(formats.get_default_filesystem_type(boot=True)))

        if self.formatRadio.isVisible():
            self.radioButton.setChecked(True)
            self.formatRadio.setChecked(self.mountpointMenu.itemData(index).toBool())
