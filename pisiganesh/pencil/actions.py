#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

#WorkDir = get.workDIR() + "/pencil-2.0.5"


def install():
    #shelltools.cd("..")
    pisitools.dodir("/usr")
    pisitools.insinto("/usr/bin","usr/bin/pencil")
    pisitools.insinto("/usr/share/applications/","usr/share/applications/pencil.desktop")
    pisitools.insinto("/usr/share/pencil/","usr/share/pencil/chrome/")
    pisitools.insinto("/usr/share/pencil/","usr/share/pencil/content/")
    pisitools.insinto("/usr/share/pencil/","usr/share/pencil/defaults/")
    pisitools.insinto("/usr/share/pencil/","usr/share/pencil/icons/")
    pisitools.insinto("/usr/share/pencil/","usr/share/pencil/locale/")
    pisitools.insinto("/usr/share/pencil/","usr/share/pencil/skin/")
    pisitools.insinto("/usr/share/pencil/","usr/share/pencil/application.ini")
    pisitools.insinto("/usr/share/pencil/","usr/share/pencil/chrome.manifest")
    pisitools.insinto("/usr/share/pencil/","usr/share/pencil/install.rdf")
    pisitools.insinto("/usr/share/pencil/","usr/share/pencil/install.rdf.tpl.xml")
    pisitools.insinto("/usr/share/pencil/","usr/share/pencil/main-window.icns")
    pisitools.insinto("/usr/share/pencil/","usr/share/pencil/update.rdf.tpl.xml")

    
    

    
# By PiSiDo 2.0.0
# By PiSiDo 2.0.0
