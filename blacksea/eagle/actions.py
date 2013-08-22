#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir="."

def setup():
   
   shelltools.system("sh eagle-lin-*.run .")


def install():
       
    pisitools.insinto("/opt/eagle-6.5.0", "eagle-6.5.0/all")
    pisitools.insinto("/opt/eagle-6.5.0", "eagle-6.5.0/bin")
    pisitools.insinto("/opt/eagle-6.5.0", "eagle-6.5.0/cam")
    pisitools.insinto("/opt/eagle-6.5.0", "eagle-6.5.0/doc")
    pisitools.insinto("/opt/eagle-6.5.0", "eagle-6.5.0/dru")
    pisitools.insinto("/opt/eagle-6.5.0", "eagle-6.5.0/lbr")
    pisitools.insinto("/opt/eagle-6.5.0", "eagle-6.5.0/projects")
    pisitools.insinto("/opt/eagle-6.5.0", "eagle-6.5.0/scr")
    pisitools.insinto("/opt/eagle-6.5.0", "eagle-6.5.0/ulp")
    pisitools.dodoc("eagle-6.5.0/doc/README_en", "eagle-6.5.0/doc/license_en.txt")    
    
