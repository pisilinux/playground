#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/old-licenses/gpl.txt

from pisi.actionsapi import autotools

def setup():
    autotools.configure()

def build():
    autotools.make("V=1")

def install():
    autotools.install()
