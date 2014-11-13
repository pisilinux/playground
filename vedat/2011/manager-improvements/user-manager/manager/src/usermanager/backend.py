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

# DBus
import dbus

class Interface:
    def __init__(self):
        self.link = comar.Link()
        self.link.setLocale()
        self.link.useAgent()
        self.package = self.getMainPackage()

    def getPackages(self):
        """
            List of packages that provide User.Manager model
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
        return "baselayout"

    def userList(self, func=None):
        if func:
            self.link.User.Manager[self.package].userList(async=func)
        else:
            return self.link.User.Manager[self.package].userList()

    def groupList(self, func=None):
        if func:
            self.link.User.Manager[self.package].groupList(async=func)
        else:
            return self.link.User.Manager[self.package].groupList()

    def userInfo(self, uid, func=None):
        if func:
            self.link.User.Manager[self.package].userInfo(uid, async=func)
        else:
            return self.link.User.Manager[self.package].userInfo(uid)

    def deleteUser(self, uid, deleteFiles=False, func=None):
        if func:
            self.link.User.Manager[self.package].deleteUser(uid, deleteFiles, async=func)
        else:
            self.link.User.Manager[self.package].deleteUser(uid, deleteFiles)

    def deleteGroup(self, gid, func=None):
        if func:
            self.link.User.Manager[self.package].deleteGroup(gid, async=func)
        else:
            self.link.User.Manager[self.package].deleteGroup(gid)

    def addUser(self, uid, name, fullname, homedir, shell, password, groups, grants=[], blocks=[], func=None):
        if not grants:
            grants = dbus.Array([], "s")
        if not blocks:
            blocks = dbus.Array([], "s")
        if func:
            self.link.User.Manager[self.package].addUser(uid, name, fullname, homedir, shell, password, groups, grants, blocks, async=func)
        else:
            return self.link.User.Manager[self.package].addUser(uid, name, fullname, homedir, shell, password, groups, grants, blocks)

    def setUser(self, uid, fullname, homedir, shell, password, groups, func=None):
        if func:
            self.link.User.Manager[self.package].setUser(uid, fullname, homedir, shell, password, groups, async=func)
        else:
            self.link.User.Manager[self.package].setUser(uid, fullname, homedir, shell, password, groups)
            print " User id : %d" %uid 

    def addGroup(self, gid, name, func=None):
        if func:
            self.link.User.Manager[self.package].addGroup(gid, name, async=func)
        else:
            self.link.User.Manager[self.package].addGroup(gid, name)

    def getAuthorizations(self, uid, func=None):
        if func:
            self.link.User.Manager[self.package].listUserAuthorizations(uid, async=func)
        else:
            return self.link.User.Manager[self.package].listUserAuthorizations(uid)

    def setGrant(self, uid, action_id, func=None):
        if func:
            self.link.User.Manager[self.package].grantAuthorization(uid, action_id, async=func)
            print " Grant %s " %action_id
        else:
            return self.link.User.Manager[self.package].grantAuthorization(uid, action_id)

    def setRevoke(self, uid, action_id, func=None):
        if func:
            self.link.User.Manager[self.package].revokeAuthorization(uid, action_id, async=func)
        else:
            return self.link.User.Manager[self.package].revokeAuthorization(uid, action_id)

    def setBlock(self, uid, action_id, func=None):
        if func:
            self.link.User.Manager[self.package].blockAuthorization(uid, action_id, async=func)
            print " Block %s " %action_id
        else:
            return self.link.User.Manager[self.package].blockAuthorization(uid, action_id)
