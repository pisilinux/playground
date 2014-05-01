#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    autotools.autoreconf("-fi")
    shelltools.chmod("autogen.sh",0755)
    shelltools.system("NOCONFIGURE=1 ./autogen.sh")
    autotools.configure("--disable-static \
                         --disable-systemd \
                         --disable-update-mimedb \
                         --with-libsocialweb=no \
                         --disable-cups \
                         --enable-ibus")
    
    pisitools.dosed("libtool", "( -shared )", " -Wl,-O1,--as-needed\\1")
    pisitools.dosed("libtool", '(    if test "\$export_dynamic" = yes && test -n "\$export_dynamic_flag_spec"; then)', '      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\\1')

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("README", "COPYING", "AUTHORS")