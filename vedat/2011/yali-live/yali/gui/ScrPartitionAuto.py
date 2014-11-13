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
import gettext

_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL

import yali.context as ctx
from yali.gui import ScreenWidget
from yali.gui.Ui.autopartwidget import Ui_AutoPartWidget
from yali.gui.shrink_gui import ShrinkEditor
from yali.storage.partitioning import CLEARPART_TYPE_ALL, CLEARPART_TYPE_LINUX, CLEARPART_TYPE_NONE, doAutoPartition, defaultPartitioning

USE_ALL_SPACE, SHRINK_CURRENT, FREE_SPACE, CUSTOM = xrange(4)

class Widget(QWidget, ScreenWidget):
    name = "automaticPartitioning"

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_AutoPartWidget()
        self.ui.setupUi(self)
        self.storage = ctx.storage
        self.intf = ctx.interface
        self.connect(self.ui.autopartType, SIGNAL("currentRowChanged(int)"), self.typeChanged)

    def typeChanged(self, index):
        if index == SHRINK_CURRENT:
            resizable_partitions = [partition for partition in self.storage.partitions if partition.exists and
                                                                                         partition.resizable and
                                                                                         partition.format.resizable and
                                                                                         partition.size > ctx.consts.min_root_size]
            if not len(resizable_partitions):
                self.intf.messageWindow(_("Warning"),
                                        _("No partitions are available to resize. Only physical\n"
                                          "partitions which size is greater than %s MB can be resized.")
                                        % ctx.consts.min_root_size, type="warning")
                ctx.mainScreen.disableNext()
        else:
            ctx.mainScreen.enableNext()

    def setPartitioningType(self):
        if self.storage.clearPartType == CLEARPART_TYPE_NONE:
            self.ui.autopartType.setCurrentRow(FREE_SPACE)
        elif self.storage.clearPartType == CLEARPART_TYPE_ALL:
            self.ui.autopartType.setCurrentRow(USE_ALL_SPACE)

    def shown(self):
        if len(self.storage.clearPartDisks) > 1:
            self.ui.autopartType.item(USE_ALL_SPACE).setText(_("Use All Disks"))
        self.setPartitioningType()

    def execute(self):
        rc = self.nextCheck()
        if rc is None:
            # If return code from nextCheck method is None,
            # storage backend throws exceptions in doPartitioning method.
            ctx.mainScreen.enableBack()
            return False
        else:
            return rc

    def nextCheck(self):
        if self.ui.autopartType.currentRow() == CUSTOM:
            self.storage.clearPartType = CLEARPART_TYPE_NONE
            self.storage.doAutoPart = False
            #If user return back next screen or choose not permitted
            #option(like chosing free space installation however not
            #enough free space to install), we have to reset increment
            ctx.mainScreen.step_increment = 1
            return True
        else:
            self.storage.doAutoPart = True
            if self.ui.autopartType.currentRow() == SHRINK_CURRENT:
                shrinkeditor = ShrinkEditor(self, self.storage)
                rc, operations = shrinkeditor.run()
                if rc:
                    for operation in operations:
                        self.storage.devicetree.addOperation(operation)
                else:
                    return False
                self.storage.clearPartType = CLEARPART_TYPE_NONE
            elif self.ui.autopartType.currentRow() == USE_ALL_SPACE:
                self.storage.clearPartType = CLEARPART_TYPE_ALL
            elif self.ui.autopartType.currentRow() == FREE_SPACE:
                self.storage.clearPartType = CLEARPART_TYPE_NONE

            ctx.mainScreen.step_increment = 2
            self.storage.autoPartitionRequests = defaultPartitioning(self.storage,
                                                                     quiet=0,
                                                                     asVol=ctx.flags.partitioning_lvm)

            try:
                returncode = doAutoPartition(self.storage)
            except Exception, msg:
                ctx.logger.debug(msg)
                ctx.mainScreen.enableBack()
            else:
                return returncode

        return False


    def backCheck(self):
        disks = filter(lambda d: not d.format.hidden, ctx.storage.disks)
        if len(disks) == 1:
            ctx.mainScreen.step_increment = 2
        else:
            ctx.mainScreen.step_increment = 1

        return True


