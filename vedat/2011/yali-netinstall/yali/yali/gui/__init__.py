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
import yali
import yali.context as ctx

class GUIError(yali.Error):
    pass


GUI_STEPS = {ctx.STEP_DEFAULT:("license", "mediaCheck", "keyboardSetup",
                               "timeSetup", "accounts", "admin", "driveSelection",
                               "automaticPartitioning", "manualPartitioning", "bootloadersetup",
                               "collectionSelection", "summary", "packageInstallation", "goodbye"),
             ctx.STEP_BASE:("license", "mediaCheck", "keyboardSetup",
                            "timeSetup", "driveSelection", "automaticPartitioning",
                            "manualPartitioning", "bootloadersetup", "collectionSelection",
                            "summary", "packageInstallation", "goodbye"),
             ctx.STEP_OEM_INSTALL:("license", "mediaCheck", "keyboardSetup", "driveSelection",
                                   "automaticPartitioning", "manualPartitioning", "bootloadersetup",
                                   "collectionSelection", "summary", "packageInstallation", "goodbye"),
             ctx.STEP_FIRST_BOOT:("welcome", "accounts", "admin", "summary", "goodbye"),
             ctx.STEP_RESCUE:("rescue", "bootloadersetup", "passwordRescue", "goodbye")}

stepToClass = {"license":"ScrLicense",
               "network":"ScrNetwork",
               "welcome":"ScrWelcome",
               "mediaCheck":"ScrCheckCD",
               "keyboardSetup":"ScrKeyboard",
               "timeSetup":"ScrDateTime",
               "accounts":"ScrUsers",
               "admin":"ScrAdmin",
               "driveSelection":"ScrDriveSelection",
               "automaticPartitioning":"ScrPartitionAuto",
               "manualPartitioning":"ScrPartitionManual",
               "bootloadersetup":"ScrBootloader",
               "collectionSelection":"ScrCollection",
               "summary":"ScrSummary",
               "packageInstallation":"ScrInstall",
               "goodbye":"ScrGoodbye",
               "rescue":"ScrRescue",
               "passwordRescue":"ScrRescuePassword"
               }

class ScreenWidget:
    _id = 0
    title = ""
    name = ""
    help = ""
    icon = None

    def __init__(self):
        self._id = ScreenWidget._id
        ScreenWidget._id += 1

    def shown(self):
        pass

    def execute(self):
        return True

    def nextCheck(self):
        """Calling when Screen nextButton clicked"""
        return True

    def backCheck(self):
        """Calling when Screen backButton clicked"""
        return True

