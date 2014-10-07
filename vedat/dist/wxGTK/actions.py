# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    pisitools.flags.add("-fno-strict-aliasing")
    pisitools.dosed("configure", '(wx_cv_std_libpath="lib)64"', r'\1"')

    autotools.configure("--disable-debug \
                         --disable-gtktest \
                         --disable-optimise \
                         --disable-precomp-headers \
                         --disable-rpath \
                         --disable-sdltest \
                         --enable-compat28 \
                         --enable-display \
                         --enable-geometry \
                         --enable-graphics_ctx \
                         --enable-gstreamer \
                         --enable-gui \
                         --enable-intl \
                         --enable-joystick \
                         --enable-libnotify \
                         --enable-libtiff \
                         --enable-mediactrl \
                         --enable-no_deps \
                         --enable-opengl \
                         --enable-shared \
                         --enable-sound \
                         --enable-sys \
                         --enable-tiff \
                         --enable-timer \
                         --enable-unicode \
                         --enable-webkit \
                         --enable-webview \
                         --enable-xrc \
                         --with-expat=sys \
                         --with-gtk=2 \
                         --with-gtkprint \
                         --with-libjpeg=sys \
                         --with-libpng=sys \
                         --with-libtiff=sys \
                         --with-libxpm=sys \
                         --with-opengl \
                         --with-regex=sys \
                         --with-sdl \
                         --with-zlib=sys \
                         --without-gnomeprint \
                         --without-gnomevfs \
                         --without-odbc ")

def build():
    autotools.make()
    autotools.make("-C locale allmo")

def install():
    autotools.install()

    pisitools.dodoc("docs/*.txt", "docs/*.htm")
    pisitools.rename("/usr/bin/wxrc-3.0", "wxrc")
    pisitools.rename("/usr/bin/wx-config", "wxconfig")
