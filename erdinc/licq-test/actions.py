#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import qt4
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

dirs=["build","plugins"]

def setup():
    shelltools.makedirs("build")
    for dir in dirs:
        shelltools.cd(dir)
        cmaketools.configure("-DUSE_OPENSSL=ON -DCMAKE_INSTALL_PREFIX=/usr" ,sourceDir="..")
        shelltools.cd("..")

def build():
    shelltools.cd("build")
    cmaketools.make()
    shelltools.cd("..")

    shelltools.cd("plugins")
    cmaketools.make()


def install():
    for dir in dirs:
        shelltools.cd(dir)
        cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
        shelltools.cd("..")

    pisitools.dodoc("LICENSE", "README")
