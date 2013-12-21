#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir="ASTranslator-master"

def setup():
    shelltools.system("qmake Translator.pro")

def build():
    autotools.make()

def install():
    pisitools.dobin("bin/Translator")
    pisitools.dosym("/usr/bin/Translator", "/usr/bin/astranslator")

    pisitools.insinto("/usr/share/pixmaps", "src/res/icon.png", "astranslator.png")
    pisitools.insinto("/usr/share/icons/hicolor/128x128/apps", "src/res/icon-128.png", "astranslator.png")

    pisitools.dodoc("*.txt")