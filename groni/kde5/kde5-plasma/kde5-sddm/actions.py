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
    shelltools.system("sed -e 's|-Wall -march=native||'  -e 's|-O2||'  -i CMakeLists.txt")
    cmaketools.configure("-DCMAKE_INSTALL_PREFIX=/usr \
                          -DCMAKE_BUILD_TYPE=Release \
                          -with-systemdsystemunitdir=no \
                          -DCMAKE_INSTALL_LIBEXECDIR=/usr/lib/sddm \
                          -DBUILD_MAN_PAGES=ON")

def build():
    cmaketools.make()

def install():
    cmaketools.install()
    pisitools.dodoc("COPYING-CC-BY-3.0", "CONTRIBUTORS", "ChangeLog", "COPYING", "COPYING-CC-BY-SA-3.0", "README.md")
