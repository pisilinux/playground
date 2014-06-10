#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def build():
    shelltools.system("sed -i -e 's/-Werror//g' -e '/^LEX=/s|=.*$|= LC_ALL=C flex|g' -e '/^YACC=/s|=.*$|= LC_ALL=C bison|g' generate/unix/Makefile.config || exit 1")
    shelltools.export("CFLAGS", "%s -fno-strict-aliasing" % get.CFLAGS())
    autotools.make("-j1 BITS=64")
    if get.ARCH() == "x86_64":
        autotools.make("BITS=64")
    else:
        autotools.make("BITS=32")
    
    
def install():
    autotools.rawInstall('DESTDIR="%s"' % get.installDIR())
    pisitools.dodoc("changes.txt")
