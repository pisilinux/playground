#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import block
import yali.util
import yali.context as ctx
from yali.storage.library import  LibraryError

class DeviceMapperError(LibraryError):
    pass

def name_from_dm_node(dm_node):
    name = block.getNameFromDmNode(dm_node)
    if name is not None:
        return name

    st = os.stat("/dev/%s" % dm_node)
    major = os.major(st.st_rdev)
    minor = os.minor(st.st_rdev)
    name = yali.util.run_batch("dmsetup", ["info", "--columns",
                               "--noheadings", "-o", "name",
                               "-j", str(major), "-m", str(minor)])[1]
    ctx.logger.debug("name_from_dm(%s) returning '%s'" % (dm_node, name.strip()))
    return name.strip()

def dm_node_from_name(name):
    dm_node = block.getDmNodeFromName(name)
    if dm_node is not None:
        return dm_node

    devnum = yali.util.run_batch("dmsetup", ["info", "--columns",
                        "--noheadings", "-o", "devno",name])[1]
    (major, sep, minor) = devnum.strip().partition(":")
    if not sep:
        raise DeviceMapperError("dm device does not exist")

    dm_node = "dm-%d" % int(minor)
    ctx.logger.debug("dm_node_from_name(%s) returning '%s'" % (name, dm_node))
    return dm_node

def _get_backing_devnums_from_map(map_name):
    ret = []
    buf = yali.util.run_batch("dmsetup",["info", "--columns", "--noheadings",
                              "-o", "devnos_used", map_name])[1]
    dev_nums = buf.split()
    for dev_num in dev_nums:
        (major, colon, minor) = dev_num.partition(":")
        ret.append((int(major), int(minor)))

    return ret

def get_backing_devnums(dm_node):
    #dm_node = dm_node_from_name(map_name)
    if not dm_node:
        return None

    top_dir = "/sys/block"
    backing_devs = os.listdir("%s/%s/slaves/" % (top_dir, dm_node))
    dev_nums = []
    for backing_dev in backing_devs:
        dev_num = open("%s/%s/dev" % (top_dir, backing_dev)).read().strip()
        (_major, _minor) = dev_num.split(":")
        dev_nums.append((int(_major), int(_minor)))

    return dev_nums

def get_backing_devs_from_name(map_name):
    dm_node = dm_node_from_name(map_name)
    if not dm_node:
        return None

    slave_devs = os.listdir("/sys/block/virtual/%s" % dm_node)
    return slave_devs
