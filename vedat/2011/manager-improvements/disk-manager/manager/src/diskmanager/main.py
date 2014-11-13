#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2011 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# UI
from diskmanager.ui_main import Ui_MainWidget

# Backend
from diskmanager.backend import Interface

# Pardus Diskutils
from pardus.diskutils import getPartitions

# Config
from diskmanager.config import ANIM_SHOW, ANIM_HIDE, ANIM_TARGET, ANIM_DEFAULT, ANIM_TIME

# Item widget
from diskmanager.item import ItemListWidgetItem, ItemWidget

# Edit widget
from diskmanager.pagedialog import PageDialog

# Pds vs Kde4 Stuff
import diskmanager.context as ctx

if ctx.Pds.session == ctx.pds.Kde4:
    from PyKDE4.kdeui import KIcon
    from PyKDE4.kdecore import i18n
else:
    from diskmanager.context import KIcon, i18n, KIconLoader

class MainWidget(QtGui.QWidget, Ui_MainWidget):
    def __init__(self, parent, embed=False):
        QtGui.QWidget.__init__(self, parent)

        if embed:
            self.setupUi(parent)
        else:
            self.setupUi(self)

        # Backend
        self.iface = Interface()
        self.iface.listenSignals(self.signalHandler)

        # Fail if no packages provide backend
        self.checkBackend()

        # Build item list
        self.buildItemList()

        # Get system partitions
        self._partitions = getPartitions()
        self._hidden_fss = ("swap")

    def checkBackend(self):
        """ Check if there are packages that provide required backend. """
        if not len(self.iface.getPackages()):
            QtGui.QMessageBox.critical(self, i18n("Error"), \
                                             i18n("There are no packages that provide \
                                                  backend for this application.\n \
                                                  Please make sure that packages \
                                                  are installed and configured correctly."))
            return False
        return True

    def clearItemList(self):
        """ Clears item list. """
        self.listItems.clear()

    def makeItemWidget(self, id_, title="", description="",diskUsage="",
                       type_=None, icon=None, state=None):
        """ Makes an item widget having given properties. """
        widget = ItemWidget(self.listItems, id_, title, \
                            description, diskUsage, type_, icon, state)

        self.connect(widget, QtCore.SIGNAL("stateChanged(int)"), \
                             self.slotItemState)
        self.connect(widget, QtCore.SIGNAL("editClicked()"), \
                             self.slotItemEdit)
        self.connect(widget, QtCore.SIGNAL("deleteClicked()"), \
                             self.slotItemDelete)

        return widget

    def addItem(self, id_, name="", description="", diskUsage="", mounted=False):
        """ Adds an item to list. """
        if mounted:
            if ctx.Pds.session == ctx.pds.Kde4:
                icon = KIcon("drive-harddisk", None, ["emblem-mounted"])
            else:
                icon = QtGui.QIcon(KIconLoader.loadOverlayed('drive-harddisk', ["emblem-mounted"], 32))
        else:
            icon = KIcon("drive-harddisk")

        type_ = "disk"

        # Build widget and widget item
        widget = self.makeItemWidget(id_, name, description, \
                                     diskUsage, type_, icon, mounted)
        widgetItem = ItemListWidgetItem(self.listItems, widget)

        # Delete is unnecessary
        widget.hideDelete()

        # Add to list
        self.listItems.setItemWidget(widgetItem, widget)

    def buildItemList(self):
        """ Builds item list. """
        # Clear list
        self.clearItemList()
        self.device_entries = {}
        self.mounted_devices = {}

        for entry in self.iface.entryList():
            self.device_entries[entry] = entry

        for device, path in self.iface.mountList():
            self.mounted_devices[device] = path

        def handleList(package, exception, args):
            if exception:
                pass
                # TODO: Handle exception
            else:
                devices = args[0]
                for device in devices:
                    parts = self.iface.partitionList(device)
                    parts = filter(lambda x: not self._partitions[x]["fstype"] in self._hidden_fss, parts)
                    parts.sort()
                    for part in parts:
                        if part in self.mounted_devices:
                            description = i18n("Mounted at %1", self.mounted_devices[part])
                            diskUsage = self.iface.calculateDiskUsage(self.mounted_devices[part].decode("string_escape"))
                            if diskUsage:
                                self.addItem(part, part, description, diskUsage, True)
                            else:
                                self.addItem(part, part, description, True)
                        else:
                            self.addItem(part, part, "")

        self.iface.deviceList(func=handleList)

    def slotItemState(self, state):
        """ Item state changed. """
        widget = self.sender()
        if state == QtCore.Qt.Checked:
            if widget.getId() not in self.iface.entryList():
                widget.pushEdit.animateClick(100)
                widget.setState(False)
                return
            path = self.iface.getEntry(widget.getId())[0]
            try:
                self.iface.mount(widget.getId(), path)
            except Exception, e:
                if "Comar.PolicyKit" in e._dbus_error_name:
                    QtGui.QMessageBox.critical(self, i18n("Error"), i18n("Access denied."))
                else:
                    QtGui.QMessageBox.critical(self, i18n("Error"), i18n("Error") + unicode(e)[unicode(e).find(":"):])
                widget.setState(False)
                return
        elif state == QtCore.Qt.Unchecked:
            try:
                self.iface.umount(widget.getId())
            except Exception, e:
                if "Comar.PolicyKit" in e._dbus_error_name:
                    QtGui.QMessageBox.critical(self, i18n("Error"), i18n("Access denied."))
                else:
                    QtGui.QMessageBox.critical(self, i18n("Error"), i18n("Error") + unicode(e)[unicode(e).find(":"):])
                widget.setState(True)
                return
        self.buildItemList()

    def slotItemEdit(self):
        """ Edit button clicked, show edit box. """
        widget = self.sender()

        dialog = PageDialog(self);

        if widget.getId() in self.device_entries:
            path, fsType, options = \
                    self.iface.getEntry(self.device_entries[widget.getId()])
            dialog.edit.setAutoMount(True)
            dialog.edit.setMountPoint(path)
            dialog.edit.setFilesystem(fsType)
            dialog.edit.setOptions(options)
        else:
            dialog.edit.setAutoMount(False)
            if widget.getId() in self.mounted_devices:
                dialog.edit.setMountPoint(self.mounted_devices[widget.getId()])
            dialog.edit.setFilesystem(self._partitions[widget.getId()]["fstype"])
            dialog.edit.slotResetOptions()

        if dialog.exec_():
            device = widget.getId()
            if widget.getId() in self.device_entries:
                device = self.device_entries[device]
            try:
                if dialog.edit.getAutoMount():
                    self.iface.addEntry(device, dialog.edit.getMountPoint(),
                            dialog.edit.getFilesystem(), dialog.edit.getOptions())
                else:
                    self.iface.removeEntry(device)
            except Exception, e:
                if "Comar.PolicyKit" in e._dbus_error_name:
                    QtGui.QMessageBox.critical(self, i18n("Error"), i18n("Access denied."))
                else:
                    QtGui.QMessageBox.critical(self, i18n("Error"), i18n("Error") + unicode(e)[unicode(e).find(":"):])

    def slotItemDelete(self):
        """ Delete button clicked. """
        widget = self.sender()

    def slotButtonStatusChanged(self, status):
        if status:
            self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        else:
            self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)

    def signalHandler(self, package, signal, args):
        self.buildItemList()

