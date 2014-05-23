#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import get

def install():
    shelltools.system("java -jar jedit5.3pre1install.jar auto %s/usr/share/java/jedit unix-script=%s/usr/bin unix-man=%s/usr/share/man" % (get.installDIR(), get.installDIR(), get.installDIR()))
