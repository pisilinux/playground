#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import qt4
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
#    qt4.configure()
#     shelltools.system("qmake plume-creator-all.pro.user")
      shelltools.cd ()
      shelltools.system("qmake-qt ${./plume-creator-all.pro}")
def build():
    qt4.make()

def install():
    qt4.install()

    pisitools.dodoc("Credits", "License", "KNOWN ISSUES", "COPYING", "INSTALL_NOTES", "README")
