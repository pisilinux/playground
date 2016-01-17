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
    autotools.autoreconf("-vif")
    autotools.configure("--sysconfdir=/etc \
                         --libexecdir=/usr/lib/cinnamon-screensaver \
                         --prefix=/usr \
                         --disable-static \
                         --with-mit-ext \
                         --with-xf86gamma-ext \
                         --enable-locking \
                         --enable-docbook-docs")
    
    pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("README", "AUTHORS")