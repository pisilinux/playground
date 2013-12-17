#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

# if pisi can't find source directory, see /var/pisi/heimdall/work/ and:
# WorkDir="heimdall-"+ get.srcVERSION() +"/sub_project_dir/"

def setup():
    shelltools.cd("%s/libpit" % get.curDIR())
    autotools.configure("--prefix=/usr")
    shelltools.cd("..")
    shelltools.cd("%s/heimdall" % get.curDIR())
    autotools.configure("--prefix=/usr")
    shelltools.cd("..")
    shelltools.cd("%s/heimdall-frontend" % get.curDIR())
    autotools.system("qmake .")
    shelltools.cd("..")

def build():
    shelltools.cd("%s/libpit" % get.curDIR())
    autotools.make()
    shelltools.cd("..")
    shelltools.cd("%s/heimdall" % get.curDIR())
    autotools.make()
    shelltools.cd("..")
    shelltools.cd("%s/heimdall-frontend" % get.curDIR())
    autotools.make()
    shelltools.cd("..")

def install():
    shelltools.cd("%s/libpit" % get.curDIR())
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    shelltools.cd("..")    
    shelltools.cd("%s/heimdall" % get.curDIR())
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    shelltools.cd("..")
    shelltools.cd("%s/heimdall-frontend" % get.curDIR())   
    pisitools.insinto("/usr/bin","../Linux/heimdall-frontend")

# By PiSiDo 2.0.0
