#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt


from pisi.actionsapi import shelltools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import autotools

def setup():
    shelltools.system("./autogen.sh --libdir=/usr/lib \
                                    --sysconfdir=/etc \
                                    --prefix=/usr \
                                    --enable-shared \
                                    --disable-static \
				    --without-gtk \
				    --disable-gtk-doc \
				    --enable-udisks \
				    --disable-actions \
                                    --disable-demo \
                                    --disable-dependency-tracking \
                                    --enable-fast-install=autogen")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.dodoc("AUTHORS", "COPYING")