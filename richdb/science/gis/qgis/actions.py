#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

shelltools.export("HOME", get.workDIR())

def setup():
    shelltools.makedirs("build")
    shelltools.cd("build")

    cmaketools.configure("-DCMAKE_BUILD_TYPE=Release \
                          -DQGIS_MANUAL_SUBDIR=share/man", installPrefix="/usr",sourceDir="..")

def build():
    shelltools.cd("build")
    cmaketools.make()

def install():
    shelltools.cd("build")
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
    shelltools.cd("")
    pisitools.dosed('debian/qgis.desktop',  'qgis-icon',  '/usr/share/qgis/images/icons/qgis-icon.png')
    pisitools.insinto("/usr/share/applications/", "debian/qgis.desktop")
    pisitools.domove("/usr/share/qgis/doc/*", "/usr/share/doc/qgis/")
