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

import re
import sys
import yali.yalireadpiks as yaliReadPiks
from yali.localedata import *
from yali.users import *

class userErrors:
    def __init__(self):
        self.Empty=False
        self.Uname=False
        self.Rname=False
        self.Password=False
        self.Groups=False

class partitionErrors:
    def __init__(self):
        self.PartitionType=False
        self.Format=False
        self.Disk=False
        self.FsType=False
        self.MountPoint=False

class errors:
    def __init__(self):
        self.Keymap=False
        self.Lang=False
        self.Root=False
        self.Users=False
        self.Empty=False
        self.Disk=False
        self.Root=False
        self.TotalRatio=False

class userFunctions:
    def __init__(self,username,groups,correctdata):
        self.username=username
        self.groups=groups
        self.correctData = correctdata

    def checkAutologin(self):
        """It verifies if another autologin user exists"""
        if self.correctData.autoLoginUser:
            return False
        return True

    def checkValidity(self):
        """It checks username format"""
        if self.username and re.search("[0-9a-zA-Z.?!_-]",self.username):
            return True
        return False

    def checkName(self):
        """It verifies if the username already exists"""
        for usr in self.correctData.users:
            if usr.username==self.username:
                return True
        return False

    def checkGroups(self):
        """It checks the groups validity"""
        for element in self.groups:
            for group in kahya().defaultGroups:
                if group==element or element=="wheel":
                    break
            else:
                return element
        else:
            return False

class otherFunctions:
    def __init__(self,keyX):
        self.keyX=keyX

    def checkKeymapX(self):
        """It checks keymap validity"""
        for country, data in locales.items():
            if data["xkblayout"] == self.keyX:
                return True
        return False

    def findKeymap(self):
        """It attaches console Keymap"""
        for country,data in locales.items():
            if data["xkblayout"] == self.keyX:
                return data["consolekeymap"]
        return False

class partitionFunctions:
    def __init__(self,fs,disk):
        self.fs=fs
        self.disk=disk

    def checkFileSystem(self):
        for element in kahya().fileSystems:
            if element==self.fs:
                return True
        return False

    def checkFileSystem2(self):
        for element in kahya().fileSystems2:
            if element == self.fs:
                return True
        return False

    def checkDiskSyntax(self):
        return re.match("disk[0-9]p[1-9]$",self.disk) 

    def checkDiskSyntax2(self):
        return re.match("disk[0-9]$",self.disk) 

