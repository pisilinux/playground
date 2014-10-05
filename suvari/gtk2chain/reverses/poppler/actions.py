#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools


def setup():
    options = "--disable-static \
               --disable-gtk-doc-html \
               --enable-zlib \
               --disable-gtk-test \
               --enable-poppler-qt4 \
               --disable-poppler-qt5 \
               --enable-cairo-output \
               --enable-xpdf-headers \
               --enable-libjpeg \
               --enable-libopenjpeg \
               --enable-poppler-glib \
               --with-testdatadir=%s/%s/test" % (get.workDIR(), get.srcDIR())

    if get.buildTYPE() == "emul32":
        options += " --libdir=/usr/lib32 \
                     --disable-utils \
                     --disable-gtk-test \
                     --disable-poppler-cpp \
                     --disable-poppler-qt4"

    autotools.configure(options)

def build():
    autotools.make()

def check():
    autotools.make("check")

def install():
    if get.buildTYPE() == "emul32":
        pisitools.insinto("/usr/lib32", "poppler/.libs/libpoppler.so*")
        pisitools.insinto("/usr/lib32", "glib/.libs/libpoppler-glib.so*")
        for f in ["poppler.pc", "poppler-glib.pc"]:
            pisitools.insinto("/usr/lib32/pkgconfig", f)
            pisitools.dosed("%s/usr/lib32/pkgconfig/%s" % (get.installDIR(), f), get.emul32prefixDIR(), get.defaultprefixDIR())
        return
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())


    pisitools.removeDir("/usr/share/gtk-doc")
    pisitools.dodoc("README", "AUTHORS", "ChangeLog", "NEWS", "README-XPDF", "TODO")
