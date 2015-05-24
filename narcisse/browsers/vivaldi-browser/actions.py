# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "."

def setup():
  
     shelltools.system("ar -xv Vivaldi_TP3.1.0.162.9-1_amd64.deb")
     shelltools.system("mkdir vivaldi")
     shelltools.system("tar -xJf data.tar.xz -C vivaldi")     
     
def install():
    
      pisitools.insinto("/usr/bin/","./vivaldi/usr/bin/*")
      pisitools.insinto("/usr/share/","./vivaldi/usr/share/*")
      pisitools.insinto("/opt/","./vivaldi/opt/*")
      pisitools.insinto("/etc/","./vivaldi/opt/*")
      
      pisitools.dosym("/opt/vivaldi/product_logo_22.png", "/usr/share/icons/hicolor/22x22/apps/vivaldi.png")
      pisitools.dosym("/opt/vivaldi/product_logo_24.png", "/usr/share/icons/hicolor/24x24/apps/vivaldi.png")
      pisitools.dosym("/opt/vivaldi/product_logo_32.png", "/usr/share/icons/hicolor/32x32/apps/vivaldi.png")
      pisitools.dosym("/opt/vivaldi/product_logo_48.png", "/usr/share/icons/hicolor/48x48/apps/vivaldi.png")
      pisitools.dosym("/opt/vivaldi/product_logo_64.png", "/usr/share/icons/hicolor/64x64/apps/vivaldi.png")
      pisitools.dosym("/opt/vivaldi/product_logo_128.png", "/usr/share/icons/hicolor/128x128/apps/vivaldi.png")
      pisitools.dosym("/opt/vivaldi/product_logo_256.png", "/usr/share/icons/hicolor/256x256/apps/vivaldi.png")
      
      #pisitools.dosym("/opt/vivaldi/vivaldi", "/usr/bin/vivaldi-preview")
      
      pisitools.removeDir("/usr/share/menu")
      pisitools.removeDir("/usr/share/doc")
      
