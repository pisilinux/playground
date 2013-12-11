#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools

# if pisi can't find source directory, see /var/pisi/pngcrush/work/ and:
# WorkDir="pngcrush-"+ get.srcVERSION() +"/sub_project_dir/"

def build():
    autotools.make()

def install():
    pisitools.dodir("/usr")
    pisitools.insinto("/usr/bin","pngcrush")
    pisitools.insinto("/usr/share/pngcrush-1.7.69/doc","ChangeLog.html")
# By PiSiDo 2.0.0
