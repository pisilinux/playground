#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

def setup():
    autotools.configure(" --prefix=/usr \
                          --enable-python='python3.4' \
                          --enable-perl \
                          --enable-openssl \
                          --enable-textfe")

    
def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s \
                         UPDATE_ICON_CACHE=true \
                         UPDATE_MIME_DATABASE=true \
                         UPDATE_DESKTOP_DATABASE=true" % get.installDIR())
    
    pisitools.dodoc("COPYING", "readme.*")
