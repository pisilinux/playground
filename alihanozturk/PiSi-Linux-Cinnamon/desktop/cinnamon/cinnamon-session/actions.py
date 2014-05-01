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
    autotools.autoreconf("-vif")
    shelltools.system("NOCONFIGURE=1 ./autogen.sh")
    autotools.configure("--libexecdir=/usr/lib/cinnamon-session \
                         --disable-schemas-compile \
                         --disable-gconf \
                         --enable-docbook-docs \
                         --disable-systemd \
                         --with-gnu-ld")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("COPYING", "AUTHORS")