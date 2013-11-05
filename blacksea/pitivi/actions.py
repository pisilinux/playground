#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools
 
myfiles=["bin/pitivi.in","pitivi/utils/pipeline.py","pitivi/utils/signal.py","pitivi/undo/effect.py","pitivi/timeline/__init__.py"]

def setup():
      for i in myfiles:
          pisitools.dosed(i, "python2", "python")
          autotools.configure("--prefix=/usr --disable-static")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.dodoc("AUTHORS", "COPYING","README")
