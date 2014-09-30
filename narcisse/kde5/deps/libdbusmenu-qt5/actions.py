#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    cmaketools.configure("-DCMAKE_INSTALL_LIBDIR=lib \
                          -DUSE_QT5=ON \
                          -DCMAKE_DISABLE_FIND_PACKAGE_QJSON=TRUE \
                          ")

def build():
    shelltools.export("CFLAGS", "%s -DQT_NO_DEBUG -DQT_NO_DEBUG_OUTPUT -DQT_NO_WARNING_OUTPUT" %get.CFLAGS())
    shelltools.export("CXXFLAGS", "%s -DQT_NO_DEBUG -DQT_NO_DEBUG_OUTPUT -DQT_NO_WARNING_OUTPUT" %get.CXXFLAGS())    
    shelltools.export("LDFLAGS", "-Wl,-Bsymbolic-functions %s" %get.LDFLAGS())
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("COPYING", "NEWS", "README")
