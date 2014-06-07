#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    shelltools.system("./autogen.sh")
    autotools.configure("--prefix=/usr \
                         --sysconfdir=/etc \
                         --localstatedir=/var \
                         --disable-static \
                         --disable-rpath \
                         --disable-schemas-compile \
                         --enable-introspection=yes \
                         --enable-compile-warnings=no")
    
    pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")
    
def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    shelltools.makedirs("/usr/share/cinnamon/locale/")

    pisitools.dodoc("README", "AUTHORS")