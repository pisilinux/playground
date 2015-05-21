#!/usr/bin/python

import os

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    os.system("gtk-query-immodules-3.0 --update-cache")
    os.system("glib-compile-schemas /usr/share/glib-2.0/schemas")
    os.system("gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor")
