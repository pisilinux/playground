#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import hashlib

def update_sum(db):
    open('%s.md5' % db, 'w').write(hashlib.md5(open(db).read()).hexdigest())

