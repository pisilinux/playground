#!/usr/bin/python
# -*- coding: utf-8 -*- 
#
# Copyright 2005 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# S.Çağlar Onur <caglar@pardus.org.tr>

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "preload"

def build():
    autotools.make("CFLAGS=\"%s\"" % get.CFLAGS())

def install():
    pisitools.dosbin("preload", "/sbin")
    pisitools.dosbin("print-bmap", "/sbin")
    
    pisitools.dobin("preload.sh")
    pisitools.dosbin("parse_strace")
    pisitools.dosbin("prepare_preload_file")
    
    pisitools.doexe("preload.desktop", "/usr/share/autostart/")
