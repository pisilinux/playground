#!/usr/bin/python
# -*- coding: utf-8 -*-

# pisi-index.xml.xz dosyalarından paketleri veritabanına kaydeden script.
# ekledigi indexlerin sha1sumlarını veritabanına kaydeder, degisme durumunda degisiklikleri
# veritabanını pisi-index.xml'e eşitler.

# paket içeriklerinde degisiklik olup olmadıgını pisi-index.xml'deki paketlerin sha1sum kısımlarından
# karar verir. degisiklik varsa eski paketi silip, guncel olanı ekler ve bagımlılıkları tekrar tespit eder.
# veritabanında olan bir paketin pisi-index.xml'de bulunmama durumunda veritabanındaki paketi siler.
# ters durumda pisi-index.xml'deki paketi veritabanına ekler.


import os
import sys
import pisi
import lzma
import urllib2
import piksemel
import itertools
import cStringIO

location = os.path.dirname(os.path.join(os.getcwd(), __file__)).rsplit('/', 1)[0]
os.chdir(location)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append(location)

from packages.models import *
from django.contrib.auth.models import User


BASEURL = "http://packages.pardus.org.tr/pardus/"
VERSION = ("2011", "corporate2")
REPOS = ("devel", "testing", "stable")
ARCHITECTURE = ("i686", "x86_64")

# .pisi dosyalarinin bulundugu dizin
BASE_CONTENT_FOLDER = '/var/www/localhost/htdocs/pardus/'


def createAttr(pisi_package, model, attribute):
    """attrList'deki attribute'lari, eger modelde zaten yoksa, modele ekle."""
    attrList = getattr(pisi_package, attribute)
    if not isinstance(attrList, list):
        attrList = [attrList]
    for attr in attrList:
        try:
            model.objects.get(name=attr)
        except model.DoesNotExist:
            model(name=attr).save()


def check_sha1sum(xml_url, sha1sum):
    """xml_url adresindeki sha1sum'i veritabaninda kayitli ve sha1sum ile
    ayniysa True don."""
    try:
        filehash = XmlHash.objects.get(name=xml_url)
        if filehash.hash == sha1sum:
            print "%s hash is identical." % xml_url
            return True
    except XmlHash.DoesNotExist:
        return False


def parse_index(filepath):
    pisi_index = pisi.index.Index()
    pisi_index.decode(piksemel.parseString(filepath), [])
    print "piksemel parsing done."
    return pisi_index


def create_package(pisi_package, dist):
    """Paket yaratma fonksiyonu. Guncellenme ve yeni eklenme durumlarında
    veritabanında yeni paket oluşturur.
    """

    # keys: her bir paketin sahip olmasi gereken fieldlar
    # values: fieldlarin gosterdigi modeller
    attributes = {'isA': isA, 'partOf': partOf, 'license': License, 'buildHost': BuildHost,
            'distribution': Distribution, 'architecture': Architecture, 'packager': User}

    for attribute, model in attributes.iteritems():
        if attribute == 'packager':
            packager = pisi_package.source.packager
            try:
                User.objects.get(username=packager.name)
            except User.DoesNotExist:
                # Paket sahibi henuz olusturulmamis
                User(username=packager.name, password="1234", email=packager.email).save()
        else:
            createAttr(pisi_package, model, attribute)

    # her paketin sahip olması gereken özellikler
    # (bu özellikler verilmeden paket oluşturulamaz)
    _name = pisi_package.name
    _pub_date = pisi_package.history[0].date
    #_isA = isA.objects.get(name=pisi_package.isA)
    _partOf = partOf.objects.get(name=pisi_package.partOf)
    #_license = License.objects.get(name=pisi_package.license)
    _build_host = BuildHost.objects.get(name=pisi_package.buildHost)
    _arch = Architecture.objects.get(name=pisi_package.architecture)
    _installed_size = pisi_package.installedSize
    _package_size = pisi_package.packageSize
    _package_hash = pisi_package.packageHash
    _package_format = pisi_package.packageFormat
    _homepage = pisi_package.source.homepage
    _packager = User.objects.get(username=pisi_package.source.packager.name)
    _pkgbase = pisi_package.source.name
    _uri = pisi_package.packageURI
    try:
        _dist = Distribution.objects.get(name=dist)
    except Distribution.DoesNotExist:
        _dist = Distribution(name=dist)
        _dist.save()

    kwargs = {'name': _name,
            'distribution': _dist,
            'architecture': _arch,
            'pub_date': _pub_date,
            'partOf': _partOf,
            'build_host': _build_host,
            'installed_size': _installed_size,
            'package_size': _package_size,
            'package_hash': _package_hash,
            'package_format': _package_format,
            'homepage': _homepage,
            'packager': _packager,
            'pkgbase': _pkgbase,
            'uri': _uri}

    p = Package(**kwargs)

    p.save()
    print "\t" + pisi_package.name, "added"
    # paketin isA attribute'unu ekle
    for isa in pisi_package.isA:
        p.isA.add(isA.objects.get(name=isa))

    # paket lisanslarını ekle
    for license in pisi_package.license:
        p.license.add(License.objects.get(name=license))

    # .pisi dosyasının yerini tespit edip, .pisi varsa pakete ait dosyaları ekle
    d = p.distribution.name.split('-')
    d.append(os.path.join(p.architecture.name, p.uri))
    filename = os.path.join(BASE_CONTENT_FOLDER, *d)
    package_files = cStringIO.StringIO()
    try:
        metadata, files = pisi.api.info_file(filename)
        for fileinfo in files.list:
            package_files.write('/' + fileinfo.path + '\n')
        package_files.reset()  # cursor'u basa al
        p.package_files = package_files.read()
        p.save()
    except pisi.Error:
        print ".pisi dosyası bulunamadı, muhtemelen konumu yanlış belirtilmiş ya da dosya yok"

    for key, item in pisi_package.description.items():
        d = Description(lang=key, desc=item, package=p)
        d.save()

    for key, item in pisi_package.summary.items():
        s = Summary(lang=key, sum=item, package=p)
        s.save()

    username = pisi_package.source.packager.name
    try:
        user = User.objects.get(username=username)
    except user.DoesNotExist:
        user = User(username=username, email=pisi_package.source.packager.email)
        user.save()

    first = True
    for update in pisi_package.history:
        u = Update(version=update.version, release=update.release,
                comment=update.comment,
                packager=update.name,
                package=p,
                email = update.email,
                date=update.date)
        u.save()
        if first:
            p.last_update = u.date
            p.save()
            first = False


