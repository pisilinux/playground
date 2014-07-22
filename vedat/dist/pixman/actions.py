#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.autoreconf("-vif")
    autotools.configure("--disable-static")
    #pisitools.dosed("pixman/pixman.h", "pixman-version.h", "pixman-1/pixman-version.h")
    
def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    #if get.ARCH() == "x86_64" :
        #for header in ["pixman.h","pixman-version.h"]:
            #pisitools.dosym("/usr/include/pixman-1/%s" % header , "/usr/include/%s" % header)
    for header in ["pixman.h","pixman-version.h"]:
        pisitools.insinto("/usr/include/", "/usr/include/pixman-1/%s" % header)
        
    pisitools.dodoc("AUTHORS", "COPYING", "ChangeLog", "README")
