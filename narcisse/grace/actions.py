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
    shelltools.export("OS_CXXFLAGS", "%s -fno-strict-aliasing" % get.CXXFLAGS())
    shelltools.export("OS_CFLAGS", "%s -fno-strict-aliasing" % get.CFLAGS())
    
    
    autotools.configure("--prefix=/usr \
                         --bindir=/usr/bin \
                         --libdir=/usr/lib \
                         --enable-grace-home=/usr/lib/grace \
			 --datarootdir=/usr/share")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("DEVELOPERS", "COPYRIGHT", "README", "ChangeLog", "CHANGES", "LICENSE")

