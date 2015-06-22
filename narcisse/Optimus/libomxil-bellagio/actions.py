 
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
  
    autotools.autoreconf("-vfi")
  
    if get.buildTYPE() == "emul32":
      
      autotools.configure("--libdir=/usr/lib32 \
	                   --disable-werror") 
      
    elif get.ARCH() == "x86_64":
      
      autotools.configure("--disable-werror")    

def build():
    
    autotools.make("-j8")

def install():
    
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    