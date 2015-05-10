#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import cmaketools

def setup():
    cmaketools.configure("-DCMAKE_BUILD_TYPE=Release \
                          -DCMAKE_INSTALL_PREFIX=/usr \
                          -DECM_MKSPECS_INSTALL_DIR=/usr/lib/qt5/mkspecs/modules \
                          -DQML_INSTALL_DIR=lib/qt5/qml \
                          -DLIB_INSTALL_DIR=lib \
                          -DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
                          -DPYTHON_EXECUTABLE=/usr/bin/python3 \
                          -DPLUGIN_INSTALL_DIR=/usr/lib/qt5/plugins \
                          -DBUILD_TESTING=OFF")

###later think: 
                          #-DWITH_NEW_SOLID_JOB=ON \
                          #-DWITH_NEW_POWER_ASYNC_API=ON \
def build():
    cmaketools.make()

def install():
    cmaketools.install()
    
    pisitools.dodoc("README.md","COPYING.LIB", "TODO")
