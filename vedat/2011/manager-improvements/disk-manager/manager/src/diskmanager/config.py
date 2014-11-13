#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2011 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# FS types and options
FS_TYPES = {
    "ext2": "Extended 2",
    "ext3": "Extended 3",
    "ext4": "Extended 4",
    "reiserfs": "Reiser FS",
    "xfs": "XFS",
    "ntfs-3g": "NTFS",
    "vfat": "Fat 16/32",
}

FS_OPTIONS = {
    "vfat": "quiet,shortname=mixed,dmask=007,fmask=117,utf8,gid=6",
    "ext2": "noatime",
    "ext3": "noatime",
    "ext4": "noatime",
    "ntfs-3g": "dmask=007,fmask=117,locale=tr_TR.UTF-8,gid=6",
    "reiserfs": "noatime",
    "xfs": "noatime",
}

# Animation
ANIM_SHOW, ANIM_HIDE = range(2)
ANIM_TIME = 200
ANIM_TARGET = 0
ANIM_DEFAULT = 16777215

