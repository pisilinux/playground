#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    shelltools.export("MONO_SHARED_DIR=", "/.wabi")
    shelltools.system("MCS=/usr/bin/dmcs")
    autotools.configure("--prefix=/usr \
                         --sysconfdir=/etc \
                         --localstatedir=/var \
                         --disable-static \
                         --disable-scrollkeeper \
                         --disable-schemas-install \
                         --enable-release \
                         --with-gnome-screensaver=/usr \
                         --with-gnome-screensaver-privlibexecdir=/usr/lib/gnome-screensaver \
                         --with-vendor-build-id=PisiLinux")

    #pisitools.dosed("libtool", " -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING*", "NEWS", "README")

