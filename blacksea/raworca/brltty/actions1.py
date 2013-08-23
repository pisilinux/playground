#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt


from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get



def setup():

    autotools.configure("--prefix=/usr \
--sysconfdir='${prefix}/etc' \
--localstatedir='${prefix}/var'  \
--mandir='${prefix}/usr/share/man' \
--with-lib-directory='${prefix}/usr/lib/brltty' \
--with-tables-directory='${prefix}/usr/share/brltty' \
--enable-gpm \
--disable-java-bindings \
--disable-static")


def build():
    autotools.make()

def install():
     autotools.install()
  
     pisitools.dodoc("README")
