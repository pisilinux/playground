#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools

def setup():
    options = "--disable-static \
               --disable-rpath \
               --disable-silent-rules \
               --disable-guile \
               --enable-heartbeat-support \
               --enable-libdane \
               --enable-nls \
               --with-p11-kit \
               --with-zlib \
               --without-tpm \
               --with-unbound-root-key-file=/etc/dnssec/root-anchors.txt \
               --disable-valgrind-tests"
#--with-unbound-root-key-file=/etc/dnssec/root-anchors.txt \ "need to unbound package"
    if get.buildTYPE() == "emul32":
        options += " --disable-hardware-acceleration \
                     --enable-gtk-doc \
                     --enable-gtk-doc-pdf \
                     --enable-guile \
                     --enable-crywrap \
                     --enable-local-libopts \
                   "

    autotools.configure(options)

    pisitools.dosed("libtool", " -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make("-C gl")
    autotools.make("-C lib")
    autotools.make("-C extra")
    autotools.make("-C libdane")

def check():
    autotools.make("-C gl check")
    #autotools.make("-C tests check")
    #some tests fail in emul32
    if get.buildTYPE() == "emul32":
        autotools.make("-C gl check")

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
