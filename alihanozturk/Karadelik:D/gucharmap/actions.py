#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.autoreconf("-vif")
    shelltools.system("./autogen.sh")
    autotools.configure("--disable-static \
                         --disable-schemas-compile \
                         --with-gtk=3.0 \
                         --with-pic \
                         --enable-introspection")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("README", "TODO", "NEWS", "ChangeLog", "AUTHORS", "COPYING")