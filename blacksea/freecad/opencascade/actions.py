#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import libtools

WorkDir = "ros/"

def setup():
    autotools.configure("--with-gl2ps=/usr/include \
                         --with-tbb-include=/usr/include/tbb \
                         --with-tbb-library=/usr/lib \
                         --with-tcl=/usr/lib \
                         --with-tk=/usr/lib \
                         --with-ftgl=/usr/include \
                         --with-freetype=/usr \
                         --with-xmu-include=/usr/include/X11 \
                         --with-xmu-library=/usr/lib \
                         --with-qt \
                         --with-x \
                         --enable-shared \
                         --enable-openmp \
                         --disable-debug \
                         --enable-production \
                         --libdir=%s/usr/lib" % get.installDIR())

def build():
    autotools.make()

def install():
    libtools.libtoolize()
    autotools.install()
    pisitools.domove("/usr/inc/*", "/usr/include/occ/") 
    pisitools.removeDir("/usr/inc") 
