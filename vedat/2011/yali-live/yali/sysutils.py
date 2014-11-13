# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# sysutils module provides basic system utilities

import os
import sys
import string
import time
import subprocess
import random
import hashlib
import gettext

__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import _sysutils

def available_space(path):
    return _sysutils.device_space_free(path)

def ext2IsDirty(device):
    label = _sysutils.e2dirty(device)
    return label

def ext2HasJournal(device):
    hasjournal = _sysutils.e2hasjournal(device)
    return hasjournal

def checkKernelFlags(flag):
    for line in open("/proc/cpuinfo", "r").readlines():
        if line.startswith("flags"):
            return flag in line

def isLoadedKernelPAE():
    if os.uname()[2].split("-")[-1].__eq__("pae"):
        return True
    else:
        return False

def setMouse(key="left"):
    struct = {_("left") :"1 2 3",
              _("right"):"3 2 1"}
    os.system("xmodmap -e \"pointer = %s\"" % struct[key])

    # Fix for TouchPads in left handed mouse...
    if key == "right":
        os.system("synclient TapButton1=3 TapButton3=1")

def liveMediaSystem(path=None):
    if not path:
        path  = "/var/run/pardus/livemedia"
    if os.path.exists(path):
        return file("/var/run/pardus/livemedia", 'r').read().split('\n')[0]
    else:
        return None


def getShadowed(passwd):
    des_salt = list('./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') 
    salt, magic = str(random.random())[-8:], '$1$'

    ctx = hashlib.new('md5', passwd)
    ctx.update(magic)
    ctx.update(salt)

    ctx1 = hashlib.new('md5', passwd)
    ctx1.update(salt)
    ctx1.update(passwd)

    final = ctx1.digest()

    for i in range(len(passwd), 0 , -16):
        if i > 16:
            ctx.update(final)
        else:
            ctx.update(final[:i])

    i = len(passwd)

    while i:
        if i & 1:
            ctx.update('\0')
        else:
            ctx.update(passwd[:1])
        i = i >> 1
    final = ctx.digest()

    for i in range(1000):
        ctx1 = hashlib.new('md5')
        if i & 1:
            ctx1.update(passwd)
        else:
            ctx1.update(final)
        if i % 3: ctx1.update(salt)
        if i % 7: ctx1.update(passwd)
        if i & 1:
            ctx1.update(final)
        else:
            ctx1.update(passwd)
        final = ctx1.digest()

    def _to64(v, n):
        r = ''
        while (n-1 >= 0):
            r = r + des_salt[v & 0x3F]
            v = v >> 6
            n = n - 1
        return r

    rv = magic + salt + '$'
    final = map(ord, final)
    l = (final[0] << 16) + (final[6] << 8) + final[12]
    rv = rv + _to64(l, 4)
    l = (final[1] << 16) + (final[7] << 8) + final[13]
    rv = rv + _to64(l, 4)
    l = (final[2] << 16) + (final[8] << 8) + final[14]
    rv = rv + _to64(l, 4)
    l = (final[3] << 16) + (final[9] << 8) + final[15]
    rv = rv + _to64(l, 4)
    l = (final[4] << 16) + (final[10] << 8) + final[5]
    rv = rv + _to64(l, 4)
    l = final[11]
    rv = rv + _to64(l, 2)

    return rv

