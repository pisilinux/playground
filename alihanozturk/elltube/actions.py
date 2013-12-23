#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir="elltube-0.3"

def build():
    cmaketools.make()

def install():
    pisitools.insinto("usr/share/doc/elltube", "debian/copyright")
    pisitools.insinto("usr/share/doc/elltube", "debian/changelog")
    pisitools.insinto("usr/share/applications/", "elltube.desktop")
    pisitools.insinto("usr/share/elltube/", "elltube.py")
    pisitools.insinto("usr/share/elltube/atom/", "atom/__init__.py")
    pisitools.insinto("usr/share/elltube/atom/", "atom/service.py")
    pisitools.insinto("usr/share/elltube/gdata/", "gdata/__init__.py")
    pisitools.insinto("usr/share/elltube/gdata/", "gdata/auth.py")
    pisitools.insinto("usr/share/elltube/gdata/", "gdata/service.py")
    pisitools.insinto("usr/share/elltube/gdata/", "gdata/test_data.py")
    pisitools.insinto("usr/share/elltube/gdata/", "gdata/urlfetch.py")
    pisitools.insinto("usr/share/elltube/gdata/geo/", "gdata/geo/__init__.py")
    pisitools.insinto("usr/share/elltube/gdata/media/", "gdata/media/__init__.py")
    pisitools.insinto("usr/share/elltube/gdata/youtube/", "gdata/youtube/__init__.py")
    pisitools.insinto("usr/share/elltube/gdata/youtube/", "gdata/youtube/service.py")
    pisitools.insinto("usr/share/elltube/img/", "img/cancel.png")
    pisitools.insinto("usr/share/elltube/img/", "img/elltube.png")
    pisitools.insinto("usr/share/elltube/img/", "img/exit.png")
    pisitools.insinto("usr/share/elltube/img/", "img/folder.png")
    pisitools.insinto("usr/share/elltube/img/", "img/license.png")
    pisitools.insinto("usr/share/elltube/img/", "img/login.png")
    pisitools.insinto("usr/share/elltube/img/", "img/open.png")
    pisitools.insinto("usr/share/elltube/img/", "img/paste.png")
    pisitools.insinto("usr/share/elltube/img/", "img/save.png")
    pisitools.insinto("usr/share/elltube/img/", "img/settings.png")
    pisitools.insinto("usr/share/elltube/img/", "img/translators.png")
    pisitools.insinto("usr/share/elltube/locale/", "locale/ca.qm")
    pisitools.insinto("usr/share/elltube/locale/", "locale/de.qm")
    pisitools.insinto("usr/share/elltube/locale/", "locale/es.qm")
    pisitools.insinto("usr/share/elltube/locale/", "locale/fr.qm")
    pisitools.insinto("usr/share/elltube/locale/", "locale/it.qm")
    pisitools.insinto("usr/share/elltube/locale/", "locale/pl.qm")
    pisitools.insinto("usr/share/elltube/locale/", "locale/pt_BR.qm")
    pisitools.insinto("usr/share/elltube/locale/", "locale/sr.qm")
    pisitools.insinto("usr/share/elltube/locale/", "locale/sr@Latn.qm")