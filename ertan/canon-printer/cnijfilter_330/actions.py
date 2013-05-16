#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

printer_models = ("ip2700", "mx340", "mx350", "mx870")
model_numbers = ("364", "365", "366", "367")

def setup():
    shelltools.system("tar xvf MX340_Linux_Package.tar")
    shelltools.system("tar xvf cnijfilter-source-3.30-1.tar.gz")

def build():
    shelltools.cd("cnijfilter-source-3.30-1/cnijfilter")
    for model in printer_models:
        shelltools.system("./autogen.sh --prefix=/%s --program-suffix=%s" % (get.defaultprefixDIR(), model))
        autotools.make()
        shelltools.move("src/cif", "src/cif%s" % model)
        autotools.make("clean")

def install():
    shelltools.cd("cnijfilter-source-3.30-1/cnijfilter")
    for model in printer_models:
        pisitools.dobin("src/cif%s" % model)

    shelltools.cd("..")
    for model in model_numbers:
        pisitools.insinto("/usr/lib/bjlib", "%s/database/*" % model)
        pisitools.dolib("%s/libs_bin/*.so" % model)
    pisitools.insinto("/%s/share/cups/model" % get.defaultprefixDIR(), "ppd/*.ppd")

    pisitools.dodoc("LICENSE*")
