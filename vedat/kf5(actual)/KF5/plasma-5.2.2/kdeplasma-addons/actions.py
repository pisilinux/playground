#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import cmaketools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    shelltools.makedirs("build")
    shelltools.cd("build")
    cmaketools.configure("-DCMAKE_BUILD_TYPE=Release \
                          -DSYSCONF_INSTALL_DIR=/etc \
                          -DLIB_INSTALL_DIR=lib \
                          -DQML_INSTALL_DIR=/usr/lib/qt5/qml \
                          -DPLUGIN_INSTALL_DIR=/usr/lib/qt5/plugins \
                          -DPYTHON_EXECUTABLE=/usr/bin/python3 \
                          -DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
                          -DECM_MKSPECS_INSTALL_DIR=/usr/lib/qt5/mkspecs/modules \
                          -DBUILD_TESTING=OFF", sourceDir="..")

def build():
    shelltools.cd("build")
    cmaketools.make()

def install():
    shelltools.cd("build")
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())

    
    
