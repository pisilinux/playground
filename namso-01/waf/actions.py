#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    shelltools.system("./waf-light configure --prefix=/usr")

def build():
    shelltools.system("./waf-light --make-waf --strip --tools='compat,compat15,ocaml,go,cython,scala,erlang,cuda,gcj,boost,pep8'")

def install():
    shelltools.system("./waf-light install -f --destdir=%s" % get.installDIR())

    pisitools.dobin("waf")

    shelltools.cd("demos/c")
    shelltools.system("%s/usr/bin/waf configure build  >& /dev/null" % get.installDIR())
    shelltools.cd("../..")

    pisitools.dodoc("ChangeLog", "DEVEL", "README", "TODO")