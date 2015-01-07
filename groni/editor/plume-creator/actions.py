#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import qt4
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "."

def setup():
    qt4.configure(projectfile="plume-creator-all.pro", parameters="CONFIG+=release CONFIG-=debug PREFIX=/usr")
      
def build():
    qt4.make()

def install():
    qt4.install()
    
    pisitools.insinto("/usr/share/pixmaps", "resources/images/icons/hicolor/32x32/apps/plume-creator.png")
    
    pisitools.dosed("%s/usr/share/applications/plume-creator.desktop" % get.installDIR(), "Icon=plume-creator", "Icon=/usr/share/pixmaps/plume-creator.png")

    pisitools.dodoc("Credits", "License", "KNOWN ISSUES", "COPYING", "INSTALL_NOTES", "README")
