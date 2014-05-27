#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import pisitools

WorkDir="omnitux-light"

KeepSpecial=["python"]  # do not remove .pyc files

def install():
    pisitools.insinto("/usr/share/omnitux","*")   
