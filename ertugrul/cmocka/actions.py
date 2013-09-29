#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2013 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import cmaketools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get


def setup():
    shelltools.makedirs("build")
    shelltools.cd("build")
    
    cmaketools.configure("-DCMAKE_INSTALL_PREFIX=/usr  \
                          -DCMAKE_BUILD_TYPE=Debug \
                          -DUNIT_TESTING=ON \
                          -DCMAKE_INSTALL_LIBDIR=/usr/lib",sourceDir="..")

def build():
    shelltools.cd("build")
    autotools.make()

def install():
    shelltools.cd("build")
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
