#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pythonmodules
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def install():
    pythonmodules.compile()
    pythonmodules.install()
    
    pisitools.domove("/usr/share/kde4/bin/history-manager","/usr/bin")
    #Remove history-manager from systemsettings, we have a painful crash because of the thread problem of pykde/python
   # pisitools.remove("/usr/kde/4/share/kde4/services/kcm_historymanager.desktop")
