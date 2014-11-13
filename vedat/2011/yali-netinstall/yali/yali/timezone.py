#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
import re
import string

class TimeZoneEntry:
    def __init__(self, code=None, timeZone=None):
        self.code = code
        self.timeZone = timeZone

class TimeZoneList:
    def __init__(self, fromFile='/usr/share/zoneinfo/zone.tab'):
        self.entries = []
        self.readTimeZone(fromFile)

    def getEntries(self):
        return self.entries

    def readTimeZone(self, fn):
        f = open(fn, 'r')
        comment = re.compile("^#")
        while 1:
            line = f.readline()
            if not line:
                break
            if comment.search(line):
                continue
            fields = string.split(line, '\t')
            if len(fields) < 3:
                continue
            code = fields[0]
            timeZone = string.strip(fields[2])
            entry = TimeZoneEntry(code, timeZone)
            self.entries.append(entry)
