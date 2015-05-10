#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import cmaketools

def setup():
      cmaketools.configure("-DCMAKE_BUILD_TYPE=Release \
                            -DCMAKE_INSTALL_PREFIX=/usr \
                            -DLIB_INSTALL_DIR=lib \
                            -DBUILD_TESTING=OFF \
                            -DCMAKE_SKIP_RPATH=ON \
                            -DSYSCONF_INSTALL_DIR=/etc \
                            -DQML_INSTALL_DIR=/usr/lib/qt5/qml \
                            -DPYTHON_EXECUTABLE=/usr/bin/python3 \
                            -DPLUGIN_INSTALL_DIR=/usr/lib/qt5/plugins ")

def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
    
    #pisitools.dodoc("AUTHORS", "NEWS", "README")
