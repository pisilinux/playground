#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    cmaketools.configure("-DCMAKE_BUILD_TYPE=Release \
                          -DCMAKE_INSTALL_PREFIX=/usr \
                          -DSYSCONF_INSTALL_DIR=/etc \
                          -DPLUGIN_INSTALL_DIR=/usr/lib/qt5/plugins \
                          -DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
                          -DLIB_INSTALL_DIR=lib \
                          -DPYTHON_EXECUTABLE=/usr/bin/python3 ")

def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("COPYING", "README")
