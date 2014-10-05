#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def build():
    autotools.make("CC=%s CFLAGS='%s'" % (get.CC(), get.CFLAGS()))

def check():
    autotools.make("test")

def install():
    #install binaries
    binaries=["jbgtopbm", "pbmtojbg", "jbgtopbm85", "pbmtojbg85"]
    for mybin in binaries:
        pisitools.dobin("pbmtools/%s" % mybin)

    #install shared libraries
    pisitools.dolib_so("libjbig/*.so.*")

    #symlinks
    pisitools.dosym("libjbig.so.2.1", "/usr/lib/libjbig.so")
    pisitools.dosym("libjbig85.so.2.1", "/usr/lib/libjbig85.so")

    #install headers
    pisitools.insinto("/usr/include", "libjbig/*.h")

    pisitools.doman("pbmtools/jbgtopbm.1", "pbmtools/pbmtojbg.1")
    pisitools.dodoc("ANNOUNCE", "CHANGES", "COPYING", "TODO")
