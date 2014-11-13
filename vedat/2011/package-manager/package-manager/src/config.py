#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyKDE4.kdecore import KConfig
from PyQt4.Qt import QVariant

defaults = {
            "SystemTray" : False,
            "UpdateCheck" : False,
            "InstallUpdatesAutomatically" : False,
            "UpdateCheckInterval" : 60,
           }

GROUP = "General"
DATA_DIR = '/usr/share/kde4/apps/package-manager/data/'

class Config:
    def __init__(self, config):
        self.config = KConfig(config)
        self.group = None

    def setValue(self, option, value):
        self.group = self.config.group(GROUP)
        self.group.writeEntry(option, QVariant(value))
        self.config.sync()

    def getBoolValue(self, option):
        default = self._initValue(option, False)
        return self.group.readEntry(option, QVariant(default)).toBool()

    def getNumValue(self, option):
        default = self._initValue(option, 0)
        return self.group.readEntry(option, QVariant(default)).toInt()[0]

    def _initValue(self, option, value):
        self.group = self.config.group(GROUP)
        if defaults.has_key(option):
            return defaults[option]
        return value

class PMConfig(Config):
    def __init__(self):
        Config.__init__(self, "package-managerrc")

    def showOnlyGuiApp(self):
        return self.getBoolValue("ShowOnlyGuiApp")

    def showComponents(self):
        return self.getBoolValue("ShowComponents")

    def showIsA(self):
        return self.getBoolValue("ShowIsA")

    def updateCheck(self):
        return self.getBoolValue("UpdateCheck")

    def installUpdatesAutomatically(self):
        return self.getBoolValue("InstallUpdatesAutomatically")

    def updateCheckInterval(self):
        return self.getNumValue("UpdateCheckInterval")

    def hideTrayIfThereIsNoUpdate(self):
        return self.getBoolValue("HideTrayIfThereIsNoUpdate")

    def systemTray(self):
        return self.getBoolValue("SystemTray")

    def setHideTrayIfThereIsNoUpdate(self, enabled):
        self.setValue("HideTrayIfThereIsNoUpdate", enabled)

    def setSystemTray(self, enabled):
        self.setValue("SystemTray", enabled)

    def setUpdateCheck(self, enabled):
        self.setValue("UpdateCheck", enabled)

    def setInstallUpdatesAutomatically(self, enabled):
        self.setValue("InstallUpdatesAutomatically", enabled)

    def setUpdateCheckInterval(self, value):
        self.setValue("UpdateCheckInterval", value)

    def setShowOnlyGuiApp(self, enabled):
        self.setValue("ShowOnlyGuiApp", enabled)

    def setShowComponents(self, enabled):
        self.setValue("ShowComponents", enabled)

    def setShowIsA(self, enabled):
        self.setValue("ShowIsA", enabled)

