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
                          -DENABLE_GTK2=true \
                          -DQTC_QT5_ENABLE_KDE=false \
                          -DQTC_QT4_ENABLE_KDE=false \
                          -DENABLE_QT5=false \
                          -DENABLE_QT4=false")

def build():
    cmaketools.make()

def install():
    cmaketools.install()
    pisitools.remove("/usr/lib/libqtcurve-utils.so*")
    pisitools.remove("/usr/share/themes/QtCurve/gtk-2.0/kdeglobals")
    pisitools.dodoc("README.md", "COPYING", "AUTHORS", "TODO.md")
