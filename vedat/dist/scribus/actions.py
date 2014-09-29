#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import kde4
from pisi.actionsapi import shelltools

    
def setup():
    # Remove version info from doc dir
    shelltools.system("svn checkout svn://scribus.net/trunk/Scribus scribus")
    shelltools.system("svn up scribus -r19541")
    shelltools.cd("scribus")
    pisitools.dosed("CMakeLists.txt", "\"share\/doc\/\$\{MAIN_DIR_NAME\}.*", "\"share/doc/${MAIN_DIR_NAME}/\")")
    kde4.configure("-DWANT_DISTROBUILD=YES")

def build():
    shelltools.cd("scribus")
    kde4.make()

def install():
    shelltools.cd("scribus")
    kde4.install()

    pisitools.insinto("/usr/share/pixmaps", "resources/icons/scribus.png")
    pisitools.insinto("/usr/share/pixmaps", "resources/icons/scribusdoc.png", "x-scribus.png")
