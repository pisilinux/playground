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
    shelltools.system("sed -i -e 's@{ACLOCAL_FLAGS}@{ACLOCAL_FLAGS} -I m4@g' Makefile.am")
    shelltools.echo("AC_CONFIG_MACRO_DIR([m4])", "configure.ac")
    shelltools.system("./autogen.sh")
    autotools.autoreconf("-fi")
    autotools.configure("--disable-static")
    
    pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.insinto("/usr/lib/girepository-1.0", "usr/lib/cjs/girepository-1.0/CjsPrivate-1.0.typelib")

    pisitools.dodoc("COPYING", "COPYING.LGPL", "NEWS", "README")