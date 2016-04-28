#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools

def setup():
    cmaketools.configure("-DCMAKE_CXX_FLAGS='-DBOOST_VARIANT_USE_RELAXED_GET_BY_DEFAULT' \
                          -DCMAKE_INSTALL_PREFIX=/usr \
                          -DLIB_DESTINATION=/usr/lib \
                          -DENABLE_DEMO=OFF \
                          -DENABLE_TEST=OFF")

def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS", "COPYING", "README*")
