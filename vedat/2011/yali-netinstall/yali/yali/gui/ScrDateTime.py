# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import gettext
_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL, QTimer, QDate, QComboBox, QTime

from pds.thread import PThread
from pds.gui import PMessageBox, MIDCENTER, CURRENT, OUT

import yali.localedata
import yali.context as ctx
import yali.postinstall
import yali.storage
from yali.gui import ScreenWidget
from yali.gui.Ui.datetimewidget import Ui_DateTimeWidget
from yali.timezone import TimeZoneList

class Widget(QWidget, ScreenWidget):
    name = "timeSetup"

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_DateTimeWidget()
        self.ui.setupUi(self)
        self.timer = QTimer(self)
        self.from_time_updater = True
        self.is_date_changed = False

        self.current_zone = ""

        self.tz_dict = {}
        self.continents = []
        self.countries = []

        for country, data in yali.localedata.locales.items():
            if country == ctx.consts.lang:
                if data.has_key("timezone"):
                    ctx.installData.timezone = data["timezone"]

        # Append continents and countries the time zone dictionary
        self.createTZDictionary()

        # Sort continent list
        self.sortContinents()

        # Append sorted continents to combobox
        self.loadContinents()

        # Load current continents country list
        self.getCountries(self.current_zone["continent"])

        # Highlight the current zone
        self.index = self.ui.continentList.findText(self.current_zone["continent"])
        self.ui.continentList.setCurrentIndex(self.index)

        self.index = self.ui.countryList.findText(self.current_zone["country"])
        self.ui.countryList.setCurrentIndex(self.index)

        # Initialize widget signal and slots
        self.__initSignals__()

        self.ui.calendarWidget.setDate(QDate.currentDate())

        self.pthread = None
        self.pds_messagebox = PMessageBox(self)
        self.pds_messagebox.enableOverlay()

        self.timer.start(1000)

    def __initSignals__(self):
        self.connect(self.ui.timeEdit, SIGNAL("timeChanged(QTime)"), self.timerStop)
        self.connect(self.ui.calendarWidget, SIGNAL("selectionChanged()"), self.dateChanged)
        self.connect(self.timer, SIGNAL("timeout()"), self.updateClock)
        self.connect(self.ui.continentList, SIGNAL("activated(QString)"), self.getCountries)

    def createTZDictionary(self):
        tz = TimeZoneList()
        zones = [ x.timeZone for x in tz.getEntries() ]
        zones.sort()

        for zone in zones:
            split = zone.split("/")

            # Human readable continent names
            continent_pretty_name = split[0].replace("_", " ")
            continent_pretty_name = continent_pretty_name

            # Some country names can be like Argentina/Catamarca so this fixes the splitting problem
            # caused by zone.split("/")
            #
            # Remove continent info and take the rest as the country name
            split.pop(0)
            country_pretty_name = " / ".join(split)

            # Human readable country names
            country_pretty_name = country_pretty_name.replace("_", " ")

            # Get current zone
            if zone == ctx.installData.timezone:
                self.current_zone = { "continent":continent_pretty_name, "country":country_pretty_name}

            # Append to dictionary
            if self.tz_dict.has_key(continent_pretty_name):
                self.tz_dict[continent_pretty_name].append([country_pretty_name, zone])
            else:
                self.tz_dict[continent_pretty_name] = [[country_pretty_name, zone]]


    def sortContinents(self):
        for continent in self.tz_dict.keys():
            self.continents.append(continent)
        self.continents.sort()

    def loadContinents(self):
        for continent in self.continents:
            self.ui.continentList.addItem(continent)

    def getCountries(self, continent):
        # Countries of the selected continent
        countries = self.tz_dict[str(continent)]

        self.ui.countryList.clear()

        for country, zone in countries:
            self.ui.countryList.addItem(country, zone)
            self.countries.append(country)



    def dateChanged(self):
        self.is_date_changed = True

    def timerStop(self):
        if self.from_time_updater:
            return
        # Human action detected; stop the timer.
        self.timer.stop()

    def updateClock(self):

        # What time is it ?
        cur = QTime.currentTime()

        self.from_time_updater = True
        self.ui.timeEdit.setTime(cur)
        self.from_time_updater = False

    def shown(self):
        self.timer.start(1000)

        if ctx.flags.install_type == ctx.STEP_BASE:
            self.pthread = PThread(self, self.startInit, self.dummy)

    def dummy(self):
        pass

    def setTime(self):
        ctx.interface.informationWindow.update(_("Adjusting time settings"))
        date = self.ui.calendarWidget.date()
        time = self.ui.timeEdit.time()
        args = "%02d%02d%02d%02d%04d.%02d" % (date.month(), date.day(),
                                              time.hour(), time.minute(),
                                              date.year(), time.second())


        # Set current date and time
        ctx.logger.debug("Date/Time setting to %s" % args)
        yali.util.run_batch("date", [args])

        # Sync date time with hardware
        ctx.logger.debug("YALI's time is syncing with the system.")
        yali.util.run_batch("hwclock", ["--systohc"])
        ctx.interface.informationWindow.hide()

    def execute(self):
        if not self.timer.isActive() or self.is_date_changed:
            QTimer.singleShot(500, self.setTime)
            self.timer.stop()

        index = self.ui.countryList.currentIndex()
        ctx.installData.timezone = self.ui.countryList.itemData(index).toString()
        ctx.logger.debug("Time zone selected as %s " % ctx.installData.timezone)

        if ctx.flags.install_type == ctx.STEP_BASE:
            #FIXME:Refactor hacky code
            ctx.installData.rootPassword = ctx.consts.default_password
            ctx.installData.hostName = yali.util.product_release()
            if ctx.storageInitialized:
                disks = filter(lambda d: not d.format.hidden, ctx.storage.disks)
                if len(disks) == 1:
                    ctx.storage.clearPartDisks = [disks[0].name]
                    ctx.mainScreen.step_increment = 2
                else:
                    ctx.mainScreen.step_increment = 1
                return True
            else:
                self.pds_messagebox.setMessage(_("Storage Devices initialising..."))
                self.pds_messagebox.animate(start=MIDCENTER, stop=MIDCENTER)
                ctx.mainScreen.step_increment = 0
                self.pthread.start()
                QTimer.singleShot(2, self.startStorageInitialize)
                return False

        return True

    def startInit(self):
        self.pds_messagebox.animate(start=MIDCENTER, stop=MIDCENTER)

    def startStorageInitialize(self):
        ctx.storageInitialized = yali.storage.initialize(ctx.storage, ctx.interface)
        self.initFinished()

    def initFinished(self):
        self.pds_messagebox.animate(start=CURRENT, stop=CURRENT, direction=OUT)
        disks = filter(lambda d: not d.format.hidden, ctx.storage.disks)
        if ctx.storageInitialized:
            if len(disks) == 1:
                ctx.storage.clearPartDisks = [disks[0].name]
                ctx.mainScreen.step_increment = 2
            else:
                ctx.mainScreen.step_increment = 1
            ctx.mainScreen.slotNext(dry_run=True)
        else:
            ctx.mainScreen.enableBack()
