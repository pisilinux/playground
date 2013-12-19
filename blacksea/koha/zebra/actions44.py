#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get


KeepSpecial=["libtool"]

def setup():
    autotools.autoreconf("-fi")
    autotools.configure("--disable-static")
     #autotools.autoreconf("-vif")
    # shelltools.system('./configure --disable-static')
     #autotools.configure("--disable-static")
     #shelltools.system("sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool")
    # shelltools.system("sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool")
     #autotools.configure("--disable-static")
     #shelltools.system('CPPFLAGS="-DUSE_INTERP_ERRORLINE" ./configure')
          #autotools.autoreconf("-fiv")
               pisitools.cflags.add("-fno-strict-aliasing")
def build():
    autotools.make()

def check():
    autotools.make("check")

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR()) 
