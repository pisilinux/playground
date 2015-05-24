#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    shelltools.system("sed -i 's|glib/gquark\.h|glib.h|' src/gtk-hotkey-error.h")
    shelltools.system("sed -i 's|glib/gtypes\.h|glib.h|' src/x11/tomboykeybinder.h")
    
    #shelltools.export("DATADIR", "/usr/share")
    
    #shelltools.system("sed -i '/gtkhotkeydocdir/s//\$DATADIR/g' Makefile.{am,in}")
    
    autotools.autoreconf("-fiv")
    
    autotools.configure("--disable-static \
                         --docdir=/usr/share/doc")

def build():
    autotools.make()

def install():
    autotools.install()
    
    pisitools.domove("/usr/doc/gtkhotkey", "/usr/share/doc/gtkhotkey")
    pisitools.removeDir("/usr/doc")

    pisitools.dodoc("NEWS", "README", "ChangeLog", "AUTHORS", "COPYING")
