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
  #  shelltools.system('xdt-autogen')
    autotools.configure("--prefix=/usr \
    --sysconfdir=/etc \
    --libexecdir=/usr/lib \
    --localstatedir=/var \
    --disable-static \
    --enable-gtk-doc \
    --disable-debug \
    --with-vendor-info='Pisi Linux'")

def build():
    autotools.make()

def install():
    autotools.rawInstall('DESTDIR=%s' % get.installDIR())
    pisitools.dodoc('NEWS', 'COPYING', 'README', 'TODO', 'ChangeLog', 'AUTHORS', 'THANKS')
