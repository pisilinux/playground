#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.autoreconf("-vfi")
    autotools.configure("--disable-static \
                         --sysconfdir=/etc \
                         --without-ibmtts \
                         --without-flite \
                         --without-nas \
                         --with-ivona \
                         --with-alsa \
                         --with-espeak \
                         --with-libao \
                         --with-pulse")
    
    pisitools.dosed("libtool", " -shared ", " -Wl,-O1,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.install()

    # Create log directory, it should be world unreadable
    pisitools.dodir("/var/log/speech-dispatcher")
    shelltools.chmod("%s/var/log/speech-dispatcher" % get.installDIR(), 0700)

    pisitools.dodoc("AUTHORS", "COPYING", "README")
