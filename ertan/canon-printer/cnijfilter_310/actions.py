#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

printer_models = ("mx860", "mx320", "mx330")
model_numbers = ("347", "348", "349")

WorkDir = "cnijfilter-source-3.10"

def setup():
    pass

def build():
    shelltools.cd("cnijfilter")
    for model in printer_models:
        shelltools.system("./autogen.sh --prefix=/%s --program-suffix=%s" % (get.defaultprefixDIR(), model))
        autotools.make()
        shelltools.move("src/cif", "src/cif%s" % model)
        autotools.make("clean")

def install():
    shelltools.cd("cnijfilter")
    for model in printer_models:
        pisitools.dobin("src/cif%s" % model)

    shelltools.cd("..")
    for model in model_numbers:
        pisitools.insinto("/usr/lib/bjlib", "%s/database/*" % model)
        pisitools.dolib("%s/libs_bin/*.so" % model)
    pisitools.insinto("/%s/share/cups/model" % get.defaultprefixDIR(), "ppd/*.ppd")

    pisitools.dodoc("LICENSE*")
