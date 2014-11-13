#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# Comar
import comar

class Interface:
    def __init__(self):
        self.link = comar.Link()
        self.link.setLocale()
        self.link.useAgent()
        self.package = self.getMainPackage()

    def listenSignals(self, func):
        self.link.listenSignals("Boot.Loader", func)

    def getPackages(self):
        """
            List of packages that provide Boot.Manager model
        """
        return list(self.link.User.Manager)

    def getMainPackage(self):
        """
            Package that's selected by system.
            For now, it's hardcoded. This value should be given by COMAR.
        """
        packages = self.getPackages()
        if not len(packages):
            return None
        return "grub"

    def getSystems(self, func=None):
        if func:
            self.link.Boot.Loader[self.package].listSystems(async=func)
        else:
            return self.link.Boot.Loader[self.package].listSystems()

    def getEntries(self, func=None):
        if func:
            self.link.Boot.Loader[self.package].listEntries(async=func)
        else:
            return self.link.Boot.Loader[self.package].listEntries()

    def getOptions(self, func=None):
        if func:
            self.link.Boot.Loader[self.package].getOptions(async=func)
        else:
            return self.link.Boot.Loader[self.package].getOptions()

    def setOption(self, option, value, func=None):
        if func:
            self.link.Boot.Loader[self.package].setOption(option, value, async=func)
        else:
            self.link.Boot.Loader[self.package].setOption(option, value)

    def removeEntry(self, index, title, uninstall=False, func=None):
        index = int(index)
        if func:
            self.link.Boot.Loader[self.package].removeEntry(index, title, uninstall, async=func)
        else:
            self.link.Boot.Loader[self.package].removeEntry(index, title, uninstall)

    def setEntry(self, title, os_type, root="", kernel="", initrd="", options="", default="no", index=-1, func=None):
        if func:
            self.link.Boot.Loader[self.package].setEntry(title, os_type, root, kernel, initrd, options, default, index, async=func)
        else:
            self.link.Boot.Loader[self.package].setEntry(title, os_type, root, kernel, initrd, options, default, index)
