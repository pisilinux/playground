#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

def install():
    pisitools.insinto("/opt/sublime-text","*")
    for i in [16,32,48,128,256]:
        pisitools.domove("/opt/sublime-text/Icon/{0}x{0}/sublime_text.png".format(i),"/usr/share/icons/hicolor/{0}x{0}/apps".format(i))
    pisitools.removeDir("/opt/sublime-text/Icon")
    pisitools.removeDir("/opt/sublime-text/lib")
    for i in ['-','_']:
        pisitools.dosym("/opt/sublime-text/sublime_text","/usr/bin/sublime%stext" % i)
