# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools

def setup():
    autotools.configure("--prefix=/usr  \
    --sysconfdir=/etc \
    --sbindir=/usr/bin \
    --with-rcdir=no \
    --enable-avahi \
    --with-browseremoteprotocols=DNSSD,CUPS")
        
  #      --disable-static \
   #                      --disable-dependency-tracking \
    #                     --enable-avahi \
     #                    --with-rcdir=no")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

