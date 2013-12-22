#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import cmaketools
from pisi.actionsapi import get

shelltools.export("HOME", get.workDIR())
NoStrip=["/usr/share/icons"]

def setup():
    cmaketools.configure("-DCMAKE_INSTALL_PREFIX=`kde4-config --prefix=/usr`")
    
def build():
    cmaketools.make()

def install():
    cmaketools.install()