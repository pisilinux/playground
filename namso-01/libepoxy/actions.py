#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

def setup():
    options = "./autogen.sh \
               --prefix=/usr \
               --disable-static \
               --disable-silent-rules \
              "
    
    if get.buildTYPE() == "_emul32":
        options += " --libdir=/usr/lib32 \
                   "
    
    shelltools.export("CC", "%s -m32" % get.CC())
    shelltools.export("CXX", "%s -m32" % get.CC())
    shelltools.export("PKG_CONFIG_PATH", "/usr/lib32/pkgconfig")
    
    shelltools.system(options)

def build():
    autotools.make()
    
def check():
    autotools.make("check")

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("COPYING","README.*")
