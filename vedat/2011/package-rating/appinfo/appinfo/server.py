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
import sqlite3

# AppInfo Libs
from appinfo import database

# AppInfo Base Object
from appinfo.base import AppInfo

# Utils
from appinfo.utils import update_sum

class AppInfoServer(AppInfo):
    """ AppInfoServer
        -------------
        Server-side operations for AppInfo

        Notes:
        ------
        - All methods returns a tuple which contains state of operation and
          state message (Boolean, Unicode)
        - Whole DB is built on sqlite3
        - Default database scheme described in database.py

    """

    def __init__(self, pm = 'pisi'):
        AppInfo.__init__(self, pm)
        self._dbcrm.extend(['updatePackageList',
                            'updatePackageScore',
                            'resetPackageScores'])

    def createDB(self, db='appinfo.db', force=False):
        """ Create given database """

        if not force and os.path.exists(db):
            self.initializeDB(db)
            return (False, 'DB already exists.')

        if os.path.exists(db+'.backup'):
            os.unlink(db+'.backup')

        if os.path.exists(db):
            os.rename(db, db+'.backup')

        self._db = db
        self._sq = sqlite3.connect(db)
        self._sq.execute(database.DB_SCHEME)
        self.commitDB()
        return (True, 'DB created sucessfuly.')

    def updatePackageList(self):
        """ Merge packages in database with packages in PMS """

        packages_from_pms = self._pm.getPackageList()
        packages_from_db = [str(x[1]) for x in self.getPackagesFromDB()]
        new_packages = list(set(packages_from_pms) - set(packages_from_db))

        for package in new_packages:
            _sql = 'INSERT INTO %s (name, score, nose) VALUES (?,0,0)' % \
                    database.PKG_TABLE
            self._sq.execute(_sql, (package,) )

        self.commitDB()

        return (True, '%s package insterted.' % len(new_packages))

    def updatePackageScore(self, package, score):
        """ Update given packages score """

        # We accept 1-5
        score = min(5, max(score, 0.5))

        info = self.getPackagesFromDB(condition = "name = '%s'" % package)
        if info:
            self._sq.execute("UPDATE %s SET score = score + ? WHERE name = ?" % \
                    database.PKG_TABLE, (score, package,))
            self._sq.execute("UPDATE %s SET nose = nose + 1 WHERE name = ?" % \
                    database.PKG_TABLE, (package,))
            self.commitDB()

            return (True, self.getPackagesFromDB(condition = "name = '%s'" % \
                    package))
        return (False, 'Package %s does not exists' % package)

    def resetPackageScores(self, package = ''):
        """ Resets package scores
            WARNING ! If no package given it will resets all package scores """

        if package:
            package = " WHERE name = '%s'" % package

        self._sq.execute("UPDATE %s SET score = 0, nose = 0 %s" % \
                (database.PKG_TABLE, package,))
        self.commitDB()

        return (True, 'All scores reset.')


    def closeAndUpdateSum(self):
        """ It closes the db and updates db sum file """
        if self._sq:
            self._sq.close()
            update_sum(self._db)

