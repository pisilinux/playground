# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt 

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    autotools.configure("--prefix=/usr \
                         --includedir=/usr/include/sdcc \
                         --libdir=/usr/lib/sdcc")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR='%s'" % get.installDIR())

    pisitools.remove("usr/share/doc/sdcc/INSTALL.txt")

    pisitools.dodoc("ChangeLog", "COPYING", "README")