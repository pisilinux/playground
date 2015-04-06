#!/usr/bin/python
# -*- coding: utf-8 -*-

from pisi.actionsapi import get
from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools

NoStrip=["/usr/bin/ocamlfind"]

def setup():
    autotools.rawConfigure("-bindir /usr/bin -mandir /usr/share/man -config /etc/findlib.conf -sitelib /usr/lib/ocaml/site-lib")

def build():
    autotools.make("all")
    autotools.make("opt")

def install():
    shelltools.makedirs("%s/etc" % get.installDIR())
    autotools.rawInstall("prefix=%s" %get.installDIR())
