#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import autotools

def setup():
    autotools.configure("--prefix=/usr \
                         --force \
                         --disable-gtk-update-checks")
    
def build():
    perlmodules.make()

def install():
    perlmodules.install()

  
