#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt 

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get



def setup(): 
    shelltools.system("ar -xv atunes_3.1.1-1_all.deb")
    shelltools.system("tar -xzf data.tar.gz") 

def install():
    pisitools.insinto("/usr/bin/","usr/bin/*")
    pisitools.insinto("/usr/share/","usr/share/*")

