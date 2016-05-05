#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

def setup():
    shelltools.system("sed -e '/UPOWER_SERVICE)/ s:^://:' \
                       -i src/daemon/PowerManager.cpp")
    shelltools.system("sed -e 's/eval exec/& ck-launch-session /' \
    -i data/scripts/Xsession")
    
    shelltools.makedirs("build")
    shelltools.cd("build")    

    cmaketools.configure("-DCMAKE_INSTALL_PREFIX=/usr \
                          -DCMAKE_BUILD_TYPE=Release \
                          -DCMAKE_INSTALL_LIBEXECDIR=/usr/lib/sddm \
                          -DENABLE_JOURNALD=OFF \
                          -DDBUS_CONFIG_FILENAME=sddm_org.freedesktop.DisplayManager.conf \
                          -DBUILD_MAN_PAGES=ON \
                          -Wno-dev", sourceDir=".." )

def build():
    shelltools.makedirs("build")
    shelltools.cd("build")

    cmaketools.make()

def install():
    shelltools.makedirs("build")
    shelltools.cd("build")

    cmaketools.install()

    pisitools.dodoc("../COPYING")
