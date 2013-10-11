#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.configure("--prefix=/usr \
                         --sbindir=/usr/bin \
                         --libexecdir=/usr/lib \
<<<<<<< HEAD
                         --disable-static \
                         --enable-gtk-doc")
=======
                         --localstatedir=/var \
                         --disable-static \
                         --disable-gtk-doc \
                         --disable-debug")

    pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")
>>>>>>> 9de22661d9cb842ef5d137deafb795148cc692b0

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS", "ChangeLog*", "COPYING", "NEWS", "README*", "THANKS", "TODO")
