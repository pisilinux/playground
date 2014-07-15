#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools

from pisi.actionsapi import get


def setup():
  
    #shelltools.system ("sed -i -e 's:getgroups:lightdm_&:' tests/src/libsystem.c")
    autotools.configure("--prefix=/usr \
                         --localstatedir=/var \
                         --sysconfdir=/etc \
                         --sbindir=/usr/bin \
                         --libexecdir=/usr/libexec/lightdm \
                         --disable-static \
                         --enable-introspection \
                         --enable-liblightdm-gobject \
                         --enable-liblightdm-qt \
                         --with-greeter-session=lightdm-gtk-greeter \
                         --with-html-dir=/usr/share/doc/lightdm/html \
                         ")
##--with-greeter-user=lightdm --disable-tests \ --with-greeter-user=root \ --with-user-session=kde \
def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

