#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pythonmodules
from pisi.actionsapi import pisitools
from pisi.actionsapi import kde4

kde5appsdir="/usr/share"
kde5docdir="/usr/share/doc"

def install():
    pythonmodules.install()

    # Copy Notification Rc file for Kde 5
    # pisitools.insinto("%s/package-manager/" % kde5appsdir, "src/package-manager.notifyrc")

    # for lang in ('de','en','es','fr','nl','sv','tr'):
     #    pisitools.insinto("%s/html/%s/package-manager/" % (kde5docdir, lang),
            #               "help/%s/main_help.html" % lang, "index.html")


