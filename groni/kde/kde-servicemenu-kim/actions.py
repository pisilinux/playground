#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

WorkDir = "kim4";
PkgSrcDir = get.workDIR() +"/"+ WorkDir


def setup():
    shelltools.chmod("src/*", 0644)
    shelltools.chmod("src/bin/*", 0755)
    shelltools.chmod("src/gallery/*", 0644)
    shelltools.chmod("src/slideshow/*", 0644)


def install():
    pisitools.dodoc("ChangeLog", "AUTHORS", "COPYING", "INSTALL", "README", "manual/work.css", "manual/index.html")
    pisitools.insinto("/usr/share/kim/", "README", "kim_about.txt")
    pisitools.insinto("/usr/share/kim/gallery/", "src/gallery/*")
    pisitools.insinto("/usr/share/kim/slideshow/", "src/slideshow/*")
    pisitools.insinto("/usr/share/kde4/services/ServiceMenus/", "src/*.desktop")

    # Just remove some unneded backup fles and installing binaries
    shelltools.cd(PkgSrcDir +"/src/bin/")
    for file in shelltools.ls("kim_*~"):
        shelltools.unlink(file)
    for file in shelltools.ls("kim_*"):
        pisitools.insinto("/usr/bin/", file)
