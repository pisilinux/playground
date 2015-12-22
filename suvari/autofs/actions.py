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
    autotools.autoreconf("-vif")
    autotools.configure("./configure --prefix=/usr --sysconfdir=/etc/autofs --sbindir=/usr/bin \
                                     --with-mapdir=/etc/autofs --without-hesiod \
                                     --enable-ignore-busy")
    shelltools.system("sed -i -e 's|/etc/auto.misc|/etc/autofs/auto.misc|' \
                              -e 's|/etc/auto.master.d|/etc/autofs/auto.master.d|' samples/auto.master")

def build():
    autotools.make()

def install():
    autotools.rawInstall("INSTALLROOT=%s" % get.installDIR())

    #pisitools.removeDir("/etc/init.d")

    pisitools.dodoc("CREDITS", "COPY*", "samples/ldap*", "samples/autofs.schema")