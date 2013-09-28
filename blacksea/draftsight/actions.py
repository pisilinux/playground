#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "."

def setup():
  
     shelltools.system("rpm2targz draftSight.rpm")
     shelltools.system("tar xfvz draftSight.tar.gz")

def install():
    pisitools.insinto("/usr/bin/","./usr/bin/*")
    pisitools.insinto("/opt/","./opt/*")
    pisitools.insinto("/usr/share/icons/hicolor/","./opt/dassault-systemes/draftsight/mime/pixmaps/*")
    pisitools.insinto("/usr/share/mime/application/","./opt/dassault-systemes/draftsight/mime/*.xml")
    shelltools.cd("./opt/dassault-systemes/draftsight/Eula/")
    pisitools.dohtml("english/*")
