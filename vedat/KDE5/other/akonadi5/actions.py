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
                            -DPLUGIN_INSTALL_DIR=/usr/lib/qt5/plugins \
                            -DDATABASE_BACKEND=SQLITE \
                            -DKDE_INSTALL_USE_QT_SYS_PATHS=ON")

def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
    
    pisitools.dodoc("AUTHORS", "NEWS", "README")
