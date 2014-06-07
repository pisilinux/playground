#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "f-spot-%s" % get.srcVERSION()

def setup():
    shelltools.export("MONO_SHARED_DIR", get.workDIR())
    shelltools.system("MCS=/usr/bin/dmcs")
    autotools.configure("--prefix=/usr \
                         --disable-static \
                         --disable-scrollkeeper \
                         --disable-schemas-install \
                         --enable-release \
                         --with-gnome-screensaver=/usr \
                         --with-gnome-screensaver-privlibexecdir=/usr/libexec/gnome-screensaver \
                         --with-vendor-build-id=PisiLinux")
    
    #pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")

def build():
    shelltools.export("MONO_SHARED_DIR", get.workDIR())
    autotools.make()

def install():
    shelltools.export("MONO_SHARED_DIR", get.workDIR())
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
        
    pisitools.dodoc("README", "NEWS", "TODO", "AUTHORS", "ChangeLog")