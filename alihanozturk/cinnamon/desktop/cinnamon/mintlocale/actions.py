#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools

def install():
    shelltools.system("./makepot")
    pisitools.insinto("/usr/share/applications/", "usr/share/applications/mintLocale.desktop")
    pisitools.insinto("/usr/bin/", "usr/bin/*")
    pisitools.insinto("/usr/lib/linuxmint/mintLocale/flags/16/languages/", "usr/lib/linuxmint/mintLocale/flags/16/languages/eo.png")
    pisitools.insinto("/usr/lib/linuxmint/mintLocale/flags/16/", "usr/lib/linuxmint/mintLocale/flags/16/*.png")
    pisitools.insinto("/usr/lib/linuxmint/mintLocale/", "usr/lib/linuxmint/mintLocale/*.py")
    pisitools.insinto("/usr/lib/linuxmint/mintLocale/", "usr/lib/linuxmint/mintLocale/*.ui")
    pisitools.insinto("/usr/lib/linuxmint/mintLocale/", "usr/lib/linuxmint/mintLocale/countries")
    pisitools.insinto("/usr/lib/linuxmint/mintLocale/", "usr/lib/linuxmint/mintLocale/default_locale.template")
    pisitools.insinto("/usr/lib/linuxmint/mintLocale/", "usr/lib/linuxmint/mintLocale/languages")