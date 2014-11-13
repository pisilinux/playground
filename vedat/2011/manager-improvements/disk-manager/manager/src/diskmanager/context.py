#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2011 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import pds
from pds.qiconloader import QIconLoader

Pds = pds.Pds('disk-manager', debug = False)

i18n = Pds.i18n
KIconLoader = QIconLoader(Pds, forceCache=True)
KIcon = KIconLoader.icon

