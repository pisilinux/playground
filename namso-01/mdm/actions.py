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
    #shelltools.system("chmod +x ./autogen.sh")
    #shelltools.export("AUTOMAKE", "automake")
    shelltools.system("./autogen.sh")
    autotools.configure("--enable-ipv6=yes \
                         --with-prefetch \
                         --prefix=/usr \
                         --with-console-kit=no \
                         --sysconfdir=/etc \
                         --libexecdir=/usr/lib/mdm \
                         --localstatedir=/var/lib \
                         --disable-static \
                         --disable-scrollkeeper \
                         --enable-secureremote=yes \
                         --enable-ipv6=yes \
                         --enable-compile-warnings=no\
                         --sbindir=/usr/bin \
                         LDFLAGS=-lXau")
    shelltools.system("sed -i -e 's|${prefix}|/usr|' config.h")
    
    # fix unused-direct-shlib-dependency
    pisitools.dosed("libtool", "( -shared )", " -Wl,-O1,--as-needed\\1")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    
    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING", "MAINTAINERS", "NEWS", "README*", "TODO")