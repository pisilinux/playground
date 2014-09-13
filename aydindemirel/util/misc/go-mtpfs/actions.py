#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools

def install():
    pisitools.insinto("/usr/lib/go/src/pkg", "fs")
    pisitools.insinto("/usr/lib/go/src/pkg", "mtp")

    pisitools.dodoc("README","LICENSE")

