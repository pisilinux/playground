#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt


from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get


def setup():
    autotools.rawConfigure ("-opensource \
                             -eglfs \
                             -opengl es2 \
                             -xcb \
                             -no-pch \
                             -no-rpath \
                             -dbus-linked \
                             -optimized-qmake \
                             -dbus-linked \
                             -icu \
                             -cups \
                             -nis \
                             -widgets \
                             -gui \
                             -qt-xcb \
                             -system-xkbcommon \
                             -openssl-linked \
                             -system-libjpeg \
                             -system-libpng \
                             -system-zlib \
                             -largefile \
                             -c++11 \
                             -shared \
                             -no-static \
                             -confirm-license \
                             -release \
                             -prefix /usr \
                             -bindir /usr/lib/qt5/bin \
                             -docdir /usr/share/doc/qt5 \
                             -headerdir /usr/include/qt5 \
                             -archdatadir /usr/lib/qt5 \
                             -datadir /usr/share/qt5 \
                             -sysconfdir /etc/xdg \
                             -examplesdir /usr/lib/qt5/examples \
                             -nomake examples \
                             -nomake tests")


def build():
    autotools.make ()

def install():
    autotools.rawInstall ("INSTALL_ROOT=%s" % get.installDIR())

    pisitools.remove("/usr/lib/*.prl")
