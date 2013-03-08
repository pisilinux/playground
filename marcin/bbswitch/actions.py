#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import kerneltools

KDIR = kerneltools.getKernelVersion()

#def setup():
#    autotools.configure()

def build():
    autotools.make("KDIR=/lib/modules/%s/build" % KDIR)

def install():
#    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
     pisitools.insinto("/lib/modules/3.2.5/kernel/drivers/acpi", "bbswitch.ko")

# Take a look at the source folder for these file as documentation.
#    pisitools.dodoc("AUTHORS", "BUGS", "ChangeLog", "COPYING", "README")
# If there is no install rule for a runnable binary, you can 
# install it to binary directory.
#    pisitools.dobin("bbswitch")
