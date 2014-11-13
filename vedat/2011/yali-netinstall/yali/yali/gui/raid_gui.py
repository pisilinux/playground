#!/usr/bin/python
# -*- coding: utf-8 -*-
import gettext
_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL, QObject, QSize, Qt

from yali.gui.YaliDialog import Dialog
from yali.gui.Ui.raid import Ui_RaidWidget
from yali.gui import storageGuiHelpers
from yali.storage import formats
from yali.storage.library import raid
from yali.storage.operations import OperationCreateDevice, OperationDestroyDevice, OperationCreateFormat, OperationMigrateFormat
from yali.storage.storageBackendHelpers import queryNoFormatPreExisting, sanityCheckMountPoint

class RaidEditor(object):
    def __init__(self, parent, request, isNew=False):
        self.parent = parent
        self.storage = parent.storage
        self.intf = parent.intf
        self.origrequest = request
        self.isNew = isNew

        availraidparts = self.parent.storage.unusedRaidMembers(array=self.origrequest)
        if availraidparts < 2:
            self.intf.messageWindow(_("Invalid Raid Members"),
                                    _("At least two unused software RAID "
                                     "partitions are needed to create "
                                     "a RAID device.\n\n"
                                     "First create at least two partitions "
                                     "of type \"software RAID\", and then "
                                     "select the \"RAID\" option again."),
                                    type="error")
            return

        if isNew:
            title = _("Make RAID Device")
        else:
            if request.minor is not None:
                title = _("Edit RAID Device: %s") % request.path
            else:
                title = _("Edit RAID Device")

        self.dialog = Dialog(title, closeButton=False)
        self.dialog.addWidget(RaidWidget(self, request, isNew))
        self.dialog.resize(QSize(450, 200))

    def run(self):
        if self.dialog is None:
            return []

        while 1:
            rc = self.dialog.exec_()
            operations = []
            raidmembers = []

            if not rc:
                self.destroy()
                return []

            widget = self.dialog.content

            mountpoint = unicode(widget.mountpointMenu.currentText())
            active = widget.mountpointMenu.isEnabled()
            if active and mountpoint:
                msg = sanityCheckMountPoint(mountpoint)
                if msg:
                    self.intf.messageWindow(_("Mount Point Error"), msg,
                                            type="error")
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
                    self.intf.messageWindow(_("Mount point in use"),
                                            _("The mount point \"%s\" is in "
                                              "use. Please pick another.") %
                                            (mountpoint,),
                                            type="warning")
                    continue

            for index in range(widget.raidMembers.count()):
                if widget.raidMembers.item(index).checkState() == Qt.Checked:
                    raidmembers.append(widget.raidMembers.item(index).partition)

            # The user has to select some devices to be part of the array.
            if not raidmembers:
                raidlevel = widget.raidLevels.itemData(widget.raidLevels.currentIndex()).toInt()[0]
                self.intf.messageWindow(_("Invalid Raid Members"),
                                        _("A RAID%(level)d set requires at least %(min_member)d member")
                                        % {"level":raidlevel,
                                           "min_member":raid.get_raid_min_members(raidlevel)},
                                        type="warning")
                continue

            if not self.origrequest.exists:
                formatType = str(widget.filesystemMenu.currentText())
                raidminor = widget.raidMinors.itemData(widget.raidMinors.currentIndex()).toInt()[0]
                raidlevel = widget.raidLevels.itemData(widget.raidLevels.currentIndex()).toInt()[0]

                if not raid.isRaid(raid.RAID0, raidlevel):
                    spares = widget.spareSpin.value()
                else:
                    spares = 0

                format = formats.getFormat(formatType, mountpoint=mountpoint)
                members = len(raidmembers) - spares

                try:
                    request = self.storage.newRaidArray(minor=raidminor,
                                                        level=raidlevel,
                                                        format=format,
                                                        parents=raidmembers,
                                                        totalDevices=len(raidmembers),
                                                        memberDevices=members)
                except ValueError, msg:
                    self.intf.messageWindow(_("Invalid Raid Members"), unicode(msg),
                                            type="warning")
                    continue

                if not self.isNew:
                    # This may be handled in devicetree.registerAction,
                    # but not in case when we change minor and thus
                    # device name/path (at least with current md)
                    operations.append(OperationDestroyDevice(self.origrequest))

                operations.append(OperationCreateDevice(request))
                operations.append(OperationCreateFormat(request))

            else:
                format = None
                if widget.formatRadio.isChecked():
                    formatType = str(widget.formatCombo.currentText())
                    format = formats.getFormat(formatType, mountpoint=mountpoint, device=self.origrequest.path)
                    operations.append(OperationCreateFormat(self.origrequest, format))
                else:
                    cancel = []
                    cancel.extend(self.storage.devicetree.findOperations(type="destroy",
                                                                         object="format",
                                                                         devid=self.origrequest.id))
                    cancel.extend(self.storage.devicetree.findOperations(type="create",
                                                                         object="format",
                                                                         devid=self.origrequest.id))
                    for operation in cancel:
                        self.storage.devicetree.removeOperation(operation)

                    self.origrequest.format = self.origrequest.originalFormat

                if self.origrequest.format.mountable:
                    self.origrequest.format.mountpoint = mountpoint

                if widget.migrateRadio.isChecked():
                    operations.append(OperationMigrateFormat(self.origrequest))

                if self.origrequest.format.exists and not format and \
                   self.storage.formatByDefault(self.origrequest):
                    if not queryNoFormatPreExisting(self.intf):
                        continue

            # everything ok, fall out of loop
            break

        return operations

    def destroy(self):
        if self.dialog:
            self.dialog = None

