#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import perlmodules
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    perlmodules.configure("INSTALLDIRS=vendor \
                           PERL_MM_USE_DEFAULT=1")

def build():
    perlmodules.make()

def check():
    perlmodules.make("test")

def install():
    perlmodules.install("pure_install doc_install")

    pisitools.dodoc("README","Changes")
