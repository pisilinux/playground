#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get

def build():
    autotools.make("OPT_CFLAGS='%{optflags}'")

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())