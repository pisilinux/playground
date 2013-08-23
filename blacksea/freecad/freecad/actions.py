#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "freecad-0.13.1830"  

def setup():
    shelltools.makedirs("%s/%s/build" % (get.workDIR(),WorkDir))
    shelltools.cd("%s/%s/build" % (get.workDIR(),WorkDir))
    cmaketools.configure("-DOCC_INCLUDE_DIR:PATH=/usr/include/occ/ ", sourceDir = "..")
                         
                         # -DOCC_INCLUDE_DIR:PATH=/usr/include/occ/ 


def build():
    shelltools.cd("%s/%s/build" % (get.workDIR(),WorkDir))
    cmaketools.make()

def install():
    libtools.libtoolize()
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.dosym("/usr/lib/freecad/FreeCAD", "/usr/bin/FreeCAD") 
    pisitools.dosym("/usr/lib/freecad/FreeCADCmd", "/usr/bin/FreeCADCmd")
  