class RaidWidget(QWidget, Ui_RaidWidget):
    def __init__(self, parent, request, isNew):
        QWidget.__init__(self, parent.parent)
        self.setupUi(self)
        self.parent = parent
        self.origrequest = request
        self.isNew = isNew

        if self.origrequest.exists:
            self.filesystemLabel.hide()
            self.filesystemMenu.hide()
        else:
            self.formatRadio.hide()
            self.formatCombo.hide()
            self.migrateRadio.hide()
            self.migrateCombo.hide()

        # Mountpoints
        storageGuiHelpers.fillMountpointMenu(self.mountpointMenu, self.origrequest)

        # Format options filesystems
        if not self.origrequest.exists:
            storageGuiHelpers.fillFilesystemMenu(self.filesystemMenu, self.origrequest.format,
                                                 ignores=["mdmember", "efi", "prepboot", "appleboot"])
            QObject.connect(self.filesystemMenu, SIGNAL("currentIndexChanged(int)"), self.formatTypeChanged)
        else:
            if self.origrequest.format.formattable or not self.origrequest.format.type:
                storageGuiHelpers.fillFilesystemMenu(self.formatCombo, self.origrequest.format,
                                                     ignores=["mdmember", "efi", "prepboot", "appleboot"])
                self.formatRadio.setChecked(self.origrequest.format.formattable and not self.origrequest.format.exists)
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

        # Raid Members
        availraidparts = self.parent.storage.unusedRaidMembers(array=self.origrequest)
        storageGuiHelpers.fillRaidMembers(self.raidMembers, availraidparts, self.origrequest.devices,
                                          self.origrequest.format)
        if self.origrequest.exists:
            self.raidMembers.setEnabled(False)

        # Raid Minors
        if not self.origrequest.exists:
            availminors = self.parent.storage.unusedRaidMinors[:16]
            if self.origrequest.minor is not None and self.origrequest.minor not in availminors:
                availminors.append(self.origrequest.minor)

            availminors.sort()
            storageGuiHelpers.fillRaidMinors(self.raidMinors, availminors, self.origrequest.minor)
        else:
            self.raidMinors.addItem(self.origrequest.name)
            self.raidMinors.setEnabled(0)

        # Raid Level
        if not self.origrequest.exists:
            storageGuiHelpers.fillRaidLevels(self.raidLevels, raid.raid_levels, self.origrequest.level)
        else:
            self.raidLevels.addItem(str(self.origrequest.level))
            self.raidLevels.setEnabled(0)

        QObject.connect(self.raidLevels, SIGNAL("currentIndexChanged(int)"), self.raidLevelChanged)

        # Raid Spares
        if not self.origrequest.exists:
            numparts =  len(availraidparts)
            if self.origrequest.spares:
                spares = self.origrequest.spares
            else:
                spares = 0

            if self.origrequest.level:
                maxspares = raid.get_raid_max_spares(self.origrequest.level, numparts)
            else:
                maxspares = 0

            self.spareSpin.setRange(0, maxspares)
            self.spareSpin.setValue(spares)

            if maxspares > 0:
                self.spareSpin.setEnabled(True)
            else:
                self.spareSpin.setEnabled(False)
                self.spareSpin.setValue(0)
        else:
            self.spareSpin.setValue(self.origrequest.spares)
            self.spareSpin.setEnabled(0)


        if self.origrequest.level is not None and self.origrequest.level == raid.RAID0:
            self.spareSpin.setEnabled(False)

        self.connect(self.buttonBox, SIGNAL("accepted()"), self.parent.dialog.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.parent.dialog.reject)

    def raidLevelChanged(self, index):
        raidlevel = self.raidLevels.itemData(index).toInt()[0]
        availraidparts = self.parent.storage.unusedRaidMembers(array=self.origrequest)
        maxspares = raid.get_raid_max_spares(raidlevel, len(availraidparts))

        if maxspares > 0 and not raid.isRaid(raid.RAID0, raidlevel):
           value = self.spareSpin.value()
           if value > maxspares:
               value = maxspares

           self.spareSpin.setRange(0, maxspares)
           self.spareSpin.setValue(value)
        else:
            self.spareSpin.setValue(0)
            self.spareSpin.setEnabled(False)


    def formatTypeChanged(self, index):
        format = formats.getFormat(str(self.sender().itemText(index)))
        if format.mountable:
            self.mountpointMenu.setEnabled(True)
        else:
            self.mountpointMenu.setEnabled(False)
            self.mountpointMenu.setCurrentIndex(0)
            #if self.mountpointMenu.findText(_("<Not Applicable>")) != -1:
            #    self.mountpointMenu.insertItem(0, _("<Not Applicable>"))
