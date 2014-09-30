#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools

def setup():
    options = "\
                 --disable-static \
                 --disable-silent-rules \
                 --with-libjasper \
                 --with-x11 \
                 --with-libpng \
                 --with-libtiff \
                 --with-libjpeg \
                 --enable-introspection \
                 --with-included-loaders=png \
              "

    autotools.configure(options)


def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
  
    pisitools.dodoc("AUTHORS", "COPYING", "NEWS", "README")
