#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "."

def build():
    shelltools.cd("FlickrNet")
    shelltools.system("xbuild  /property:Configuration=Release FlickrNet.csproj")

def install():
    shelltools.cd("FlickrNet")
    shelltools.system("gacutil -i bin/Release/FlickrNet.dll -package flickrnet-3.10.0 -root %s/usr/lib/" % get.installDIR())