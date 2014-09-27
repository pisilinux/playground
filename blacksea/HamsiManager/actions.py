#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "."

def install():
    
    pisitools.insinto("/usr/lib","./usr/lib/*")
    pisitools.insinto("/usr/share/locale","./usr/share/locale/*")
    pisitools.dobin("usr/lib/HamsiManager-1.2.2/hamsi")
               
