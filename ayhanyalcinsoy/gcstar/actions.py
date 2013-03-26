#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools
# from pisi.actionsapi import shelltools

# if pisi can't find source directory, see /var/pisi/gcstar/work/ and:
WorkDir="./gcstar"

def setup():
    autotools.install("./install")
#     pisitools.dobin("./bin/gcstar", "/bin")
#     pisitools.dolib("/lib/gcstar", "usr/lib/")
#     pisitools.doman("./man/gcstar.1")
#     pisitools.domove("./share/applications ","usr/share/applications")
#     pisitools.domove("./share/gcstar","usr/share")
    
def build():
      autotools.make("./install")

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
#    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "README")

