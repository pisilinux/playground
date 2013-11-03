#!/usr/bin/python

# Created For PisiLinux

from pisi.actionsapi import autotools, get, cmaketools, pisitools


def setup():
    cmaketools.configure()


def build():
    autotools.make("-j5")


def install():
    autotools.install()

    pisitools.dodoc("COPYING", "INSTALL", "ChangeLog", "README", "TODO")
