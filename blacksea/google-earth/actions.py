#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "."

def setup():
      shelltools.system("rpm2targz google-earth-stable_current_x86_64.rpm")
      shelltools.system("tar xfvz google-earth-stable_current_x86_64.tar.gz")

def install():
      pisitools.insinto("/etc/","./etc/*")
      pisitools.insinto("/opt/","./opt/*")
      pisitools.dosym("/lib/ld-2.18.so", "/lib/ld-lsb-x86-64.so.2")
      pisitools.dosym("/lib/ld-2.18.so", "/lib/ld-lsb-x86-64.so.3")
