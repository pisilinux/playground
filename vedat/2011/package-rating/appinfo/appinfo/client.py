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

# Python Libs
import os
import math
import shutil

# Python URL Libs
import urlgrabber

# AppInfo Base Object
from appinfo.base import AppInfo

# Utils
from appinfo.utils import update_sum

DB_FILE = 'appinfo.db'
DB_FILE_SUM = DB_FILE + '.md5'

class AppInfoClient(AppInfo):
    """ AppInfoClient
        -------------
        Client-side operations for AppInfo

        Notes:
        ------
        - Whole DB is built on sqlite3
        - Default database scheme described in database.py

    """

    def __init__(self, pm = 'pisi', server = None, path = None):
        AppInfo.__init__(self, pm)
        self._dbcrm.extend(['getPackageId',
                            'getPackagesFromDB'])

        if not path:
            path = os.path.join(os.getenv('HOME'), '.appinfo')

        self.path = path

        self.setServer(server)

        # Local files full paths
        self.local_db = os.path.join(self.path, DB_FILE)
        self.local_db_sum = os.path.join(self.path, DB_FILE_SUM)

    def getPackageScore(self, package):
        """ Returns given package calculated score:
            Where score = score / nose """

        if not self._sq:
            return 0

        info = self.getPackagesFromDB(condition = "name = '%s'" % package)

        if info:
            if info[0][2] == 0 and info[0][3] == 0:
                return 0
            return float(max(1,info[0][2])) / float(max(1,info[0][3]))))
        return 0

    def getPackageId(self, package):
        """ Returns given package db id """

        info = self.getPackagesFromDB("id", condition = "name = '%s'" % \
                package)
        if info:
            return info[0][0]

    def setServer(self, server):
        """ AppInfo Server address """

        if not server:
            local_server = os.path.join(self.path, 'server')
            if os.path.exists(local_server):
                server = open(local_server).read().strip('\n')

        if server:
            self.server = server

            # Get remote db full paths
            self.remote_db = os.path.join(self.server, DB_FILE)
            self.remote_db_sum = os.path.join(self.server, DB_FILE_SUM)

            self.createSkeleton()
            return True

        self.server = None

    def createSkeleton(self, force = False):
        """ Creates skeleton directories for AppInfo Client """

        if os.path.exists(self.path) and force:
            shutil.rmtree(self.path)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        if self.server:
            open(os.path.join(self.path, 'server'), 'w').write(self.server)

    def checkOutDB(self, initialize = True, force = False):
        """ Checkouts rating db from selected server """

        if not self.server:
            return (False, 'No server defined')

        def updateLocalSum():
            if os.path.exists(self.local_db):
                update_sum(self.local_db)

        self.createSkeleton()
        updateLocalSum()

        def updateLocalDb():
            try:
                if urlgrabber.urlgrab(self.remote_db, self.local_db) == self.local_db:
                    updateLocalSum()
                    return True
            except urlgrabber.grabber.URLGrabError:
                return False

        def getRemoteSum():
            try:
                return urlgrabber.urlread(self.remote_db_sum).split()[0]
            except urlgrabber.grabber.URLGrabError:
                return ''

        is_local_file_old = True

        if not os.path.exists(self.local_db) or force:
            if not updateLocalDb():
                return (False, 'File is not reachable: %s' % self.remote_db)
        else:
            if not os.path.exists(self.local_db_sum):
                updateLocalSum()

            if open(self.local_db_sum).read().startswith(getRemoteSum()):
                is_local_file_old = False

            if is_local_file_old:
                if not updateLocalDb():
                    return (False, 'File is not reachable: %s' % self.remote_db)

        if initialize:
            self.initializeLocalDB()

        if not is_local_file_old:
            return (True, 'DB is up-to date.')

        return (True, 'DB updated succesfully.')

    def initializeLocalDB(self):
        """ Just a wrapper to initialize local db """
        if not self.server:
            return (False, 'No server defined')

        return self.initializeDB(self.local_db)

