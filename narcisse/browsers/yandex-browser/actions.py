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
  
     shelltools.system("ar -xv Yandex.deb")
     shelltools.system("mkdir yandex")
     shelltools.system("tar -xJf data.tar.xz -C yandex")     
     
def install():
    
      pisitools.insinto("/usr/bin/","./yandex/usr/bin/*")
      pisitools.insinto("/usr/share/","./yandex/usr/share/*")
      pisitools.insinto("/opt/","./yandex/opt/*")
      pisitools.insinto("/etc/","./yandex/opt/*")
      
      pisitools.dosym("/opt/yandex/browser-beta/product_logo_22.png", "/usr/share/icons/hicolor/22x22/apps/yandex-browser-beta.png")
      pisitools.dosym("/opt/yandex/browser-beta/product_logo_24.png", "/usr/share/icons/hicolor/24x24/apps/yandex-browser-beta.png")
      pisitools.dosym("/opt/yandex/browser-beta/product_logo_32.png", "/usr/share/icons/hicolor/32x32/apps/yandex-browser-beta.png")
      pisitools.dosym("/opt/yandex/browser-beta/product_logo_48.png", "/usr/share/icons/hicolor/48x48/apps/yandex-browser-beta.png")
      pisitools.dosym("/opt/yandex/browser-beta/product_logo_64.png", "/usr/share/icons/hicolor/64x64/apps/yandex-browser-beta.png")
      pisitools.dosym("/opt/yandex/browser-beta/product_logo_128.png", "/usr/share/icons/hicolor/128x128/apps/yandex-browser-beta.png")
      pisitools.dosym("/opt/yandex/browser-beta/product_logo_256.png", "/usr/share/icons/hicolor/256x256/apps/yandex-browser-beta.png")
      
      pisitools.removeDir("/usr/share/menu")
      
      #pisitools.remove("/usr/bin/yandex-browser-beta")
      #pisitools.dosym("/opt/yandex/browser-beta/yandex-browser", "/usr/bin/yandex-browser-beta")
      #pisitools.dosym("/opt/yandex/browser-beta/product_logo_32.png", "/usr/share/pixmaps/yandex-browser-beta.png")