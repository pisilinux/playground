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
  
     shelltools.system("ar -xv kingsoft-office_9.1.0.4184~a12p1_i386.deb")
     shelltools.system("tar -aJxvf data.tar.lzma")
      
def install():
    
      pisitools.insinto("/usr/bin/","./usr/bin/*")
      pisitools.insinto("/usr/share/","./usr/share/*")
      pisitools.insinto("/opt/","./opt/*")
