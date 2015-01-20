# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
import sys
import os
import gettext
_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL, QListWidgetItem, QIcon

import yali.storage
import yali.util
import yali.context as ctx
from yali.gui import ScreenWidget
from yali.gui.Ui.rescuewidget import Ui_RescueWidget

class Widget(QWidget, Ui_RescueWidget, ScreenWidget):
    name = "rescue"

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.rescueSystems.setEnabled(False)
        self.rescueSystems.currentItemChanged.connect(self.rescueItemChanged)
        self.rescuePisi.hide()

    def shown(self):
        ctx.mainScreen.disableBack()
        ctx.mainScreen.disableNext()
        self.initializeStorage()
        if not ctx.installData.rootDevs:
            self.scanRescueSystems()
            if len(ctx.installData.rootDevs) == 1:
                self.rescueSystems.setCurrentRow(0)
                self.rescueSystems.setEnabled(False)
        else:
            ctx.mainScreen.enableNext()

    def nextCheck(self):
        active = ctx.storage.storageset.active
        if not active:
            try:
                active = yali.storage.mountExistingSystem(ctx.storage, ctx.interface, ctx.installData.rescueRoot, allowDirty=0)
            except ValueError as e:
                ctx.logger.error("Error mounting filesystem: %s" % e)
                ctx.interface.messageWindow(_("Mount failed"),
                                            _("The following error occurred when mounting the file "
                                              "systems listed in /etc/fstab.  Please fix this problem "
                                              "and try to rescue again.\n%s" % e))
                active = False

        return active

    def execute(self):
        if self.nextCheck():
            if self.rescuePisi.isChecked():
                ctx.installData.rescueMode = ctx.RESCUE_PISI
            elif self.rescuePassword.isChecked():
                ctx.installData.rescueMode = ctx.RESCUE_PASSWORD
            elif self.rescueGrub.isChecked():
                ctx.installData.rescueMode = ctx.RESCUE_GRUB

            ctx.mainScreen.step_increment += ctx.installData.rescueMode
            ctx.logger.debug("Selected system for rescue is %s" % ctx.installData.rescueRoot.path)
            return True
        else:
            return False

    def rescueItemChanged(self, current, previous):
        if current and current.device:
            ctx.installData.rescueRoot = current.device
        if not ctx.mainScreen.isNextEnabled():
            ctx.mainScreen.enableNext()

    def initializeStorage(self):
        if not ctx.storageInitialized:
            ctx.storageInitialized = yali.storage.initialize(ctx.storage, ctx.interface)

    def scanRescueSystems(self):
        if ctx.installData.rootDevs is None:
            ctx.installData.rootDevs = yali.storage.findExistingRootDevices(ctx.storage)

            if not ctx.installData.rootDevs:
                rc = ctx.interface.messageWindow(_("Cannot Rescue"),
                                                 _("Your current installation cannot be rescued."),
                                                 type="custom", customIcon="error",
                                                 customButtons=[_("Exit"), _("Continue")])
                if rc == 0:
                    sys.exit(0)
                else:
                    ctx.mainScreen.disableNext()
            else:
                self.rescueSystems.clear()
                self.rescueSystems.setEnabled(True)
                for device, release in ctx.installData.rootDevs:
                    RescueSystem(self.rescueSystems, device, release)

class RescueSystem(QListWidgetItem):
    def __init__(self, parent, device, release):
        label = "%s on %s" % (release, device.path)
        QListWidgetItem.__init__(self, QIcon(":/gui/pics/parduspart.png"), label, parent)
        self.device = device
        self.release = release
