#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "."
    
def setup():
    
    shelltools.system("mkdir -p %s/calibre-1.15.0-x86_64" % get.workDIR())
    
def build():    
    
    #shelltools.system("cd %s/calibre-1.15.0-x86_64" % get.workDIR())
    shelltools.move("bin","calibre-1.15.0-x86_64")
    shelltools.move("lib","calibre-1.15.0-x86_64")
    shelltools.move("resources","calibre-1.15.0-x86_64")
    shelltools.move("calibre","calibre-1.15.0-x86_64")
    shelltools.move("calibre-complete","calibre-1.15.0-x86_64")
    shelltools.move("calibre-customize","calibre-1.15.0-x86_64")
    shelltools.move("calibre-debug","calibre-1.15.0-x86_64")
    shelltools.move("calibre-parallel","calibre-1.15.0-x86_64")
    shelltools.move("calibre-server","calibre-1.15.0-x86_64")
    shelltools.move("calibre-smtp","calibre-1.15.0-x86_64")
    shelltools.move("calibre_postinstall","calibre-1.15.0-x86_64")
    shelltools.move("calibredb","calibre-1.15.0-x86_64")
    shelltools.move("ebook-convert","calibre-1.15.0-x86_64")
    shelltools.move("ebook-device","calibre-1.15.0-x86_64")
    shelltools.move("ebook-edit","calibre-1.15.0-x86_64")
    shelltools.move("ebook-meta","calibre-1.15.0-x86_64")
    shelltools.move("ebook-polish","calibre-1.15.0-x86_64")
    shelltools.move("ebook-viewer","calibre-1.15.0-x86_64")
    shelltools.move("fetch-ebook-metadata","calibre-1.15.0-x86_64")
    shelltools.move("lrf2lrs","calibre-1.15.0-x86_64")
    shelltools.move("lrfviewer","calibre-1.15.0-x86_64")
    shelltools.move("lrs2lrf","calibre-1.15.0-x86_64")
    shelltools.move("markdown-calibre","calibre-1.15.0-x86_64")
    shelltools.move("web2disk","calibre-1.15.0-x86_64")

def install():        
    pisitools.dodir("/opt")
    pisitools.insinto("/opt","%s/*" % get.workDIR())
    pisitools.remove("/opt/pisiBuildState")

    

# By PiSiDo 2.0.0
