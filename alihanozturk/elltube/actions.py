#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

WorkDir="elltube-0.3"



def build():
    pass
    

def install():
    shelltools.system("make DESTDIR=%s PREFIX=/usr install" % get.installDIR())
    #pisitools.dobin("/usr/bin/elltube")