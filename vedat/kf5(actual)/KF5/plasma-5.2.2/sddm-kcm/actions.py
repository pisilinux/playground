#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import cmaketools

def setup():
    cmaketools.configure("-DCMAKE_INSTALL_PREFIX=/usr \
                          -DCMAKE_BUILD_TYPE=Release \
                          -DCMAKE_INSTALL_LIBEXECDIR=/usr/lib/sddm \
                          -DCMAKE_INSTALL_PREFIX=/usr \
                          -DLIB_INSTALL_DIR=lib \
                          -DLIBEXEC_INSTALL_DIR=lib \
                          -DPLUGIN_INSTALL_DIR=/usr/lib/qt5/plugins \
                          -DPYTHON_EXECUTABLE=/usr/bin/python3 \
                          -DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
                          -DBUILD_TESTING=OFF \
                          -DBUILD_MAN_PAGES=ON ")

def build():
    cmaketools.make()

def install():
    cmaketools.install()
    
    pisitools.dodoc("COPYING")
    
