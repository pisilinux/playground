#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "."

def setup():
    shelltools.system("rpm2targz -v %s/jupiter-0.1.11-1.noarch.rpm" %get.workDIR())
    shelltools.system("tar xfvz %s/jupiter-0.1.11-1.noarch.tar.gz" %get.workDIR())


def install():
    pisitools.insinto("/etc/", "./etc/*")
    pisitools.insinto("/usr/", "./usr/*")

