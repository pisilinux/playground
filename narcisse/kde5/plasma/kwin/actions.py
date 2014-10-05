#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import cmaketools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

shelltools.export("LDFLAGS", "%s -lwayland-cursor" %get.LDFLAGS())

def setup():
    cmaketools.configure("-DCMAKE_BUILD_TYPE=Release \
                          -DECM_MKSPECS_INSTALL_DIR=/usr/lib/qt5/mkspecs/modules \
                          -DLIB_INSTALL_DIR=lib \
                          -DSYSCONF_INSTALL_DIR=/etc \
                          -DBUILD_TESTING=OFF")

def build():
    cmaketools.make()

def install():
    cmaketools.install()
    
    pisitools.dodoc("COMPLIANCE", "CONFIGURING", "COPYING", "HACKING", "README")
    
