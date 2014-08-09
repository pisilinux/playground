#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import pythonmodules
#from pisi.actionsapi import pisitools

# if pisi can't find source directory, see /var/pisi/harman/work/ and:
WorkDir=""

def build():
    pythonmodules.compile()

def install():
    pythonmodules.install()

