#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get


def setup():
    autotools.configure("--prefix=/usr \
                         --localstatedir=/var \
                         --sysconfdir=/etc \
                         --sbindir=/usr/bin \
                         --libexecdir=/usr/lib/ \
                         --disable-static \
                         --enable-liblightdm-gobject \
                         --enable-liblightdm-qt \
                         --with-user-session=kde \
                         --with-greeter-user=root \
                         --with-greeter-session=lxqt-lightdm-greeter \
                         --with-html-dir=/usr/share/doc/lightdm/html \
                         ")
##--with-greeter-user=lightdm --disable-tests \
def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

