#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import iso9660
import bz2, pycdio
import xml.etree.cElementTree as iks
import piksemel
import urwid
import urwid.raw_display


class getMenu:
    def selectionmenu(self,filelist):
        palette = [
                ('header', 'black,underline', 'light gray', 'standout,underline',
                    'black,underline', '#88a'),
                ('panel', 'light gray', 'dark blue', '',
                    '#ffd', '#00a'),
                ('focus', 'light gray', 'dark red', 'standout')
                ]

        screen = urwid.raw_display.Screen()
        screen.register_palette(palette)

        listbox = urwid.SimpleListWalker([])
        editedList = []

        def getTerminalSize():
            import fcntl, termios, struct
            height, width, hp, wp = struct.unpack('HHHH',
                                                fcntl.ioctl(0, termios.TIOCGWINSZ,
                                                    struct.pack('HHHH', 0, 0, 0, 0)))
            return width, height


        def focus(widget):
            return urwid.AttrMap(widget, None, 'focus')

        def selected_item (cb, state):
            if state == True:
                for fullpath in filelist:
                    if os.path.split(fullpath)[1] == cb.get_label():
                        editedList.append(fullpath)

            else:
                for fullpath in filelist:
                    if os.path.split(fullpath)[1] == cb.get_label():
                        editedList.remove(fullpath)

        def createCB(text,i):
            text = os.path.split(text)[1]
            cb = urwid.CheckBox(text, False, has_mixed=False)
            urwid.connect_signal(cb, 'change', selected_item)
            return focus(cb)

        def click_ok(button):
            raise urwid.ExitMainLoop()

        def bylength(path1, path2):
            return len(path1) - len(path2)

        width, height = getTerminalSize()
        filelist.sort(cmp=bylength)
        w = (width - len(filelist[0]))/4

        blank = urwid.Divider()

        listbox.extend([
                    blank,
                    blank,
                    urwid.Padding(
                        urwid.AttrMap(
                            urwid.Text("Select Version",align='center'),'header'),
                            ('fixed left',w-10),('fixed right',w-10)),
                    blank,
                    blank
                 ])

        i = 1
        kilo = 1024*1024



        for files in filelist:
            size = (os.path.getsize(files))/kilo
            listbox.extend([
                urwid.Padding(
                urwid.AttrMap(
                    urwid.Columns([
                        urwid.Pile([
                            createCB(files,i),
                            ]),
                        urwid.Pile([
                            urwid.Text("Size : %sMB" % size,align='left')]),
                        ]),'panel'),('fixed left',w),('fixed right',w))
                    ])

            i = i + 1

        listbox.extend([
            blank,
            urwid.Padding(
                urwid.GridFlow([
                    urwid.AttrWrap(
                        urwid.Button("OK", click_ok),
                                  'panel','focus')
                               ],10, 2, 2, 'center'),
                         ('fixed left',5), ('fixed right',5)),
                  ])

        def unhandled_input(key):
            if key in ('Q','q','esc'):
                raise urwid.ExitMainLoop()

        urwid.MainLoop(urwid.ListBox(listbox), screen=screen,
                        unhandled_input = unhandled_input).run()

        return editedList


#get as xml tree from string 
def getTree(item, level = 0):
    i = "\n" + level * "    "

    if len(item):
        if not item.text or not item.text.strip():
            item.text = i + "   "

        for e in item:
            getTree(e, level + 1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "

        if not e.tail or not e.tail.strip():
            e.tail = i

    else:
        if level and (not item.tail or not item.tail.strip()):
            item.tail = i

def ceil(x):
    return int( round ( x + 0.5 ) )

#Extracting 'pisi-index.xml' and 'gfxboot.cfg' from .iso
def extractData(local_filename):
    statbuf = iso.stat (local_filename,True)

    if statbuf is None:
        print "Couldn't get ISO-9660 file information for file"  % local_filename
        iso.close()
        sys.exit(1)

    a = ""
    blocks = ceil(statbuf['size'] / pycdio.ISO_BLOCKSIZE)

    for i in range(blocks):
        lsn = statbuf['LSN'] + i
        size, buf= iso.seek_read (lsn)
        a += buf

        if size <= 0 :
            print "Error reading ISO 9660 file %s at LSN %d" % (local_filename, lsn)
            sys.exit(1)

    if local_filename == "repo/pisi-index.xml.bz2":
        data = bz2.decompress(a)
    else:
        for line in a.split("\n"):
            if line.lstrip().startswith("distro="):
                data = line.lstrip().split("=", 1)[1]
    return data

#parsing pisi-index.xml.bz2 file which is in iso image.
def parseXml():
    xmlStr = extractData("repo/pisi-index.xml.bz2")
    doc = piksemel.parseString(xmlStr)
    installedsize = 0
    for tags in doc.tags("Package"):
        sizes = int(tags.getTagData("InstalledSize"))
        installedsize += int(sizes)
    architecture = tags.getTagData("Architecture")
    return installedsize, architecture


#if none given
isoFolder = os.getcwd()

if len(sys.argv) > 1:
    isoFolder = sys.argv[1]
if len(sys.argv) > 2:
    print "usage : %s [Path]" % sys.argv[0]

treeString = ""

#get .iso files from directory
filelist = []

for root , dirs, files in os.walk(isoFolder):
    for filespath in files:
        if filespath.endswith('.iso'):
            filelist.append(os.path.join(root,filespath))

if len(filelist) == 0:
    print "There is no ISO image file in '%s'" % isoFolder
    print "usage : %s [Path]" % sys.argv[0]
    sys.exit(1)

listObject = getMenu()
filelist = listObject.selectionmenu(filelist)

root = iks.Element("PXEBOOT")
isoimages = iks.SubElement(root, "ISOIMAGES")

for files_name in filelist:
    iso = iso9660.ISO9660.IFS ( source = files_name )

    pardus = iks.SubElement(isoimages, "Pardus")
    name = extractData("boot/isolinux/gfxboot.cfg")

    name_tag = iks.SubElement(pardus, "Name")
    name_tag.text = name

    isopath = (files_name.split(isoFolder)[1]).lstrip("/")
    path_tag = iks.SubElement(pardus, "Path")
    path_tag.text = isopath

    for dirs in iso.readdir("/"):
        if dirs[0] == "repo": 
            isosize, architecture = parseXml()
        else:
            isosize = os.path.getsize(files_name)
            architecture = "LiveCD"

    isosize = str(isosize)
    size_tag = iks.SubElement(pardus, "Size")
    size_tag.text = isosize

    architecture_tag = iks.SubElement(pardus, "Architecture")
    architecture_tag.text = architecture

getTree(root)
treeString += iks.tostring(root)
treeString += "\n"

xmlfile = open("%s/pxeboot_iso_files.xml" % isoFolder,"w")
xmlfile.write(treeString)
xmlfile.close()
