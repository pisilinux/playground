#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import piksemel

import bz2
import lzma
#install python-pyliblzma if you are using Pardus 2009
import urllib2

from collections import defaultdict


class UpdateRepoParser:

    def __init__(self, oldIndex, newIndex):

        self.oldIndex = oldIndex
        self.newIndex = newIndex

        self.pkgOld = {}
        self.pkgNew = {}

        self.obsoletesOld = []
        self.obsoletesNew = []

        self.replaces = defaultdict(list)
        self.remove = {}
        self.updateList = {}


    def createIndexes(self):
        repoRaw = self.getIndex(self.oldIndex)
        self.oldIndex = self.parseRepoIndex(repoRaw)

        repoRaw = self.getIndex(self.newIndex)
        self.newIndex = self.parseRepoIndex(repoRaw)


    def getIndex(self, uri):
        try:
            if "://" in uri:
                rawdata = urllib2.urlopen(uri).read()
            else:
                rawdata = open(uri, "r").read()
        except IOError:
            return None

        if uri.endswith("bz2"):
            data = bz2.decompress(rawdata)
        elif uri.endswith("xz") or uri.endswith("lzma"):
            data = lzma.decompress(rawdata)
        else:
            data = rawdata

        repoRaw = data
        return repoRaw


    def parseRepoIndex(self, index):
        doc = piksemel.parseString(index)
        return doc


    def getOldPackages(self):
        for pkg in self.oldIndex.tags("Package"):
            pkgName = pkg.getTagData("Name")
            pkgURI = pkg.getTagData("PackageURI")
            pkgRelease = pkg.getTag("History").getTag("Update").getAttribute("release")
            pkgVersion = pkg.getTag("History").getTag("Update").getTagData("Version")

            self.pkgOld[pkgName] = [pkgRelease, pkgVersion, pkgURI]


    def getNewPackages(self):
        #Get Packages from index
        for pkg in self.newIndex.tags("Package"):
            pkgName = pkg.getTagData("Name")
            pkgURI = pkg.getTagData("PackageURI")
            pkgRelease = pkg.getTag("History").getTag("Update").getAttribute("release")
            pkgVersion = pkg.getTag("History").getTag("Update").getTagData("Version")
            pkgDelta = {}

            if(pkg.getTag("Replaces")):
                for replace in pkg.tags("Replaces"):
                    self.replaces[replace.getTagData("Package")].append([pkgName, pkgRelease, pkgVersion, pkgURI])

            if(pkg.getTag("DeltaPackages")):
                for delta in pkg.getTag("DeltaPackages").tags("Delta"):
                    pkgDelta[delta.getAttribute("releaseFrom")] = delta.getTagData("PackageURI")

            self.pkgNew[pkgName] = [pkgRelease, pkgVersion, pkgDelta, pkgURI]


    def getDiffOfIndexes(self):
        for pkgName, attr in self.pkgOld.iteritems():
            if pkgName in self.pkgNew:
                pkgRelease = attr[0]
                if  pkgRelease != self.pkgNew[pkgName][0]:
                    if pkgRelease in self.pkgNew[pkgName][2]:
                        self.updateList[pkgName] = self.pkgNew[pkgName][2][pkgRelease]
                    else:
                        self.updateList[pkgName] = self.pkgNew[pkgName][3]
            else:
                self.remove[pkgName] = attr


    def addReplaces(self):
        for pkgName, attributes in self.replaces.iteritems():
            if pkgName in self.pkgOld:
                for attr in attributes:
                    if attr[0] not in self.updateList:
                        self.updateList[attr[0]] = attr[0]


    def createUpdateList(self):
        self.createIndexes()
        self.getOldPackages()
        self.getNewPackages()
        self.getDiffOfIndexes()
        self.addReplaces()


    def getUpdateList(self):
        self.createUpdateList()

        return self.updateList.values()


    def getObsoletes(self):
        self.__getObsolete__(self.oldIndex, self.obsoletesOld)
        self.__getObsolete__(self.newIndex, self.obsoletesNew)


    def __getObsolete__(self, index,  packages):
        #Get Obsoletes from index

        for pkg in index.getTag("Distribution").getTag("Obsoletes").tags("Package"):
            pkgName = pkg.firstChild().data()
            packages.append(pkgName)


if __name__ == "__main__":

    if len(sys.argv) > 2:
        oldIndex = sys.argv[1]
        newIndex = sys.argv[2]

    repoParser = UpdateRepoParser(oldIndex, newIndex)

    repoParser.getUpdateList()
    repoParser.getObsoletes()

    print "eski depo paket sayisi = ", len(repoParser.pkgOld)
    print "yeni depo paket sayisi = ", len(repoParser.pkgNew)
    print "eski depoda olup yeni depoda olmayan paket sayisi = ", len(repoParser.remove)
    print "guncellenecek paket sayisi = ", len(repoParser.updateList)
    print "eski depo obsolete paket sayisi = ", len(repoParser.obsoletesOld)
    print "yeni depo obsolete paket sayisi = ", len(repoParser.obsoletesNew)
