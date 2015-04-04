#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import cmaketools

def setup():
      cmaketools.configure('-DCMAKE_BUILD_TYPE=Release \
                            -DCMAKE_INSTALL_PREFIX=/usr \
                            -DJSONCPP_WITH_TESTS=OFF \
                            -DJSONCPP_LIB_BUILD_SHARED=ON -G "Unix Makefiles" ../..')

def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
    
    pisitools.dodoc("NEWS.txt", "LICENSE", "README.md")
