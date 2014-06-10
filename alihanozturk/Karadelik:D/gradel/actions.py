#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def build():
    shelltools.export("HOME",get.workDIR())
    WorkDir="gradel-0.12.1"
    shelltools.system("sh ./compile.sh")

def install():
    shelltools.system("sh ./install.sh")
    
    pisitools.dodoc("INSTALL", "README", "COPYING")