def link_dependencies(pisi_package, dist):
    """pisi_package: Piksemel object
    dist: dagıtım, 2011-devel, corporate2-devel vs.
    dist dagıtımındaki pisi_package paketinin veritabanındaki baglarını kurar.
    """
    _name = pisi_package.name
    _dist = Distribution.objects.get(name=dist)
    _arch = Architecture.objects.get(name=pisi_package.architecture)

    pack = Package.objects.get(name=_name, distribution=_dist, architecture=_arch)
    print "adding deps of", pack.name
    _deps = [Package.objects.get(name=p.package, distribution=_dist, architecture=_arch)
                    for p in pisi_package.runtimeDependencies()]
    for dep in _deps:
        try:
            pack.dependencies.get(package=dep)
        except Package.DoesNotExist:
            pack.dependencies.add(dep)

def delete_models(pkg, model):
    """modeldeki pkg paketine ait kayıtları sil."""
    entries = model.objects.filter(package=pkg)
    for entry in entries:
        entry.delete()


if __name__ == '__main__':
    product = itertools.product(VERSION, REPOS, ARCHITECTURE)
    for xml in product:
        db_set = set()
        pisi_dict = dict()
        xml_url = BASEURL + '/'.join(xml) + '/pisi-index.xml.xz'
        sha1url = BASEURL + '/'.join(xml) + '/pisi-index.xml.xz.sha1sum'
        try:
            print "downloading started"
            raw_data = urllib2.urlopen(xml_url)
            print sha1url
            sha1sum = urllib2.urlopen(sha1url).read()
        except urllib2.HTTPError:
            continue  # bir sonraki indexten devam et

        print "decompressing started."
        xml_data = lzma.decompress(raw_data.read())
        print "decompressing finished."
        print "Pisi index parse started."
        pisi_index = parse_index(xml_data)
        print "Pisi index parse completed."

        if not check_sha1sum(xml_url, sha1sum):  # sha1sum'lar farkli
            dist = xml[0] + '-' + xml[1]
            for package in pisi_index.packages:
                pisi_dict[package.packageHash] = package

            print dist
            for package in Package.objects.filter(distribution__name=dist, architecture__name=xml[2]):
                db_set.add(package.package_hash)

            pisi_set = set(pisi_dict.keys())
            for obsolete_package in db_set - pisi_set:
                p = Package.objects.get(package_hash=obsolete_package)
                # silinecek pakete ait Description ve Summary kayıtlarını sil
                delete_models(p, Description)
                delete_models(p, Summary)
                p.delete()
                print p.name, "deleted."

            for new_package in pisi_set - db_set:
                create_package(pisi_dict[new_package], dist)

            try:
                xmlhash = XmlHash.objects.get(name=xml_url)
                xmlhash.hash = sha1sum
                xmlhash.save()
            except XmlHash.DoesNotExist:
                XmlHash(name=xml_url, hash=sha1sum).save()

            for package in pisi_index.packages:
                link_dependencies(package, dist)

    try:
        Distribution.objects.get(name="Pardus Corporate").delete()
    except Distribution.DoesNotExist:
        pass
    try:
        Distribution.objects.get(name="Pardus").delete()
    except Distribution.DoesNotExist:
        pass
