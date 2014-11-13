#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import pisi

class Backend:

    def __init__(self):
        self.name = 'pisi'
        self.packagedb = pisi.db.packagedb.PackageDB()
        self.installdb = pisi.db.installdb.InstallDB()

    def getPackageList(self):
        return pisi.api.list_available()

    def getPackageInfo(self, pkg_name):
        if self.packagedb.has_package(pkg_name):
            package = self.packagedb.get_package(pkg_name)
            return {'name':package.name,
                    'homepage':package.source.homepage,
                    'icon':package.icon,
                    'license':','.join(package.license),
                    'packager.name':package.source.packager.name,
                    'packager.email':package.source.packager.email}

    def getPackageFiles(self, pkg_name):
        if self.installdb.has_package(pkg_name):
            return map(lambda x:'/'+x.path, pisi.api.info('qt', True)[1].list)

