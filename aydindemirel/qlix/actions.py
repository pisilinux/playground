#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    shelltools.system("qmake Qlix.pro")

def build():
    autotools.make()

def install():
    pisitools.insinto("/usr/bin","qlix");        
    install_dirs = ["widgets","pixmaps","mtp","modeltest"]
    for i in install_dirs:
            pisitools.insinto("/usr/share/qlix",i)

    pisitools.dodoc("COPYING")
