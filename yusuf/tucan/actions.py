#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

langs = ["cs", "de", "en", "es", "fr", "gr", "it", "pl", "pt", "ru", "se", "sk", "tr"]

def install():
    autotools.rawInstall("DESTDIR=%s/usr" % get.installDIR())

    for i in langs:
        pisitools.domo("i18n/%s/%s.po"% (i,i), i, "tucan.mo")
    pisitools.removeDir("usr/share/tucan/i18n")
    pisitools.remove("/usr/bin/tucan")
    pisitools.dosym("/usr/share/tucan/tucan.py","/usr/bin/tucan")
    pisitools.dodoc("CHANGELOG", "LICENSE", "README", "TODO", "VERSION")