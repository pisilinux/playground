#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt 

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

WorkDir="%s-%s-master" %(get.srcNAME(), get.srcVERSION())

def setup():
    shelltools.system("sed -i 's/DL_Window:://' src/download_win.h")
    autotools.autoreconf("-fi")
    autotools.configure("--prefix=/usr \
			 --disable-libtool-lock")

def build():
    autotools.make()

def install():
    autotools.install()

    pisitools.dodoc("CREDITS", "CHANGES", "COPYING*", "README")

