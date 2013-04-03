#!/usr/bin/python
# -*- coding: utf-8 -*-

from pisi import api as pisiapi
import platform
import os

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    environments = open ("/usr/lib/python2.7/site-packages/pds/environments.py","r")
    environments_array = environments.readlines()
    x= 0
    for i in range(0,environments_array.__len__()):
        if environments_array[i].find("DefaultIconTheme     = 'hicolor'") != -1:
            environments_array[i] ="    DefaultIconTheme     = 'oxygen'\n"
            x = 42
            break
    environments.close()
    if x != 0:
        environments = open("/usr/lib/python2.7/site-packages/pds/environments.py","w")
        environments.writelines(environments_array)
        environments.close()

    fileassociations = open("/usr/share/applications/mimeapps.list","a")
    fileassociations.write("application/pdf=epdfview.desktop;\n")
    fileassociations.write("application/zip=xarchiver.desktop;\n")
    fileassociations.write("application/x-rar=xarchiver.desktop;\n")
    fileassociations.write("application/x-compressed-tar=xarchiver.desktop;\n")
    fileassociations.write("application/x-tar=xarchiver.desktop;\n")
    fileassociations.write("application/x-bzip-compressed-tar=xarchiver.desktop;\n")
    fileassociations.write("image/jpeg=ristretto.desktop;\n")
    fileassociations.write("image/png=ristretto.desktop;\n")
    fileassociations.write("image/gif=ristretto.desktop;\n")
    fileassociations.write("image/x-ms-bmp=ristretto.desktop;\n")
    fileassociations.write("text/plain=medit.desktop;\n")
    fileassociations.write("application/x-pisi=package-manager.desktop;\n")
    fileassociations.close()

    desktop = open("/usr/share/gdm/BuiltInSessions/default.desktop","r")
    satirlar = desktop.readlines()
    for i in range(len(satirlar)):
        if (satirlar[i].find("Exec=default")==0):
            satirlar[i] = satirlar[i].replace("default","startxfce4")
    desktop.close()
    desktop = open("/usr/share/gdm/BuiltInSessions/default.desktop","w")
    for i in satirlar:
        desktop.write(i)
    desktop.close()


    #FIXME:
    try:
        os.unlink("/usr/share/xsessions/gnome.desktop")
    except:
        pass
    try:
        os.unlink("/usr/share/xsessions/openbox-gnome.desktop")
    except:
        pass
    try:
        os.unlink("/usr/share/xsessions/openbox-kde.desktop")
    except:
        pass
