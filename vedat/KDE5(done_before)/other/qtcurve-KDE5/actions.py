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
		          -DENABLE_GTK2=false \
		          -DQTC_QT5_ENABLE_KDE=true \
                          -DQTC_QT4_ENABLE_KDE=false \
                          -DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
                          -DPLUGIN_INSTALL_DIR=/usr/lib/qt5/plugins \
                          -DPYTHON_EXECUTABLE=/usr/bin/python3 \
                          -DECM_MKSPECS_INSTALL_DIR=/usr/lib/qt5/mkspecs/modules \
                          -DBUILD_TESTING=OFF")

def build():
    cmaketools.make()

def install():
    cmaketools.install()
    
    pisitools.dodoc("README.md", "COPYING", "AUTHORS", "TODO.md")