class kahya:
    def __init__(self):
        self.fileSystems=["swap","ext4","ext3","ntfs","reiserfs","xfs"]
        self.fileSystems2=["ext4","ext3","xfs"]
        self.defaultGroups=["audio","dialout","disk","pnp","power","users","video","lp","lpadmin","cdrom","floppy"]
        self.errorList=[]
        self.RatioList=[]
        self.correctData=yaliReadPiks.kahyaData()
        self.total=0

    def readData(self,kahyaFile):
        self.filePath = kahyaFile
        self.data = yaliReadPiks.read(kahyaFile)

    def checkRatio(self):
        """ It checks partition ratios """
        for eachRatio in self.data.partitioning:
            self.RatioList.append(eachRatio.ratio)
        for i in self.RatioList:
            self.total+=int(i)
        if self.total==100:
            return True
        return False

    def checkAllOptions(self):
        """It checks all data entries and edits them"""
        error=errors()
        otherFunct=otherFunctions(self.data.keyData["xkblayout"])

        ###repo selection###
        if self.data.repoAddr:
            self.correctData.repoAddr = self.data.repoAddr
            self.correctData.repoName = self.data.repoName

        # TimeZone
        if self.data.timezone:
            self.correctData.timezone = self.data.timezone

        ###language selection###
        if locales.has_key(self.data.language):
            self.correctData.language=self.data.language
        else:
            error.Lang=True
            self.errorList.append("Language Error: %s does not exist"%self.data.language)

        ###keymap selection###
        if self.data.keyData["xkblayout"]:
            if otherFunct.checkKeymapX():
                self.correctData.keyData = self.data.keyData
                #self.correctData.keyData["consolekeymap"]=otherFunct.findKeymap()
            else:
                error.Keymap=True
                self.errorList.append("Keymap Error: %s not valid " % self.data.keyData["xkblayout"])
        else:
            if error.Lang!=True:
                error.Keymap=True
                self.errorList.append("Keymap Error: Cannot associate Keymap for %s"%self.data.language)

        ###root password selection###
        if len(self.data.rootPassword)<4:
            if not self.data.useYaliFirstBoot:
                error.Root=True
                self.errorList.append("Root Password Error : Password is too short")
        else:
            self.correctData.rootPassword=self.data.rootPassword

        ###hostname selection###
        if self.data.hostname:
            self.correctData.hostname=self.data.hostname
        else:
            self.correctData.hostname="pardus"

        ###users selections###
        if len(self.data.users)==0:
            if not self.data.useYaliFirstBoot:
                error.Users=True
                self.errorList.append("User Error: No user entry")
        else:
            self.correctData.users=[]
            for user in self.data.users:
                userError=userErrors()
                correctUser=User()
                checkFunctions=userFunctions(user.username,user.groups,self.correctData)
                if user.autologin=="yes" and checkFunctions.checkAutologin():
                    self.correctData.autoLoginUser=user.username
                if user.username=="root" or not checkFunctions.checkValidity()==True or checkFunctions.checkName()==True:
                    userError.Uname=True
                    if (user.username and userError.Uname==True):
                        self.errorList.append("Username Error for %s : username already exist or not valid"%user.username)
                    else:
                        self.errorList.append("Username Error : no Entry")
                if not user.realname:
                    userError.Rname=True
                    if userError.Uname!=True:
                        self.errorList.append("Real name Error for %s: No entry"%user.username)
                if (len(user.password)<4 or user.username==user.password or user.realname==user.password):
                    userError.Password=True
                    if userError.Uname!=True:
                        self.errorList.append("Password Error for %s "%user.username)
                if len(user.groups)==0:
                    user.groups=self.defaultGroups
                elif (checkFunctions.checkGroups()):
                    self.errorList.append("Groups Error for %s : %s group not valid"%(user.username,checkFunctions.checkGroups()))
                    userError.Groups=True
                if(userError.Uname!=True and userError.Rname!=True and userError.Password!=True and userError.Groups!=True):
                    correctUser.username=user.username
                    correctUser.realname=user.realname
                    correctUser.passwd=user.password
                    correctUser.groups=user.groups
                    self.correctData.users.append(correctUser)

        if len(self.correctData.users)==0 and not self.data.useYaliFirstBoot:
            error.Users=True
            self.errorList.append("User Error: No user added")

        ###partitioning selection###
        correctPart=yaliReadPiks.yaliPartition()
        if (self.data.partitioningType in ["auto","smartAuto"]):
            self.correctData.partitioningType=self.data.partitioningType
            if(len(self.data.partitioning)!=1):
                error.Empty=True
                self.errorList.append("Auto Partitioning Error : No partition entry or too many partition")
            else:
                PartiFunction=partitionFunctions(self.data.partitioning[0].fsType,self.data.partitioning[0].disk)
                if not PartiFunction.checkDiskSyntax2():
                    error.Disk=True
                    self.errorList.append("Auto Partitioning Error : Wrong Disk Syntax")
                else:
                    correctPart.disk=self.data.partitioning[0].disk
                    if self.correctData.partitioningType == "auto":
                        correctPart.partitionType="pardus_root"
                        correctPart.format="true"
                        correctPart.formatType="full"
                        correctPart.ratio="100"
                    self.correctData.partitioning.append(correctPart)

        elif self.data.partitioningType=="manual":
            self.correctData.partitioningType="manual"

            if len(self.data.partitioning)==0:
                error.Empty=True
                self.errorList.append("Manual Partitioning Error : No partition entry ")
            else:
                for partitionRoot in self.data.partitioning:
                    if partitionRoot.partitionType=="pardus_root": #pardus_root is required
                        break
                else:
                    error.Root=True
                    self.errorList.append("Manual Partitioning Error : \"pardus_root\" missing ")
                if not self.checkRatio()==True:
                    error.TotalRatio=True
                    self.errorList.append(" Ratio Error : Total not equal to 100")
                else:
                    if(error.Empty!=True and error.Root!=True):
                        for partition in self.data.partitioning:
                            errorPartition=partitionErrors()
                            functPart=partitionFunctions(partition.fsType,partition.disk)
                            if not partition.partitionType in["pardus_root","pardus_swap","pardus_home","other"]:
                                errorPartition.PartitionType=True
                                self.errorList.append("Partition type Error :%s not valid"%partition.partitionType)
                            if not partition.format=="false":
                                partition.format="true"
                            if not functPart.checkDiskSyntax():
                                errorPartition.Disk=True
                                self.errorList.append(" Disk Error for %s: %s not valid"%(partition.partitionType,partition.disk))
                            if not partition.partitionType=="other":
                                if not functPart.checkFileSystem2():
                                    errorPartition.FsType=True
                                    self.errorList.append("File system Error for %s : %s not valid"%(partition.partitionType,partition.fsType))
                            else:
                                if not functPart.checkFileSystem():
                                    errorPartition.FsType=True
                                    self.errorList.append("File system Error for %s : %s not valid"%(partition.partitionType,partition.fsType))
                            if not partition.mountPoint==None  and not(re.search("[a-zA-Z0-9]",partition.mountPoint)) :
                                errorPartition.MountPoint=True
                                self.errorList.append("Mountpoint Error for %s : %s not valid"%(partition.partitionType,partition.mountPoint))
                            if not errorPartition.PartitionType==True and\
                               not errorPartition.Disk==True and\
                               not errorPartition.FsType==True and\
                               not errorPartition.MountPoint==True:
                                self.correctData.partitioning.append(partition)

        return self.errorList

    def checkFileValidity(self):
        """It reads the xml file and checks errors"""
        self.correctData=yaliReadPiks.kahyaData()
        self.errorList=self.checkAllOptions()
        if(len(self.errorList)==0):
            return True
        return self.errorList

    def getValues(self):
        if self.checkFileValidity() == True:
            return self.correctData
        return self.errorList

