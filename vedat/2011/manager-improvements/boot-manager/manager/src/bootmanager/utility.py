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

import os

def getDiskByUUID(uuid):
    if os.path.exists("/dev/disk/by-uuid/%s" % uuid):
        return os.path.realpath(os.path.join("/dev/disk/by-uuid/", os.readlink("/dev/disk/by-uuid/%s" % uuid)))
    else:
        return uuid
