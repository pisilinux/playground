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

def setup():
    cmaketools.configure("-DUSE_OPENSSL=ON")

    #shelltools.cd("plugins")
    #cmaketools.configure()
    #shelltools.cd("..")

def build():
    cmaketools.make()

    #shelltools.cd("plugins")
    #cmaketools.make()
    #shelltools.cd("..")

def install():
    #shelltools.cd("plugins")
    #cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
    #shelltools.cd("..")
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("LICENSE", "README")
