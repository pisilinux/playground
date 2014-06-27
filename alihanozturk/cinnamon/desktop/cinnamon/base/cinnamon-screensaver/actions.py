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
    shelltools.echo("ACLOCAL_AMFLAGS = -I m4", "Makefile.am")
    shelltools.echo("AC_CONFIG_MACRO_DIR([m4])", "configure.ac")
    shelltools.system("./autogen.sh")
    autotools.autoreconf("-vif")
    autotools.configure("--sysconfdir=/etc \
                         --with-mit-ext \
                         --with-xf86gamma-ext \
                         --enable-locking \
                         --disable-schemas-compile \
                         --enable-docbook-docs \
                         --with-pam-prefix=/etc \
                         --with-console-kit=yes \
                         --without-systemd")
    
    pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("README", "AUTHORS")