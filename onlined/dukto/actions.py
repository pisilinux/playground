#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

def setup():
    shelltools.system("rpm2targz -v %s/dukto-6.0-13.8.x86_64.rpm" %get.workDIR())
    shelltools.system("tar xfvz %s/dukto-6.0-13.8.x86_64.tar.gz" %get.workDIR())

def install():
    pisitools.insinto("/usr/", "usr/*")