#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "CoinMP-%s" %get.srcVERSION()



def setup():
  
    #autotools.autoreconf("-vfi")
    autotools.configure()

def build():
    autotools.make("-j8")

def install():
    autotools.make("test")
    autotools.rawInstall("DESTDIR=%s" %get.installDIR())
    
    pisitools.removeDir("/var")

