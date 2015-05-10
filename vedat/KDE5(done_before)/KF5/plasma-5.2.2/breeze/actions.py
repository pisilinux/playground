#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import cmaketools

def setup():
    cmaketools.configure("-DCMAKE_BUILD_TYPE=Release \
                          -DLIB_INSTALL_DIR=lib \
                          -DSYSCONF_INSTALL_DIR=/etc \
                          -DQML_INSTALL_DIR=/usr/lib/qt5/qml \
                          -DPLUGIN_INSTALL_DIR=/usr/lib/qt5/plugins \
                          -DPYTHON_EXECUTABLE=/usr/bin/python3 \
                          -DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
                          -DBUILD_TESTING=OFF \
                          -DECM_MKSPECS_INSTALL_DIR=/usr/lib/qt5/mkspecs/modules")

def build():
    cmaketools.make()

def install():
    cmaketools.install()
    
    pisitools.dodoc("COPYING")
