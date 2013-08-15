#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt


from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir="."
    
    
def install():  
    pisitools.insinto("/usr/bin/", "obmenu-generator")
    shelltools.chmod("%s/usr/bin/obmenu-generator" % get.installDIR(), 0755)
    shelltools.chown("%s/usr/bin/obmenu-generator" % get.installDIR(), gid="users")


