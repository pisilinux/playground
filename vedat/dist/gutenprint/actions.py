#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    shelltools.makedirs("%s/m4local" % get.curDIR())
    shelltools.export("AT_M4DIR", "m4extra")
    shelltools.export("AUTOPOINT", "true")
    autotools.autoreconf("-fi")

    autotools.configure("--with-cups \
                         --with-foomatic \
                         --with-foomatic3 \
                         --with-ghostscript \
                         --with-readline \
                         --with-modules=dlopen \
                         --enable-test \
                         --enable-escputil \
                         --enable-cups-1_2-enhancements \
                         --enable-simplified-cups-ppds \
                         --enable-static-genppd \
                         --enable-cups-ppds \
                         --enable-cups-ppds-at-top-level \
                         --enable-lexmarkutil \
                         --enable-libgutenprintui2 \
                         --enable-samples \
                         --enable-shared \
                         --enable-user-guide \
                         --enable-cups-level3-ppds \
                         --disable-nls \
                         --disable-rpath \
                         --disable-static \
                         --disable-testpattern \
                         --disable-translated-cups-ppds \
                         --disable-globalized-cups-ppds \
                         --disable-dependency-tracking \
                         --enable-xmldef \
                         --without-ghost \
                         --without-gimp2 ")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s install" % get.installDIR())

    pisitools.dohtml("%s/usr/share/gutenprint/doc/reference-html/*" % get.installDIR())

    pisitools.removeDir("/usr/share/gutenprint/doc/")
    #pisitools.removeDir("/usr/include/gutenprintui2")

    # FIXME: Remove command.types, check if any other file exists
    pisitools.removeDir("/etc/")

    pisitools.remove("/usr/share/foomatic/kitload.log")
