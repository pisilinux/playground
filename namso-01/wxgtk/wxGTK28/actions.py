# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    autotools.configure("--with-gtk=2 \
                         --with-opengl \
                         --enable-unicode \
                         --enable-graphics_ctx \
                         --disable-optimize \
                         --enable-mediactrl \
                         --with-regex=builtin \
                         --with-libpng=sys \
                         --with-libjpeg=sys \
                         --with-libxpm=sys \
                         --with-libtiff=sys \
                         --with-sdl \
                         --disable-precomp-headers")

def build():
    autotools.make()
    autotools.make("-C contrib")
    autotools.make("-C locale allmo")

def install():
    autotools.install()
    autotools.install("-C contrib")

    pisitools.dodoc("docs/*.txt", "docs/*.htm")