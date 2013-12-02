#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "Nightingale"

def install():
    shelltools.cd("..")
    pisitools.dodir("/opt")
    pisitools.insinto("/opt","Nightingale")
   
    
# By PiSiDo 2.0.0
