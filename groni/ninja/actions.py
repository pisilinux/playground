#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pythonmodules
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

#WorkDIR = "ninja-1.5.1" % get.srcVERSION()

def build():
    pythonmodules.configure("./bootstrap.py \
                          --emacs -Q --batch -f batch-byte-compile misc/ninja-mode.el \
                          --asciidoc doc/manual.asciidoc")

def check():
    pythonmodules.check("python2 ./configure.py --with-gtest=/usr/src/gtest\
                        -./ninja ninja_test\
                        -./ninja_test --gtest_filter=-SubprocessTest.SetWithLots")

def install():
    pythonmodules.install("install -m755 -D ninja $pkdir/usr/bin/ninja"
                          -"install -m644 -D doc/manual.asciidoc $pkgdir/usr/share/doc/ninja/manual.asciidoc"
                          -"install -m644 -D doc/manual.html $pkgdir/usr/share/doc/ninja/manual.html"
                          -" install -m644 -D misc/ninja-mode.el $pkgdir/usr/share/emacs/site-lisp/ninja-mode.el"
                          -"install -m644 -D misc/ninja-mode.elc $pkgdir/usr/share/emacs/site-lisp/ninja-mode.elc"
                          -"install -m644 -D misc/bash-completion $pkgdir/usr/share/bash-completion/completions/ninja"
                          -"install -m644 -D misc/zsh-completion $pkgdir/usr/share/zsh/site-functions/_ninja")

    pisitools.dodoc("HACKING.md", "COPYING", "RELEASING", "README")
