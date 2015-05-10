#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import cmaketools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get
import os

def setup(): 
    #if not os.path.exists("akonadi-calendar"):
        #shelltools.system("git clone git://anongit.kde.org/akonadi-calendar.git")
    #shelltools.cd("akonadi-calendar")
    cmaketools.configure("-DCMAKE_BUILD_TYPE=Release \
                          -DECM_MKSPECS_INSTALL_DIR=/usr/lib/qt5/mkspecs/modules \
                          -DQT_PLUGIN_INSTALL_DIR=lib/qt5/plugins \
                          -DQML_INSTALL_DIR=lib/qt5/qml \
                          -DLIB_INSTALL_DIR=lib \
                          -DPYTHON_EXECUTABLE=/usr/bin/python3 \
                          -DLOCALE_INSTALL_DIR=/usr/share/locale \
                          -DBUILD_TESTING=OFF")

def build():
    cmaketools.make()

def install():
    cmaketools.install()
    
    pisitools.dodoc("TODO")
