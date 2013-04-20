#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = 'android-notifier-desktop'

def install():
    pisitools.insinto('/opt/android-notifier-desktop', 'lib')
    pisitools.insinto('/opt/android-notifier-desktop', 'android-notifier-desktop.jar')
    pisitools.insinto('/usr/bin', 'run.sh', 'android-notifier-desktop')

    pisitools.insinto('/usr/share/pixmaps/', 'icons/android-notifier-desktop.png')
    pisitools.insinto('/usr/share/pixmaps/android-notifier-desktop', 'icons/*.png')
    pisitools.remove('/usr/share/pixmaps/android-notifier-desktop/android-notifier-desktop.png')

