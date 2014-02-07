#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir='xfig.%s' % get.srcVERSION()

def setup():
    shelltools.system("sed -i -e 's|X11R6/||' -e 's|image/x-xfig|image/fig;image/x-xfig|' xfig.desktop")
    shelltools.system("sed -i -e 's/#define XAW3D/XCOMM #define XAW3D/' Imakefile")
    shelltools.system("sed -i -e 's/XCOMM USEINLINE/USEINLINE/' Imakefile")
    shelltools.system("sed -i -e 's/XCOMM #define I18N/#define I18N/' \
                              -e 's/XCOMM XAW_INTERN/XAW_INTERN/' Imakefile")
    shelltools.system("groff -mandoc -Thtml Doc/xfig.man > Doc/xfig_man.html")

def build():
    shelltools.system("xmkmf")
    autotools.make('XFIGDOCDIR=/usr/share/doc/xfig \
                    LIBDIR=/usr/share \
                    XAPPLOADDIR=/usr/share/X11/app-defaults')

def install():
    autotools.make('DESTDIR=%s XFIGDOCDIR=/usr/share/doc/xfig LIBDIR=/usr/share \
                               MANDIR=/usr/share/man/man1 \
                               XAPPLOADDIR=/usr/share/X11/app-defaults install.all' % get.installDIR())

    pisitools.insinto("/usr/share/pixmaps", "xfig.png")
    pisitools.remove("/usr/share/app-defaults")
