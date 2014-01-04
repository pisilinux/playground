#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get
from pisi.actionsapi import libtools
from pisi.actionsapi import texlivemodules

import os

WorkDir = "."

def setup():
    if get.ARCH() == "x86_64":
        shelltools.export("CFLAGS", "%s -fPIC" % get.CFLAGS())

    shelltools.cd("/%s/source/" % get.workDIR())

    # prevent compiling Xdvi with libXp
    # it's a workaround should be fixed with a better regex pattern
    pisitools.dosed("texk/xdvik/configure","-lXp ")

    shelltools.makedirs("%s/source/build" % get.workDIR())
    shelltools.cd("%s/source/build" % get.workDIR())

    shelltools.sym("../configure", "configure")
    autotools.configure("--disable-native-texlive-build \
                         --with-banner-add=\"/PisiLinux\" \
                         --disable-multiplatform \
                         --disable-chktex \
                         --disable-dialog \
                         --disable-detex \
                         --disable-dvipng \
                         --disable-dvi2tty \
                         --disable-dvipdfmx \
                         --disable-lcdf-typetools \
                         --disable-ps2eps \
                         --disable-psutils \
                         --disable-t1utils \
                         --disable-bibtexu \
                         --disable-xz \
                         --disable-xdvik \
                         --enable-shared \
                         --disable-static \
                         --with-system-zlib \
                         --with-system-icu \
                         --with-system-pnglib \
                         --with-system-ncurses \
                         --with-system-t1lib \
                         --with-system-gd \
                         --with-system-xpdf \
                         --with-system-poppler \
                         --with-system-cairo \
                         --with-system-freetype2 \
                         --with-system-harfbuzz \
                         --with-system-graphite2 \
                         --with-freetype2-libdir=/usr/lib \
                         --with-freetype2-include=/usr/include/freetype2 \
                         --with-xdvi-x-toolkit=xaw \
                         --disable-dump-share \
                         --disable-aleph \
                         --disable-luatex \
                         --with-clisp-runtime=default \
                         --enable-xindy --disable-xindy-rules --disable-xindy-docs")

def build():
    shelltools.cd("%s/source/build" % get.workDIR())
    autotools.make()

def install():
    #make install
    shelltools.cd("%s/source/build" % get.workDIR()) 
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    ## symlink engines by hand.
    pisitools.dosym("/usr/bin/eptex","/usr/bin/platex")
    pisitools.dosym("/usr/bin/euptex","/usr/bin/uplatex")
    pisitools.dosym("/usr/bin/xetex","/usr/bin/xelatex")

    #pdftex
    pdftex_symlinks_create=["amstex","cslatex","csplain","eplain","etex","jadetex","latex","mex","mllatex","mltex","pdfetex",
                     "pdfcslatex","pdfcsplain","pdfjadetex","pdflatex","pdfmex","pdfxmltex","texsis","utf8mex","xmltex"] 

    for symlink in pdftex_symlinks_create:
        pisitools.dosym("/usr/bin/pdftex", "/usr/bin/%s" % symlink)


    # remove symlinks to scripts that are not in texlive-bin or texlive-core:
    symlinks_to_remove = ["authorindex",
                          "ebong",
                          "bibexport",
                          "cachepic",
                          "epspdf",
                          "epspdftk",
                          "fig4latex",
                          "makeglossaries",
                          "mathspic",
                          "mkgrkindex",
                          "pdfannotextractor",
                          "perltex",
                          "pst2pdf",
                          "ps4pdf",
                          "splitindex",
                          "svn-multi",
                          "htcontext",
                          "htlatex",
                          "htmex",
                          "ht",
                          "httexi",
                          "httex",
                          "htxelatex",
                          "htxetex",
                          "mk4ht",
                          "ulqda",
                          "vpe",
                          "tlmgr"]

    for symlink in symlinks_to_remove:
        pisitools.remove("/usr/bin/%s" % symlink)