#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WORKDIR = "%s-1" % get.srcDIR()
printer_models = ("mp250", "mp280", "mp495", "mg5100", "mg5200", "ip4800", "mg6100", "mg8100")
model_numbers = ("356", "369", "370", "373", "374", "375", "376", "377")

def setup():
    shelltools.cd("libs")
    shelltools.system("./autogen.sh --prefix=/%s" % get.defaultprefixDIR())
    shelltools.cd("../pstocanonij")
    shelltools.system("./autogen.sh --prefix=/%s --enable-progpath=/%s/bin" % (get.defaultprefixDIR(), get.defaultprefixDIR()))
    shelltools.cd("../backend")
    shelltools.system("./autogen.sh --prefix=/%s" % get.defaultprefixDIR())
    shelltools.cd("../backendnet")
    shelltools.system("./autogen.sh --prefix=/%s" % get.defaultprefixDIR())
    shelltools.cd("..")

def build():
    shelltools.cd("libs")
    autotools.make()
    shelltools.cd("../pstocanonij")
    autotools.make()
    shelltools.cd("../backend")
    autotools.make()
    shelltools.cd("../backendnet")
    autotools.make()

    shelltools.cd("../cnijfilter")
    for model in printer_models:
        shelltools.system("./autogen.sh --prefix=/%s --program-suffix=%s" % (get.defaultprefixDIR(), model))
        autotools.make()
        shelltools.move("src/cif", "src/cif%s" % model)
        autotools.make("clean")

    shelltools.cd("..")

def install():
    shelltools.cd("libs")
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    shelltools.cd("../pstocanonij")
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    shelltools.cd("../backend")
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    shelltools.cd("../backendnet")
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    shelltools.cd("../cnijfilter")
    for model in printer_models:
        pisitools.dobin("src/cif%s" % model)

    shelltools.cd("..")
    for model in model_numbers:
        pisitools.insinto("/usr/lib/bjlib", "%s/database/*" % model)
        if get.ARCH() == "i686":
            pisitools.dolib("%s/libs_bin%s/*.so" % (model, "32"))
        else:
            pisitools.dolib("%s/libs_bin%s/*.so" % (model, "64"))
    if get.ARCH() == "i686":
        pisitools.dolib("com/libs_bin%s/*.so" %  "32")
    else:
        pisitools.dolib("com/libs_bin%s/*.so" % "64")
    pisitools.insinto("/%s/share/cups/model" % get.defaultprefixDIR(), "ppd/*.ppd")

    pisitools.dodoc("LICENSE*")
