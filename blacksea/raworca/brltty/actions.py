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
                        --sysconfdir=/etc \
                        --localstatedir=/var \
                        --mandir=/usr/share/man \
                        --with-tables-directory=/usr/share/brltty \
                        --with-screen-driver=lx \
                        --enable-gpm \
                        --disable-java-bindings \
                        --disable-static")
def build():
     autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%(DESTDIR)s INSTALL_ROOT=%(DESTDIR)s" % {'DESTDIR':get.installDIR()})

    pisitools.dodoc("README")

