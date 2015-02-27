#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    #shelltools.cd("kpackage")
    cmaketools.configure("-DCMAKE_BUILD_TYPE=Release \
                          -DCMAKE_INSTALL_PREFIX=/usr \
                          -DLIB_INSTALL_DIR=lib \
                          -DBUILD_TESTING=OFF")

def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("COPYING", "COPYING.LIB", "README.md")
