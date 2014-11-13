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

# PyQt stuff
from PyQt4 import QtCore
from PyQt4 import QtGui

# UI
from bootmanager.ui_edit import Ui_EditWidget

# PDS stuff
import bootmanager.context as ctx

if ctx.Pds.session == ctx.pds.Kde4:
    from PyKDE4.kdeui import KIcon
    from PyKDE4.kdecore import i18n
else:
    from bootmanager.context import KIcon, i18n

class EditWidget(QtGui.QWidget, Ui_EditWidget):

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.id = None
        self.type = None

        # Kernel button signal connect
        self.kernelButton.clicked.connect(self.slotFileDialog)
        self.kernelButton.setIcon(KIcon("folder"))

        # Ramdisk button signal connect
        self.ramdiskButton.clicked.connect(self.slotRamDialog)
        self.ramdiskButton.setIcon(KIcon("folder"))

    def isNew(self):
        return self.id == None

    def reset(self):
        self.id = None
        self.type = None
        self.setTitle("")
        self.setDisk("")
        self.setKernel("")
        self.setRamdisk("")
        self.setOptions("")
        self.showTitle()
        self.showDisk()
        self.showKernel()
        self.showRamdisk()
        self.showOptions()

    def setId(self, id_):
        self.id = id_

    def getId(self):
        return self.id

    def setType(self, type_):
        self.type_ = type_

    def getType(self):
        return self.type_

    def hideTitle(self):
        self.lineTitle.setEnabled(False)

    def showTitle(self):
        self.lineTitle.setEnabled(True)

    def hideDisk(self):
        self.widgetDisk.hide()

    def showDisk(self):
        self.widgetDisk.show()

    def hideKernel(self):
        self.widgetKernel.hide()

    def showKernel(self):
        self.widgetKernel.show()

    def hideOptions(self):
        self.widgetOptions.hide()

    def showOptions(self):
        self.widgetOptions.show()

    def hideRamdisk(self):
        self.widgetRamdisk.hide()

    def showRamdisk(self):
        self.widgetRamdisk.show()

    def setTitle(self, title):
        self.lineTitle.setText(unicode(title))

    def getTitle(self):
        return unicode(self.lineTitle.text())

    def setDisk(self, disk):
        self.lineDisk.clear()
        if type(disk) == list:
            self.lineDisk.addItem('')
            self.lineDisk.addItems(disk)
        else:
            self.lineDisk.addItem(unicode(disk))

    def getDisk(self):
        return unicode(self.lineDisk.currentText())

    def setKernel(self, kernel):
        self.lineKernel.setText(unicode(kernel))

    def getKernel(self):
        return unicode(self.lineKernel.text())

    def setRamdisk(self, ramdisk):
        self.lineRamdisk.setText(unicode(ramdisk))

    def getRamdisk(self):
        return unicode(self.lineRamdisk.text())

    def setOptions(self, options):
        self.lineOptions.setText(unicode(options))

    def getOptions(self):
        return unicode(self.lineOptions.text()).replace('\n', ' ')

    # Get file name from file dialog
    def slotFileDialog(self):
        """
            Get file name from file dialog
        """

        if ctx.Pds.session == ctx.pds.Kde4:
            from PyKDE4.kio import KFileDialog
            from PyKDE4.kdecore import KUrl
            url=KUrl.fromPath("/boot/")
            filename=unicode(KFileDialog.getOpenFileName(url, "", self, i18n("File System")))
        else:
            filename=unicode(QtGui.QFileDialog.getOpenFileName(self, i18n("File System"), "/boot/"))

        if filename:
            self.setFile(filename)

    def setFile(self,filename):
        """
            Set file name
        """
        EditWidget.setKernel(self,filename)

    def slotRamDialog(self):
        """
            Get file name from RamFile dialog
        """

        # Set ram name
        if ctx.Pds.session == ctx.pds.Kde4:
            from PyKDE4.kio import KFileDialog
            from PyKDE4.kdecore import KUrl
            url=KUrl.fromPath("/boot/")
            ramname=unicode(KFileDialog.getOpenFileName(url, "", self, i18n("File System")))
        else:
            ramname=unicode(QtGui.QFileDialog.getOpenFileName(self, i18n("File System"), "/boot/"))

        if ramname:
            self.setRam(ramname)

    def setRam(self,ramname):
        EditWidget.setRamdisk(self,ramname)

