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
from appinfo import config
from appinfo import backends
from appinfo import database

# Utils
from appinfo.utils import update_sum

class AppInfo(object):
    """ AppInfo
        -------
        Package Management System indepented, package metadata
        information management system.

        Notes:
        ------
        - All methods returns a tuple which contains state of operation and
          state message (Boolean, Unicode)
        - Whole DB is built on sqlite3
        - Default database scheme described in database.py

    """

    def __getattribute__(self, name):
        if name in object.__getattribute__(self, '_dbcrm'):
            if not object.__getattribute__(self, '_sq'):
                return lambda *x:(False, 'Initialize a DB first')
        return object.__getattribute__(self, name)

    def __init__(self, pm):
        """ Initialize with given PMS (Package Management System) """

        if not pm in backends.known_pms:
            raise Exception('Selected PMS (%s) is not available yet.' % pm)

        # Database Connection Required Methods
        # Adding a method to this list, makes it in db connection check
        self._dbcrm = ['getPackagesFromDB', 'commitDB']

        self.config = config.Config()
        self._pm = backends.known_pms[pm]()
        self._sq = None
        self._db = None

    def initializeDB(self, db='appinfo.db', force = False):
        """ Initialize given database """

        def _check_table():
            try:
                return (u'packages',) in [x for x in \
                        self._sq.execute("SELECT name FROM sqlite_master "\
                                         "WHERE type IN ('table','view') "\
                                         "AND name NOT LIKE 'sqlite_%'")]
            except:
                return False

        if os.path.exists(db) or force:
            self._sq = sqlite3.connect(db)
            if _check_table():
                self._db = db
                return (True, 'DB Initialized sucessfuly.')
            else:
                self._sq = None
                self._db = None
                return (False, 'DB Initialized but tables are corrupted.')

        self._sq = None
        return (False, 'No such DB (%s).' % db)

    def getPackagesFromDB(self, fields = '*', condition = ''):
        """ Internal method to get package list from database """

        if condition:
            condition = ' WHERE %s' % condition
        try:
            return self._sq.execute('SELECT %s FROM %s%s' % \
                    (fields, database.PKG_TABLE, condition)).fetchall()
        except:
            return (False)

    def commitDB(self):
        """ Commit changes to DB """

        self._sq.commit()

        if self.config.updateSignAfterEachCommit:
            update_sum(self._db)

