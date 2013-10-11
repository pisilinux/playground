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
<<<<<<< HEAD

    autotools.configure("--libexecdir=/usr/lib \
                        --disable-static \
                        --enable-gtk-doc \
                        --with-vendor-info='Pisi Linux'")
=======
    autotools.configure("--prefix=/usr \
                         --libexecdir=/usr/lib \
                         --disable-static \
                         --disable-gtk-doc \
                         --disable-gladeui \
                         --disable-debug \
                         --with-vendor-info='Pisi Linux'")
>>>>>>> 9de22661d9cb842ef5d137deafb795148cc692b0

def build():
    autotools.make()

def install():
    autotools.rawInstall('DESTDIR=%s' % get.installDIR())
    pisitools.dodoc('NEWS', 'COPYING', 'README', 'TODO', 'ChangeLog', 'AUTHORS', 'THANKS')
