#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

#WorkDir = "polkit-qt-1-%s" % (get.srcVERSION())

def setup():
    pisitools.ldflags.add("-Wl,-rpath,/usr/lib")
    cmaketools.configure("-DUSE_QT5=ON \
                          -DCMAKE_BUILD_TYPE=Release \
                          -DCMAKE_INSTALL_PREFIX=/usr \
                          -DCMAKE_INSTALL_LIBDIR=lib \
                          -DUSE_QT4=OFF")

def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS", "COPYING", "README*", "TODO")
