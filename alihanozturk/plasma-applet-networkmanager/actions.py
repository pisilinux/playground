#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    shelltools.makedirs("build")
    shelltools.cd("build")
    cmaketools.configure("-DCMAKE_INSTALL_PREFIX=/usr \
                          -DCMAKE_BUILD_TYPE=Release", sourceDir = "..")

def build():
    shelltools.cd("build")
    cmaketools.make()

def install():
    pisitools.dodoc("COPYING.LIB", "COPYING", "README")
    shelltools.cd("build")
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())