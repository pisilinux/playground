#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "cwp-1.9.1"
shelltools.export("HOME", "%s" % get.workDIR())

def setup():
    cmaketools.configure("DQT_QMAKE_EXECUTABLE=qmake-qt4 \
                          DCMAKE_INSTALL_PREFIX=/usr \
                          DCMAKE_BUILD_TYPE=Release")

def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("COPYING", "README")
