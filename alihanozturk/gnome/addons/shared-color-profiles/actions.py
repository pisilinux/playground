#!/usr/bin/python
# -*- coding: utf-8 -*-
#

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    autotools.configure()

def build():
    autotools.make("-j1")

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    
    #pisitools.insinto("/usr/share/pixmaps", "data/icons/48x48/gnome-color-manager.png")

    pisitools.dodoc("AUTHORS", "COPYING", "ChangeLog", "NEWS", "README")