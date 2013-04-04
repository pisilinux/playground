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
    shelltools.export("LDFLAGS", "%s -lfontconfig" % get.LDFLAGS())
    autotools.autoreconf("-fiv")
    autotools.configure("--disable-static \
                         --enable-authentication-scheme=pam \
                         --with-sysconfsubdir=X11/gdm \
                         --disable-scrollkeeper \
                         --with-user=gdm \
                         --with-group=gdm \
                         --with-xauth-dir=/var/lib/gdm \
                         --with-screenshot-dir=/var/lib/gdm \
                         --with-xevie")

def build(): 
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    
    pisitools.chown("%s/var/lib/gdm" % get.installDIR(), "gdm", "gdm")

    for d in ["/var/gdm", "/var/lib/gdm/.gconf*"]:
        pisitools.removeDir(d)

    for f in ["/var/lib/gdm/.gconf*", "/usr/sbin/gdm"]:
        pisitools.remove(f)

    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING*", "NEWS", "README")
