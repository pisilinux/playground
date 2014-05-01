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
    autotools.autoreconf("-fiv")
    shelltools.echo("AC_CONFIG_MACRO_DIR([m4])", "configure.ac")
    shelltools.system("NOCONFIGURE=1 ./autogen.sh")
    autotools.configure("--prefix=/usr \
                         --sysconfdir=/etc \
                         --libexecdir=/usr/lib/muffin \
                         --localstatedir=/var \
                         --disable-static \
                         --enable-compile-warnings=minimum")
    
    pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")    

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("COPYING", "NEWS", "README")
