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
                         --enable-mediactrl \
                         --enable-webview \
                         --with-regex=builtin \
                         --with-libpng=sys \
                         --with-libxpm=sys \
                         --with-libjpeg=sys \
                         --with-libtiff=sys \
                         --disable-precomp-headers")

def build():
    autotools.make()
    autotools.make("-C locale allmo")

def install():
    autotools.install()

    pisitools.dodoc("docs/licence.txt", "docs/gpl.txt", "docs/lgpl.txt")
