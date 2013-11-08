# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    options = '--prefix=/usr'

    if get.buildTYPE() == "emul32":
        options += " --libdir=/usr/lib32"
        shelltools.export("CFLAGS", "%s -m32" % get.CFLAGS())

    autotools.configure(options)

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
   
    #remove conflict files
    pisitools.removeDir("/usr/share/man")
    pisitools.remove("/usr/include/pngconf.h")
    pisitools.remove("/usr/include/png.h")
    pisitools.remove("/usr/bin/libpng-config")
    
    if get.buildTYPE() == "emul32":
        pisitools.remove("/usr/lib32/libpng.la")
        pisitools.remove("/usr/lib32/libpng.so")
        pisitools.remove("/usr/lib32/pkgconfig/libpng.pc")

    else:
        pisitools.remove("/usr/lib/libpng.la")
        pisitools.remove("/usr/lib/libpng.so")
        pisitools.remove("/usr/lib/pkgconfig/libpng.pc")

    pisitools.dodoc("ANNOUNCE", "CHANGES", "KNOWNBUG", "README", "TODO")
