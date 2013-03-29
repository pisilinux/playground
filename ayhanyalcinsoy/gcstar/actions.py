#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

WorkDir= "./gcstar"

def setup():
    shelltools.system("./install")
    
def build():
    shelltools.system("./install --text\
				 --noclean \
				 --nomenu \
				 --prefix=/usr")

def install():
    pisitools.insinto("/usr/", "bin")
    pisitools.insinto("/usr/", "lib")    
    pisitools.insinto("/usr/share/", "man")
    pisitools.insinto("/usr/share", "share/applications")
    pisitools.insinto("/usr/share", "share/gcstar")
    
    pisitools.dodoc("CHANGELOG", "LICENSE", "README", "README.fr")