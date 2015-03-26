#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools, get, autotools, pisitools

def setup():
    # TODO: Use system xkbcommon (>=0.4.1)
    # NOTE: —no-warnings-are-errors  is due to ld.gold warnings:
    # sqlite3 hidden symbols
    autotools.rawConfigure ("-opensource \
                             -confirm-license \
                             -eglfs \
                             -opengl es2 \
                             -xcb \
                             -no-pch \
                             -dbus-linked \
                             -openssl-linked \
                             -optimized-qmake \
                             -icu \
                             -cups \
                             -nis \
                             -widgets \
                             -gui \
                             -qt-xcb \
                             -openssl-linked \
                             -system-libjpeg \
                             -system-libpng \
                             -system-harfbuzz \
                             -system-zlib \
                             -system-sqlite \
                             -largefile \
                             -c++11 \
                             -shared \
                             -no-static \
                             -release \
                             -prefix /usr \
                             -bindir /usr/bin \
                             -headerdir /usr/include/qt5 \
                             -archdatadir /usr/lib/qt5 \
                             -datadir /usr/share/qt5 \
                             -docdir /usr/share/doc/qt5 \
                             -examplesdir /usr/lib/qt5/examples \
                             -sysconfdir /etc/xdg \
                             -plugin-sql-{psql,mysql,sqlite} \
                             -nomake tests \
                             -nomake examples \
                             -xkb-config-root /usr/share/X11/xkb \
                             -no-use-gold-linker \
                             -no-warnings-are-errors ")


def build():
    autotools.make ()

def install():
    pisitools.dodir("/usr/bin")
    pisitools.dodir("/usr/lib")
    autotools.rawInstall ("INSTALL_ROOT=%s" % get.installDIR())

    pisitools.remove("/usr/lib/*.prl") 
