#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import libtools
from pisi.actionsapi import get

def setup():
    autotools.autoheader()
    libtools.libtoolize("--force --copy --automake")
    autotools.configure("--enable-shared \
                         --enable-sharedlibs=gcc \
                         --enable-error-messages=all \
                         --enable-timer-type=clock_gettime \
                         --enable-romio \
                         --enable-pmiport \
                         --with-python=python2")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("README","RELEASE_NOTES","CHANGES","COPYRIGHT")

