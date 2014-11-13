#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/BILGEM
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# (See COPYING)

import gettext

__trans = gettext.translation("quickformat", fallback=True)

def i18n(*text):
    "Needs for internationalization"
    if len(text) == 1:
        return __trans.ugettext(text[0])
    ttt = unicode(__trans.ugettext(text[0]))
    for i in range(1,len(text)):
        ttt = ttt.replace('%%%d' % i, unicode(text[i]))
    return ttt

