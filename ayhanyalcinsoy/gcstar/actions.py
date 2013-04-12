#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

WorkDir= "./gcstar"

def fixPermissions():
    import os
    for root, dirs, files in os.walk("%s/opt" % get.installDIR()):
        for d in dirs:
            shelltools.system("/bin/chmod 0755 %s/%s" % (root, d))
        for f in files:
            shelltools.system("/bin/chmod 0644 %s/%s" % (root, f))

def install():
    pisitools.insinto("/usr/", "bin")
    pisitools.insinto("/usr/", "lib")    
    pisitools.insinto("/usr/share/", "man")
    pisitools.insinto("/usr/share", "share/applications")
    pisitools.insinto("/usr/share", "share/gcstar")
    
    pisitools.dodoc("CHANGELOG", "LICENSE", "README", "README.fr")
