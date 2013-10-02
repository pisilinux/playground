#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt 

from pisi.actionsapi import pisitools

def setup():

    print "xdman installing..."

def install():
    pisitools.dobin("xdman.sh")
    pisitools.insinto("/usr/share/xdman","xdman.jar")
    pisitools.insinto("/usr/share/xdman","icon.png")
    pisitools.dohtml("*.html")
    pisitools.dodoc("ReadMe.txt", "xdm-linux.txt")



