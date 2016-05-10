#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    autotools.configure("--prefix=/usr --sysconfdir=/etc --localstatedir=/var \
    --disable-static --enable-experimental --enable-gtk-doc \
    --with-package-name='GStreamer Bad Plugins (Pisi Linux)' \
    --with-package-origin='http://www.pisilinux.org/' \
    --with-gtk=3.0")
    #shelltools.system("sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool")

    pisitools.dosed("libtool", " -shared ", " -Wl,-O1,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS", "ChangeLog", "README", "NEWS", "COPYING.LIB")
