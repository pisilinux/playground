 
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    #autotools.autoreconf("-fiv")
     
    autotools.configure("--prefix=/usr \
                         --disable-nautilus \
                         --enable-libburnia \
                         --enable-preview \
                         --enable-inotify \
                         --enable-cdrdao \
                         --enable-cdrkit \
                         --disable-cdrtools \
                         --disable-caches \
                         --disable-static \
                         --enable-gtk-doc \
                         --enable-gtk-doc-html")
    

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("ChangeLog","COPYING", "NEWS", "README")