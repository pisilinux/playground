#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

def setup():
    shelltools.system("patch -p0 < no-rpath.patch")
    shelltools.system("patch -p0 < ca-dir.patch")
    options = " --prefix=/usr \
                --libdir=lib \
                --openssldir=/etc/ssl \
                shared zlib enable-md2 -Wa,--noexecstack"
               

    shelltools.system("./config %s" % options)

def build():
    autotools.make("-j1")

def install():
    pisitools.insinto("/usr/lib/","libssl.so.0.9.8","libssl.so.0.9.8")
    pisitools.insinto("/usr/lib/","libcrypto.so.0.9.8","libcrypto.so.0.9.8")
    pisitools.dodoc("LICENSE")
