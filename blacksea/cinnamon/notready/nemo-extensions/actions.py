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
     for i in ["nemo-fileroller", "nemo-preview", "nemo-python", "nemo-seahorse", 
               "nemo-dropbox", "nemo-gtkhash", "nemo-python", "nemo-seahorse"]:
        shelltools.cd(i)
        cmaketools.configure("-DCMAKE_INSTALL_PREFIX=/usr")
        shelltools.cd("..")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("COPYING", "AUTHORS")