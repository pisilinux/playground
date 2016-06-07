#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools

def setup():
    autotools.configure("--prefix=/usr \
                         --sysconfdir=/etc \
                         --localstatedir=/var \
                         --libexecdir=/usr/lib/colord \
                         --with-daemon-user=colord    \
                         --enable-vala                \
                         --enable-systemd-login=no    \
                         --disable-argyllcms-sensor   \
                         --disable-bash-completion    \
                         --disable-static             \
                         --with-systemdsystemunitdir=no")
    
    pisitools.dosed("libtool", " -shared ", " -Wl,-O1,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING", "TODO", "README.md")
