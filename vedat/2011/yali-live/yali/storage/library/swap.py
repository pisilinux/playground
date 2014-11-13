#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import resource
import gettext

__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import yali.util
from yali.storage.library import devicemapper
from yali.storage.library import  LibraryError

class SwapError(LibraryError):
    pass

class OldSwapError(SwapError):
    pass

class UnknownSwapError(SwapError):
    pass

class SuspendError(SwapError):
    pass

def mkswap(device, label=''):
    # We use -f to force since mkswap tends to refuse creation on lvs with
    # a message about erasing bootbits sectors on whole disks. Bah.
    argv = ["-f"]
    if label:
        argv.extend(["-L", label])
    argv.append(device)

    rc = yali.util.run_batch("mkswap", argv)[0]

    if rc:
        raise SwapError("mkswap failed for '%s'" % device)

def swapon(device, priority=None):
    pagesize = resource.getpagesize()
    buf = None
    sig = None

    if pagesize > 2048:
        num = pagesize
    else:
        eum = 2048

    try:
        fd = os.open(device, os.O_RDONLY)
        buf = os.read(fd, num)
    except OSError:
        pass
    finally:
        try:
            os.close(fd)
        except (OSError, UnboundLocalError):
            pass

    if buf is not None and len(buf) == pagesize:
        sig = buf[pagesize - 10:]
        if sig == 'SWAP-SPACE':
            raise OldSwapError
        if sig == 'S1SUSPEND\x00' or sig == 'S2SUSPEND\x00':
            raise SuspendError

    if sig != 'SWAPSPACE2':
        raise UnknownSwapError

    argv = []
    if isinstance(priority, int) and 0 <= priority <= 32767:
        argv.extend(["-p", "%d" % priority])
    argv.append(device)
    rc = yali.util.run_batch("swapon",argv)[0]

    if rc:
        raise SwapError("swapon failed for '%s'" % device)

def swap_off(device):
    rc = yali.util.run_batch("swapoff", [device])[0]

    if rc:
        raise SwapError("swapoff failed for '%s'" % device)

def swap_status(device):
    alt_dev = None
    if device.startswith("/dev/mapper/"):
        # get the real device node for device-mapper devices since the ones
        # with meaningful names are just symlinks
        try:
            alt_dev = "/dev/%s" % devicemapper.dm_node_from_name(device.split("/")[-1])
        except devicemapper.DeviceMapperError:
            alt_dev = None

    lines = open("/proc/swaps").readlines()
    status = False
    for line in lines:
        if not line.strip():
            continue

        swap_dev = line.split()[0]
        if swap_dev in [device, alt_dev]:
            status = True
            break

    return status
