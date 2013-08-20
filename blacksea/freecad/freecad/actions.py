#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2006-2011 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
#

from pisi.actionsapi import pisitools
from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import libtools

WorkDir = "FreeCAD-%s" % get.srcVERSION()

def setup():
    autotools.autoreconf("-fi")
    autotools.configure("--prefix=/usr/lib/freecad \
                         --datadir=/usr/share/freecad \
                         --includedir=/usr/include/freecad \
                         --docdir=/usr/share/doc/freecad \
                         --with-qt4-bin=/usr/bin \
                         --with-qt4-include=/usr/include \
                         --with-qt4-lib=/usr/lib \
                         --with-occ-include=/usr/include/occ \
                         --with-occ-lib=/usr/lib \
                         --with-python-include=/usr/include/python2.7 \
                         --with-python-lib=/usr/lib/python2.7 \
                         --disable-debug")

def build():
    autotools.make("-lGL -lGLU -lglut")

def install():
    libtools.libtoolize()
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dosym("/usr/lib/freecad/FreeCAD", "/usr/bin/FreeCAD") 
    pisitools.dosym("/usr/lib/freecad/FreeCADCmd", "/usr/bin/FreeCADCmd")
