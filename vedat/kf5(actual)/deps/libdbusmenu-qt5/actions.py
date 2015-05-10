#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    pisitools.ldflags.add("-Wl,-rpath,/usr/lib")
    cmaketools.configure("-DCMAKE_BUILD_TYPE=Release  \
                          -DCMAKE_INSTALL_PREFIX=/usr \
                          -DSYSCONF_INSTALL_DIR=/etc \
                          -DLIB_INSTALL_DIR=lib \
                          -DLIBEXEC_INSTALL_DIR=libexec \
                          -DCMAKE_INCLUDE_DIR=/usr/include \
                          -DCMAKE_INSTALL_LIBDIR=lib \
                          -DQML_INSTALL_DIR=/usr/lib/qt5/qml \
                          -DPYTHON_EXECUTABLE=/usr/bin/python3 \
                          -DLOCALE_INSTALL_DIR=/usr/share/locale \
                          -DECM_MKSPECS_INSTALL_DIR=/usr/lib/qt5/mkspecs/modules \
                          -DPLUGIN_INSTALL_DIR=/usr/lib/qt5/plugins \
                          -DUSE_QT5=ON \
                          -DBUILD_TESTING=OFF")

                          #-DCMAKE_DISABLE_FIND_PACKAGE_QJSON=TRUE \
def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("COPYING", "NEWS", "README")
