#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

def setup():
    pisitools.flags.add("-fwrapv")

    #pisitools.dosed("Lib/cgi.py","^#.* /usr/local/bin/python","#!/usr/bin/python")
    #shelltools.system("find . -name '*.py' | xargs -r grep -El '^#! */usr/bin/env python3?' | xargs sed -i -e '1s,^#! */usr/bin/env python3\?,#!/usr/bin/python3,'")
    shelltools.unlinkDir("Modules/expat")
    shelltools.unlinkDir("Modules/zlib")
    shelltools.unlinkDir("Modules/_ctypes/darwin")
    shelltools.unlinkDir("Modules/_ctypes/libffi")
    shelltools.unlinkDir("Modules/_ctypes/libffi_arm_wince")
    shelltools.unlinkDir("Modules/_ctypes/libffi_msvc")
    shelltools.unlinkDir("Modules/_ctypes/libffi_osx")

    autotools.rawConfigure("\
                            --prefix=/usr \
                            --enable-ipv6 \
                            --enable-shared \
                            --enable-loadable-sqlite-extensions \
                            --with-fpectl \
                            --with-computed-gotos \
                            --with-dbmliborder=gdbm:ndbm \
                            --with-tsc \
                            --with-signal-module \
                            --with-system-expat \
                            --with-system-ffi \
                            --with-system-libmpdec \
                            --with-threads \
                            --with-valgrind \
                            --without-ensurepip \
                           ")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.remove("/usr/bin/2to3")
    #pisitools.insinto("/usr/include/", "/usr/include/python3.4m", "python3.4")
    pisitools.dodoc("LICENSE", "README")
