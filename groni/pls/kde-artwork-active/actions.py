#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import get
#from pisi.actionsapi import pisitools

# if pisi can't find source directory, see /var/pisi/kde-artwork-active/work/ and:
# WorkDir="kde-artwork-active-"+ get.srcVERSION() +"/sub_project_dir/"

def setup():
    cmaketools.configure("-DCMAKE_BUILD_TYPE=release", installPrefix="/usr")

def build():
    cmaketools.make()

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())



# By PiSiDo 2.0.0
