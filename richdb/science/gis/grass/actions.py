#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

if get.ARCH()== "x86_64": e64 = " --enable-64bit"
else: e64 = ''

def setup():
    #pisitools.dosed("configure", "--libmysqld-libs", "--libs")
    autotools.configure("--with-cxx \
                         --enable-shared \
                         --disable-static \
                         --datadir=/usr/share/grass \
                         --with-curses \
                         --with-proj \
                         --with-proj-includes=/usr/include \
                         --with-proj-libs=/usr/lib \
                         --with-proj-share=/usr/share/proj \
                         --with-gdal \
                         --without-glw \
                         --with-postgres \
                         --with-sqlite \
                         --with-mysql \
                         --with-mysql-includes=/usr/include/mysql \
                         --with-opengl \
                         --enable-largefile \
                         --with-x \
                         --with-odbc \
                         --with-blas \
                         --with-lapack \
                         --with-fftw \
                         --with-cairo \
                         --with-python \
                         --with-freetype=yes \
                         --with-motif \
                         --with-wxwidgets=wx-config \
                         --with-readline \
                         --with-readline-includes=/usr/include/readline \
                         --with-readline-libs=/lib \
                         --with-postgres-includes=/usr/include/postgresql \
                         --with-freetype-includes=/usr/include/freetype2 \
                         --with-ffmpeg \
                         --with-ffmpeg-includes='/usr/include/libavcodec \
                         /usr/include/libavformat \
                         /usr/include/libavutil \
                         /usr/include/libswscale' \
                         --with-nls%s" % e64)

def build():
    autotools.make("htmldocs-single")
    autotools.make()

def install():
    autotools.install()
    gw = get.srcVERSION().replace('.',  '')[:-1]
    print gw
    for i in ["AUTHORS", "CHANGES", "COPYING", "GPL.TXT", "REQUIREMENTS.html"]:
        pisitools.domove("/usr/lib/grass%s/%s" % (gw, i),  "/usr/share/doc/grass/")
    pisitools.domove("/usr/lib/grass%s/docs/html" % gw,  "/usr/share/doc/grass/html")
    pisitools.remove("/usr/lib/grass%s/docs" % gw)
    pisitools.domove("/usr/lib/grass%s/include/grass" % gw, "/usr/include")
    pisitools.insinto("/usr/lib/pkgconfig", "grass.pc")
    pisitools.dosed("%s/usr/bin/grass%s" % (get.installDIR(), gw), "(GISBASE=).*install(.*)", r"\1\2")
