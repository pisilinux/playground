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
    shelltools.makedirs("%s/source/build" % get.workDIR())
    shelltools.cd("%s/source/build" % get.workDIR())
    shelltools.sym("../configure", "configure")
    autotools.configure("--disable-native-texlive-build \
                         --with-banner-add=/PisiLinux \
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
                         --disable-dump-share \
                         --disable-aleph \
                         --enable-shared \
                         --disable-static \
                         --with-system-zlib \
                         --with-system-zziplib \
                         --with-system-pnglib \
                         --with-system-ncurses \
                         --with-system-t1lib \
                         --with-system-gd \
                         --with-system-poppler \
                         --with-system-xpdf \
                         --with-system-freetype2 \
                         --with-system-pixman \
                         --with-system-icu \
                         --with-freetype2-libdir=/usr/lib \
                         --with-freetype2-include=/usr/include/freetype2 \
                         --with-xdvi-x-toolkit=xaw \
                         --disable-dump-share \
                         --disable-aleph \
                         --disable-luatex \
                         --with-clisp-runtime=default \
                         --enable-xindy \
                         --disable-xindy-rules \
                         --with-system-graphite2 \
                         --disable-web2c \
                         --disable-dependency-tracking \
                         --disable-mktexmf-default \
                         --enable-build-in-source-tree \
                         --disable-tex \
                         --disable-mktexfmt-default \
                         --disable-texlive \
                         --disable-xindy-docs ")
#--prefix=/usr  \
 #                        --libdir=/usr/lib \
  #                       --sysconfdir=/etc \
   #                      --includedir=/usr/include \
    #                     --datarootdir=/usr/share \
#                         --datadir=/usr/share \
     #                    --mandir=/usr/share/man \

def build():
    #shelltools.cd("%s/source/build" % get.workDIR())
    shelltools.cd("%s/source/build/" % get.workDIR())
    #autotools.make("prefix=%s/source/build/usr texmf=/usr/share/texmf install"  % get.workDIR())
    autotools.make()
    
def install():
    #autotools.install("prefix=%s/source/build/usr texmf=%s/usr/share/texmf" % (get.workDIR(), get.installDIR()))
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.insinto("%s/source/build/biber" "%s/usr/bin/biber" % (get.workDIR(), get.installDIR()))
    pisitools.insinto("%s/source/utils/biber/TeXLive/*.pm" "%s/usr/share/tlpkg/TeXLive" % (get.workDIR(), get.installDIR()))
