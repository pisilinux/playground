 
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import cmaketools
from pisi.actionsapi import shelltools

def setup():
    shelltools.export("CXXFLAGS", get.CXXFLAGS())
    shelltools.export("CFLAGS", get.CFLAGS())
    
    cmaketools.configure("-DCMAKE_INSTALL_PREFIX=/usr/lib \
                          -DOPUSFILE_LIBRARY=/usr/lib/libopus.so \
                          -DOPUS_INCLUDE_DIR=/usr/include/opus \
                          -DUSE_CURSES=0 \
                          -DUSE_GEOIP:BOOL=OFF \
                          -DUSE_CIN_XVID=0 \
                          -DUSE_CIN_THEORA=1 \
                          -DHAVE_BZIP2=1 \
                          -DUSE_INTERNAL_SDL=0 \
                          -DUSE_INTERNAL_CRYPTO=0 \
                          -DUSE_INTERNAL_JPEG=0 \
                          -DUSE_INTERNAL_OPUS=0 \
                          -DUSE_INTERNAL_SPEEX=0 \
                          -DUSE_INTERNAL_GLEW=0 \
                          -DUSE_INTERNAL_WEBP=0 \
                          -DUSE_INTERNAL_OPUS=1")   

def build():
    cmaketools.make()

def install():
    cmaketools.install()    

    pisitools.dodoc("GPL.txt","COPYING.txt", "README.md")