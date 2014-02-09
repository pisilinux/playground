#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

def build():
    autotools.make()

def install():
    pisitools.dobin("sshuttle")
    
    pisitools.dodir("/usr/share/sshuttle")
    pisitools.insinto("/usr/share/sshuttle", "*.py")
    pisitools.insinto("/usr/share/sshuttle", "compat")
    pisitools.insinto("/usr/share/sshuttle/version", "version/*")
    
    pisitools.doman("Documentation/sshuttle.8")