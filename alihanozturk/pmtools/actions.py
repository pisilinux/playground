#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    # Don't build acpixtract as a newer one is shipped with acpica
    pisitools.dosed("Makefile", "acpixtract ", "")

def build():
    autotools.make()
    shelltools.cd("madt")
    autotools.make()

def install():
    pisitools.dosbin("acpidump/acpidump")
    pisitools.dosbin("madt/madt")
    pisitools.dosbin("turbostat/turbostat")

    pisitools.newdoc("madt/README", "README.madt")
    pisitools.dodoc("COPYING", "README")
