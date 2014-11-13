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

from appinfo.server import AppInfoServer
from appinfo.client import AppInfoClient

if __name__ == '__main__':

    server = AppInfoServer()
    client = AppInfoClient()

    print
    print ' - Trying to create db:'
    print '   ',server.createDB()[1]
    print
    print ' - Trying to update packagelist:'
    print '   ', server.updatePackageList()[1]
    print
    print ' - Trying to initialize Client DB:'
    print '   ', client.initializeDB()[1]
    print
    print ' - Trying to get score for package "yali":'
    print '   ', client.getPackageScore('yali')
    print
    print ' - Trying to update package "yali" score:'
    print '   ', server.updatePackageScore('yali', 5)[1]
    print
    print ' - Trying to get score for package "yali":'
    print '   ', client.getPackageScore('yali')
    print
    print ' - Trying to reset package score:'
    print '   ', server.resetPackageScores('yali')[1]
    print
    print ' - Trying to get score for package "yali":'
    print '   ', client.getPackageScore('yali')
    print
    print ' - Get AppInfo Client dir:'
    print '   ', client.path
    print
    print ' - Remote Server Test'
    print '   ------------------'
    print
    print ' - Trying to set server as "http://cekirdek.pardus.org.tr/~gokmen/":'
    print '   ', client.setServer('http://cekirdek.pardus.org.tr/~gokmen/')
    print
    print ' - Trying to check out DB from server:'
    print '   ', client.checkOutDB()
    print
    print ' - Trying to get score for package "yali":'
    print '   ', client.getPackageScore('yali')
    print
    print ' - Trying to get score for package "package-manager":'
    print '   ', client.getPackageScore('package-manager')
    print
