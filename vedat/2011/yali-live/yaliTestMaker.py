#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
from optparse import OptionParser

i18n_languages = ["tr","nl","it","fr","de","pt_BR","es","pl","ca","sv"]
i18n_domain = "yali"

def install(path):
    unicode(path)
    os.system("python %s/setup.py install" % path)

def copy(path, exclude_share):
    print "Only YALI source is copied"
    imagedir = os.path.join(path, "image")
    unicode(imagedir)
    if not exclude_share:
        os.system("/bin/cp -PR /usr/share/yali %s/usr/share/" % imagedir)
    os.system("/bin/cp -PR /usr/lib/python2.6/site-packages/yali %s/usr/lib/python2.6/site-packages/" % imagedir)
    os.system("/bin/cp -PR /etc/yali %s/etc/yali" % imagedir)
    os.system("/bin/cp /usr/bin/yali-bin %s/usr/bin/yali-bin" % imagedir)
    os.system("/bin/cp /usr/bin/start-yali %s/usr/bin/start-yali" % imagedir)
    os.system("/bin/cp /usr/bin/bindYali %s/usr/bin/bindYali" % imagedir)
    os.system("/bin/cp /lib/udev/rules.d/70-yali.rules %s/lib/udev/rules.d/70-yali.rules" % imagedir)
    
    os.system("/bin/cp /usr/share/yali/branding/pardus/release.xml %s/usr/share/yali/branding/pardus/release.xml" % imagedir)
    for lang in i18n_languages:
            destpath = os.path.join(imagedir, "usr/share/locale/%s/LC_MESSAGES" % lang)
            srcpath = os.path.join("/", "usr/share/locale/%s/LC_MESSAGES/yali.mo" % lang)
            unicode(destpath)
            unicode(srcpath)
            try:
                os.makedirs(destpath)
            except:
                pass
            shutil.copy(srcpath, destpath)

def main():
    parser = OptionParser()
    parser.add_option("-i", "--install", dest="install", metavar="/path/to/YALI", help="Build & Install YALI")
    parser.add_option("-o", "--only", dest="only", action="store_true", default=False, help="Skip Image Packages redownload")
    parser.add_option("-e", "--exclude", dest="exclude", action="store_true", default=False, help="Exclude data files")
    parser.add_option("-a", "--arch-file", dest="arch_file", metavar="Archive File", help="Use archive spesific file")
    parser.add_option("-w", "--workdir", dest="workdir", metavar="WORKDIR", help="Pardusman workdir to make iso files")
    parser.add_option("-f", "--projectfile", dest="projectfile", metavar="FILE", help="Pardusman project file")
    parser.add_option("-p", "--pardusman", dest="pardusman", metavar="/path/to/PARDUSMAN", help="Pardusman Path")
    (opts, args) = parser.parse_args()

    if args :
        parser.error("incorrect number of arguments...")
    elif not opts.pardusman:
        opts.pardusman = os.getcwd()

    if opts.install:
        install(opts.install)
        print "Using YALI in existing syspath"

    if opts.workdir and opts.only:
        os.system("python %s make-repo %s" % (unicode(opts.pardusman), unicode(opts.projectfile)))
        os.system("python %s make-live %s" % (unicode(opts.pardusman), unicode(opts.projectfile)))

    #if opts.copy:
    #    copy(opts.workdir)
    #    print "Only YALI source is copied"
    #    return
    copy(opts.workdir, opts.exclude)

    os.system("python %s pack-live %s" % (unicode(opts.pardusman), unicode(opts.projectfile)))
    os.system("python %s make-iso %s" % (unicode(opts.pardusman), unicode(opts.projectfile)))

if __name__ == "__main__":
    main()
