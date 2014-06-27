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
    shelltools.echo("AC_CONFIG_MACRO_DIR([m4])", "configure.ac")
    shelltools.system("./autogen.sh")
    autotools.autoreconf("-fi")
    autotools.configure("--prefix=/usr \
                         --localstatedir=/var \
                         --disable-static \
                         --disable-schemas-compile \
                         --enable-sm \
                         --enable-startup-notification")
    
    pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")    

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.insinto("/usr/share/gir-1.0", "usr/lib/muffin/*.gir")
    pisitools.insinto("/usr/lib/girepository-1.0", "usr/lib/muffin/*.typelib")

    pisitools.dodoc("COPYING", "NEWS", "README")
