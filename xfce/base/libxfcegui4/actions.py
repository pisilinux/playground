#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
<<<<<<< HEAD
    autotools.configure("--libexecdir=/usr/lib \
                         --disable-static")
=======
    autotools.configure("--prefix=/usr \
                         --libexecdir=/usr/lib \
                         --disable-static \
                         --disable-debug \
                         --disable-gladeui \
                         --enable-startup-notification")
>>>>>>> 9de22661d9cb842ef5d137deafb795148cc692b0

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())


    pisitools.dodoc("COPYING*", "NEWS", "README", "TODO", "ChangeLog", "AUTHORS")
