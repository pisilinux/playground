#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get

def build():
    autotools.make()

def install():
    autotools.rawInstall("BINDIR={0}/usr/bin LOCALEDIR={0}/usr/share/locale MANDIR={0}/usr/share/man".format(get.installDIR()))