#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import cmaketools

def setup():
    pisitools.ldflags.add("-Wl,-rpath,/usr/lib")
    cmaketools.configure("-DCMAKE_BUILD_TYPE=Release \
                          -DLIB_INSTALL_DIR=lib \
                          -DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
                          -DPYTHON_EXECUTABLE=/usr/bin/python3 \
                          -DPLUGIN_INSTALL_DIR=/usr/lib/qt5/plugins \
                          -DECM_MKSPECS_INSTALL_DIR=/usr/lib/qt5/mkspecs/modules \
                          -DBUILD_TESTING=OFF")

def build():
    cmaketools.make()

def install():
    cmaketools.install()
    
    pisitools.dodoc("README.md", "COPYING.LIB", "ISSUES")
