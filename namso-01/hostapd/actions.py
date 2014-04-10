#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

def build():
    shelltools.cd("hostapd")
    shelltools.system("sed -i 's#/etc/hostapd#/etc/hostapd/hostapd#' hostapd.conf")
    autotools.make()

def install():
    shelltools.cd("hostapd")
    pisitools.dobin("hostapd")
    pisitools.dobin("hostapd_cli")
    
    pisitools.doman("hostapd.8")
    pisitools.doman("hostapd_cli.1")
    
    pisitools.insinto("/etc/hostapd/", "wired.conf")
    pisitools.insinto("/etc/hostapd/", "hostapd.deny")
    pisitools.insinto("/etc/hostapd/", "hostapd.conf")
    pisitools.insinto("/etc/hostapd/", "hostapd.vlan")
    pisitools.insinto("/etc/hostapd/", "hostapd.sim_db")
    pisitools.insinto("/etc/hostapd/", "hostapd.accept")
    pisitools.insinto("/etc/hostapd/", "hostapd.wpa_psk")
    pisitools.insinto("/etc/hostapd/", "hostapd.eap_user")
    pisitools.insinto("/etc/hostapd/", "hlr_auc_gw.milenage_db")
    pisitools.insinto("/etc/hostapd/", "hostapd.radius_clients")
    
    shelltools.cd("..")
    pisitools.dodoc("COPYING", "README")
