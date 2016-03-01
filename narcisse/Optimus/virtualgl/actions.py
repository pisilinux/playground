# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import cmaketools
from pisi.actionsapi import shelltools

def setup():
    shelltools.makedirs("build")
    shelltools.cd("build")
    
    options = "-DCMAKE_INSTALL_PREFIX=/usr/share \
               -DTJPEG_INCLUDE_DIR=/usr/include \
               -DVGL_INCDIR=/usr/include \
               -DVGL_DOCDIR=/usr/share/doc/%s \
               -DVGL_SYSTEMFLTK=ON \
               -DVGL_BUILDSTATIC=OFF \
               " % get.srcNAME()
    
    if get.buildTYPE() == "emul32":
      
      options += "-DVGL_LIBDIR=/usr/lib32 \
                  -DTJPEG_LIBRARY=/usr/lib32/libturbojpeg.so \
                  -DVGL_FAKELIBDIR=/usr/lib32/fakelib \
                  -DVGL_BINDIR=/usr/lib32/virtualgl/bin \
                 "
    elif get.ARCH() == "x86_64":
      
      options += "-DVGL_LIBDIR=/usr/lib \
                  -DTJPEG_LIBRARY=/usr/lib/libturbojpeg.so \
                  -DVGL_FAKELIBDIR=/usr/lib/fakelib \
                  -DVGL_BINDIR=/usr/bin \
                  -DVGL_SYSTEMGLX=ON \
                 "
      
    
    cmaketools.configure(options, sourceDir="..")

def build():
    shelltools.cd("build")
    cmaketools.make()

def install():
    shelltools.cd("build")
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
    
    if get.buildTYPE() == "emul32":      
      pisitools.domove("/usr/lib32/virtualgl/bin/glxinfo", "/usr/lib32/virtualgl/bin", "vglxinfo")    
      
      for exe in ["cpustat", "glreadtest", "glxspheres", "nettest", "tcbench",
		  "vglclient", "vglconfig", "vglconnect", "vglgenkey", "vgllogin",
		  "vglrun", "vglserver_config", "vglxinfo"]:
	
	pisitools.dosym("/usr/lib32/virtualgl/bin/%s" %exe, "/usr/bin/%s32" %exe)
	
    else:      
      pisitools.rename("/usr/bin/glxinfo", "vglxinfo")  
      pisitools.rename("/usr/bin/glxspheres64", "glxspheres")
