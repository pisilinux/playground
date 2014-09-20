#!/usr/bin/python

import os

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
	if not os.listdir("/etc/dropbear"):
		os.system("/usr/bin/dropbearkey -t rsa -f /etc/dropbear/dropbear_rsa_host_key")
		os.system("/usr/bin/dropbearkey -t dss -f /etc/dropbear/dropbear_dss_host_key")

def postRemove():
	if not os.listdir("/etc/dropbear"):
		os.rmdir("/etc/dropbear")
