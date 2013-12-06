#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import kerneltools
from pisi.actionsapi import pisitools

KDIR = kerneltools.getKernelVersion()

def build():
    autotools.make()

def install():
     pisitools.insinto("/lib/modules/%s/kernel/drivers/acpi" % KDIR, "*.ko")
     pisitools.dodoc("README.md", "NEWS")
