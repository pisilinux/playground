#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.configure("--prefix=/usr \
                         --sysconfdir=/etc \
                         --localstatedir=/var \
                         --sbindir=/usr/sbin \
                         --disable-rpath \
                         --enable-gost \
                         --with-libevent \
                         --with-pythonmodule \
                         --with-pyunbound \
                         --with-pthreads \
                         --enable-ecdsa \
                         --with-rootkey-file=/etc/dnssec/root-anchors.txt \
                         --with-conf-file=/etc/unbound/unbound.conf \
                         --with-pidfile=/run/unbound.pid")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    
    pisitools.dodoc("LICENSE", "README")
