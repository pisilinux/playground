#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "AssaultCube_v1.2.0.2.source"
WorkDir = "AssaultCube_v1.2.0.2"

def setup():
    WorkDir = "AssaultCube_v1.2.0.2.source"
    shelltools.cd("source/enet")
    autotools.autoreconf("-vfi")

def build():
    WorkDir = "AssaultCube_v1.2.0.2.source"
    shelltools.cd("source/src")
    autotools.make()

def install():
    WorkDir = "AssaultCube_v1.2.0.2"
    shelltools.cd("source/src")
    pisitools.dobin("ac_client")
    pisitools.dobin("ac_server")
    shelltools.cd("..")
    shelltools.cd("..")
    pisitools.insinto("/usr/share/AssaultCube", "config")
    pisitools.insinto("/usr/share/AssaultCube", "docs")
    pisitools.insinto("/usr/share/AssaultCube", "mods")
    pisitools.insinto("/usr/share/AssaultCube", "packages")