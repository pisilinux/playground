#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

# if pisi can't find source directory, see /var/pisi/gcstar/work/ and:
WorkDir="./gcstar"

def setup():
    autotools.configure()

def build():
    autotools.make("./install")

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "README")

