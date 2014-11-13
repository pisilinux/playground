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
from diskmanager.ui_edit import Ui_EditWidget

# FS Options
from diskmanager.config import FS_TYPES, FS_OPTIONS

# Pds Stuff
import context as ctx

class EditWidget(QtGui.QWidget, Ui_EditWidget):

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        # Build filesystems
        self.buildFilesystems()

        self.connect(self.pushOptions, QtCore.SIGNAL("clicked()"), self.slotResetOptions)
        self.connect(self.comboFilesystem, QtCore.SIGNAL("activated(int)"), self.slotChangeOptions)

    def slotResetOptions(self):
        index = self.comboFilesystem.currentIndex()
        fsname = unicode(self.comboFilesystem.itemData(index).toString())
        options = FS_OPTIONS.get(fsname, "")
        self.lineOptions.setText(unicode(options))

    def slotChangeOptions(self, index):
        if len(self.lineOptions.text()) or self.lineOptions.isModified():
            return
        self.slotResetOptions()

    def buildFilesystems(self):
        for fsname, fslabel in FS_TYPES.iteritems():
            self.comboFilesystem.addItem(fslabel, QtCore.QVariant(fsname))

    def setAutoMount(self, mount):
        self.groupMount.setChecked(mount)

    def getAutoMount(self):
        return self.groupMount.isChecked()

    def setMountPoint(self, path):
        self.lineMountPoint.setText(unicode(path))

    def getMountPoint(self):
        return unicode(self.lineMountPoint.text())

    def setFilesystem(self, fsname):
        index = self.comboFilesystem.findData(QtCore.QVariant(fsname))
        if index == -1:
            self.comboFilesystem.addItem(fsname, QtCore.QVariant(fsname))
            self.comboFilesystem.setCurrentIndex(self.comboFilesystem.count() - 1)
        else:
            self.comboFilesystem.setCurrentIndex(index)

    def getFilesystem(self):
        index = self.comboFilesystem.currentIndex()
        return unicode(self.comboFilesystem.itemData(index).toString())

    def setOptions(self, options):
        self.lineOptions.setText(unicode(options))

    def getOptions(self):
        return unicode(self.lineOptions.text())

