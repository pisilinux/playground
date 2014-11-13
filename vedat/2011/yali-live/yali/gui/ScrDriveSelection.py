# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
import sys
import math
import gettext

_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL, QObject, QListWidgetItem, QSize, QPixmap

import yali.context as ctx
from yali.gui import ScreenWidget, GUIError
from yali.gui.Ui.driveselectionwidget import Ui_DriveSelectionWidget
from yali.gui.Ui.partitionshrinkwidget import Ui_PartShrinkWidget
from yali.gui.Ui.diskItem import Ui_DiskItem
from yali.storage.operations import OperationResizeDevice, OperationResizeFormat
from yali.storage.formats.filesystem import FilesystemError

class DrivesListItem(QListWidgetItem):
    def __init__(self, parent, widget):
        QListWidgetItem.__init__(self, parent)
        self.widget = widget
        self.setSizeHint(QSize(widget.width()-20, widget.height()))

class DriveItem(QWidget, Ui_DiskItem):
    def __init__(self, parent, drive, name):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        if drive.removable:
            self.icon.setPixmap(QPixmap(":/gui/pics/drive-removable-media-usb-big.png"))
        elif drive.name.startswith("mmc"):
            self.icon.setPixmap(QPixmap(":/gui/pics/media-flash-sd-mmc-big.png"))
        else:
            self.icon.setPixmap(QPixmap(":/gui/pics/drive-harddisk-big.png"))
        self.labelDrive.setText("%s" % (name))
        self.labelInfo.setText("%s\n%s GB" % (drive.model, str(int(drive.size) / 1024)))


class Widget(QWidget, ScreenWidget):
    name = "driveSelection"

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_DriveSelectionWidget()
        self.ui.setupUi(self)
        self.storage = None
        self.intf = None
        self.shrink_operations = None
        self.clear_partdisks = None
        self.selected_disks = []

        self.useAllSpace, self.replaceExistingLinux, self.shrinkCurrent, self.useFreeSpace, self.createCustom = range(5)
        self.connect(self.ui.drives, SIGNAL("itemSelectionChanged()"), self.itemStateChanged)

    def itemStateChanged(self):
        self.selected_disks = []

        for item in self.ui.drives.selectedItems():
            self.selected_disks.append(str(item.statusTip()))

        self.selected_disks.sort(self.storage.compareDisks)

        if len(self.selected_disks):
            ctx.mainScreen.enableNext()
        else:
            ctx.mainScreen.disableNext()

    def fillDrives(self):
        disks = filter(lambda d: not d.format.hidden, self.storage.disks)
        self.ui.drives.clear()

        count = 1
        for disk in disks:
            if disk.size >= ctx.consts.min_root_size:
                # GUI Hack
                if len(disks) <= 4:
                    self.ui.drives.setMinimumWidth(150 * len(disks))
                    self.ui.drives.setMaximumWidth(150 * len(disks))
                else:
                    self.ui.drives.setMinimumWidth(600)
                    self.ui.drives.setMaximumWidth(600)

                name = "Disk %s" % count
                drive = DriveItem(self.ui.drives, disk, name)
                item = DrivesListItem(self.ui.drives, drive)
                item.setStatusTip(disk.name)
                item.setToolTip(_("Device Path: %s") % (disk.name))
                self.ui.drives.setGridSize(QSize(drive.width(), drive.height()))
                self.ui.drives.setItemWidget(item, drive)

            count += 1
        # select the first disk by default
        self.ui.drives.setCurrentRow(0)

    def shown(self):
        self.storage = ctx.storage
        self.intf = ctx.interface
        self.fillDrives()

    def nextCheck(self):

        if len(self.selected_disks) == 0:
            self.intf.messageWindow(_("Error"),
                                    _("You must select at least one "
                                      "drive to be used for installation."), type="error")
            return False
        else:
            self.selected_disks.sort(self.storage.compareDisks)
            self.storage.clearPartDisks = self.selected_disks
            return True

    def execute(self):
        return self.nextCheck()


