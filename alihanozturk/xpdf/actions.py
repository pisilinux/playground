#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    shelltools.system("sed -i -e 's:/usr/share/fonts/type1/gsfonts:/usr/share/fonts/Type1:' xpdf/GlobalParams.cc")
    shelltools.system("sed -i -e 's:times-medium-r-normal--16:times-medium-r-normal--14:' xpdf/XPDFViewer.cc # FS#14217")
    autotools.configure("--prefix=/usr \
                         --sysconfdir=/etc \
                         --mandir=/usr/share/man \
                         --enable-multithreaded \
                         --enable-wordlist \
                         --with-freetype2-library=/usr/lib \
                         --with-freetype2-includes=/usr/include/freetype2 \
                         --x-includes=/usr/include \
                         --with-Xm-library=/usr/lib \
                         --with-Xm-includes=/usr/include")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.insinto("/usr/share/pixmaps/xpdfIcon.xpm", "xpdf/xpdfIcon.xpm")
    
    pisitools.dodoc("COPYING", "README")
