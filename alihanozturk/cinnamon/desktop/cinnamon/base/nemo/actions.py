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
    shelltools.system("sed -i -e '/AC_SUBST(DISABLE_DEPRECATED_CFLAGS)/d' configure.in")
    shelltools.system("./autogen.sh")
    autotools.configure("--disable-schemas-compile \
                         --enable-gtk-doc \
                         --disable-more-warnings \
                         --disable-update-mimedb")
    
    pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.dodir("/usr/share/nemo/themes/Adwaita-Nemo/gtk-3.0/apps/")

    pisitools.dodoc("README", "AUTHORS")