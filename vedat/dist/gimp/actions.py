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
    shelltools.export("PYTHON","/usr/bin/python")
    #pisitools.dosed("app/text/gimpfont.c", "freetype/tttables.h", "freetype2/tttables.h")
    shelltools.system("sh ./autogen.sh")
    #autotools.aclocal()
    #autotools.autoreconf("-vif")
    autotools.configure("--prefix=/usr \
                         --sysconfdir=/etc \
                         --enable-mp \
                         --enable-gimp-console \
                         --enable-default-binary \
                         --enable-python \
                         --enable-static \
                         --enable-gimp-remote \
                         --disable-silent-rules \
                         --with-gif-compression=lzw \
                         --with-libcurl \
                         --without-aa \
                         --without-gnomevfs \
                         --without-hal \
                         --without-gvfs \
                         --without-xvfb-run \
                         --with-xmc ")
    
    pisitools.dosed("libtool", " -shared ", " -Wl,-O1,--as-needed -shared ")

    # Add illustrator and other mime types
    pisitools.dosed("desktop/gimp.desktop.in", "^MimeType=application/postscript;application/pdf;(.*)$",
                    "MimeType=\\1;image/x-sun-raster;image/x-gray;image/x-pcx;image/jpg;image/x-bmp;image/pjpeg;image/x-png;application/illustrator;")


def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS", "ChangeLog*", "HACKING", "NEWS", "README", "INSTALL", "LICENSE")