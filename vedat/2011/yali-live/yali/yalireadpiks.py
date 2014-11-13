#!/usr/bin/python
#
# Copyright (C) 2007-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import piksemel
import sys
import yali.localedata

class kahyaData:
    def __init__(self):
        self.language=None
        self.keyData={"xkblayout":"tr",
                      "xkbvariant":"q",
                      "consolekeymap":"trq"}
        self.rootPassword=''
        self.hostname=None
        self.users=[]
        self.partitioning=[]
        self.partitioningType=None
        self.autoLoginUser=None
        self.repoName = "remoteRepo"
        self.repoAddr = None
        self.timezone = "Europe/Istanbul"
        self.useYaliFirstBoot = False

class yaliUser:
    def __init__(self):
        self.autologin=None
        self.username=None
        self.realname=None
        self.password=None
        self.groups=[]

class yaliPartition:
    def __init__(self):
        self.partitionType=None
        self.format=None
        self.formatType="useAvail"
        self.ratio=None
        self.disk=None
        self.fsType=None
        self.mountPoint=None

def read(args):
    doc=piksemel.parse(args)
    data=kahyaData()
    data.language=doc.getTagData("language")
    data.keyData = yali.localedata.locales[data.language]
    _xkblayout = data.keyData["xkblayout"]
    data.keyData["xkblayout"]=doc.getTagData("keymap") or data.keyData["xkblayout"]
    if data.keyData["xkblayout"] != _xkblayout:
        data.keyData["xkbvariant"] = None
    if data.keyData["xkbvariant"]:
        data.keyData["xkbvariant"]=doc.getTagData("variant") or data.keyData["xkbvariant"][0][0]
    data.rootPassword=doc.getTagData("root_password") or ''
    data.hostname=doc.getTagData("hostname")
    data.timezone=doc.getTagData("timezone")
    data.repoName=doc.getTagData("reponame") or data.repoName
    data.repoAddr=doc.getTagData("repoaddr")
    usrsTag=doc.getTag("users")
    data.useYaliFirstBoot=usrsTag.getAttribute("first_boot") or False

    for p in usrsTag.tags():
        info=yaliUser()
        info.autologin=p.getAttribute("autologin")
        info.username=p.getTagData("username")
        info.realname=p.getTagData("realname")
        info.password=p.getTagData("password")
        if(p.getTagData("groups")!=None):
            info.groups=p.getTagData("groups").split(",")
        data.users.append(info)

    partitioning=doc.getTag("partitioning")
    data.partitioningType=partitioning.getAttribute("partitioning_type")
    if(data.partitioningType in ["auto","smartAuto"]):
        autoPart=yaliPartition()
        autoPart.disk=partitioning.firstChild().data()
        data.partitioning.append(autoPart)
    elif(data.partitioningType=="manual"):
        for q in partitioning.tags():
            partinfo=yaliPartition()
            partinfo.partitionType=q.getAttribute("partition_type")
            partinfo.format=q.getAttribute("format")
            partinfo.ratio=q.getAttribute("ratio")
            partinfo.fsType=q.getAttribute("fs_type")
            partinfo.mountPoint=q.getAttribute("mountpoint")
            partinfo.disk=q.firstChild().data()
            data.partitioning.append(partinfo)
    return data

