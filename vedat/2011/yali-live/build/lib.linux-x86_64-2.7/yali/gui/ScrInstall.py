# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
import os
from multiprocessing import Process, Queue
from Queue import Empty

import gettext
_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL, QPixmap, QObject, QTimer, QMutex, QWaitCondition

import pisi.ui

import yali.util
import yali.pisiiface
import yali.postinstall
import yali.context as ctx
from yali.gui import ScreenWidget
from yali.gui.Ui.installwidget import Ui_InstallWidget

from yali.gui.Ui.installprogress import Ui_InstallProgress
from pds.gui import PAbstractBox, BOTCENTER

EventConfigure, EventInstall, EventSetProgress, EventError, EventAllFinished, EventPackageInstallFinished, EventRetry = range(1001, 1008)

class InstallProgressWidget(PAbstractBox):

    def __init__(self, parent):
        PAbstractBox.__init__(self, parent)

        self.ui = Ui_InstallProgress()
        self.ui.setupUi(self)

        self._animation = 2
        self._duration = 500

    def showInstallProgress(self):
        QTimer.singleShot(1, lambda: self.animate(start = BOTCENTER, stop = BOTCENTER))

    """
    def hideHelp(self):
            self.animate(start = CURRENT,
                         stop  = TOPCENTER,
                         direction = OUT)
    def toggleHelp(self):
        if self.isVisible():
            self.hideHelp()
        else:
            self.showHelp()

    def setHelp(self, help):
        self.ui.helpContent.hide()
        self.ui.helpContent2.setText(help)
        # self.resize(QSize(1,1))
        QTimer.singleShot(1, self.adjustSize)
    """



def iter_slideshows():
    slideshows = []

    release_file = os.path.join(ctx.consts.branding_dir, ctx.flags.branding, ctx.consts.release_file)
    slideshows_content = yali.util.parse_branding_slideshows(release_file)

    for content in slideshows_content:
        slideshows.append({"picture":QPixmap(os.path.join(ctx.consts.branding_dir,
                                                    ctx.flags.branding,
                                                    ctx.consts.slideshows_dir,
                                                    content[0])), "description":content[1]})
    while True:
        for slideshow in slideshows:
            yield slideshow

class Widget(QWidget, ScreenWidget):
    name = "packageInstallation"

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_InstallWidget()
        self.ui.setupUi(self)

        self.installProgress = InstallProgressWidget(self)

        self.timer = QTimer(self)
        QObject.connect(self.timer, SIGNAL("timeout()"), self.changeSlideshows)

        self.poll_timer = QTimer(self)
        QObject.connect(self.poll_timer, SIGNAL("timeout()"), self.checkQueueEvent)

        if ctx.consts.lang == "tr":
            self.installProgress.ui.progress.setFormat("%%p")

        self.iter_slideshows = iter_slideshows()

        # show first pic
        self.changeSlideshows()

        self.total = 0
        self.cur = 0
        self.has_errors = False

        # mutual exclusion
        self.mutex = None
        self.wait_condition = None
        self.queue = None

        self.retry_answer = False
        self.pkg_configurator = None
        self.pkg_installer = None

    def shown(self):
        # Disable mouse handler
        ctx.mainScreen.dontAskCmbAgain = True
        ctx.mainScreen.theme_shortcut.setEnabled(False)
        ctx.mainScreen.ui.system_menu.setEnabled(False)

        # start installer thread
        ctx.logger.debug("PkgInstaller is creating...")
        self.mutex = QMutex()
        self.wait_condition = QWaitCondition()
        self.queue = Queue()
        self.pkg_installer = PkgInstaller(self.queue, self.mutex, self.wait_condition, self.retry_answer)

        self.poll_timer.start(500)

        # start installer polling
        ctx.logger.debug("Calling PkgInstaller.start...")
        self.pkg_installer.start()

        ctx.mainScreen.disableNext()
        ctx.mainScreen.disableBack()

        # start 30 seconds
        self.timer.start(1000 * 30)

        self.installProgress.showInstallProgress()

    def checkQueueEvent(self):

        while True:
            try:
                data = self.queue.get_nowait()
                event = data[0]
            except Empty, msg:
                return

            ctx.logger.debug("checkQueueEvent: Processing %s event..." % event)
            # EventInstall
            if event == EventInstall:
                package = data[1]
                self.installProgress.ui.info.setText(_("Installing <b>%(name)s</b> -- %(summary)s") % {"name":package.name,
                                                                                       "summary":package.summary})
                ctx.logger.debug("Pisi: %s installing" % package.name)
                self.cur += 1
                self.installProgress.ui.progress.setValue(self.cur)

            # EventConfigure
            elif event == EventConfigure:
                package = data[1]
                self.installProgress.ui.info.setText(_("Configuring <b>%s</b>") % package.name)
                ctx.logger.debug("Pisi: %s configuring" % package.name)
                self.cur += 1
                self.installProgress.ui.progress.setValue(self.cur)

            # EventSetProgress
            elif event == EventSetProgress:
                total = data[1]
                self.installProgress.ui.progress.setMaximum(total)

            # EventPackageInstallFinished
            elif event == EventPackageInstallFinished:
                print "***EventPackageInstallFinished called...."
                self.packageInstallFinished()

            # EventError
            elif event == EventError:
                err = data[1]
                self.installError(err)

            # EventRetry
            elif event == EventRetry:
                package = os.path.basename(data[1])
                self.timer.stop()
                self.poll_timer.stop()
                rc = ctx.interface.messageWindow(_("Warning"),
                                                 _("Following error occured while "
                                                   "installing packages:"
                                                   "<b>%s</b><br><br>"
                                                   "Do you want to retry?")
                                                 % package,
                                                 type="custom", customIcon="warning",
                                                 customButtons=[_("Yes"), _("No")])
                self.retry_answer = not rc

                self.timer.start(1000 * 30)
                self.poll_timer.start(500)
                self.wait_condition.wakeAll()

            # EventAllFinished
            elif event == EventAllFinished:
                self.finished()

    def changeSlideshows(self):
        slide = self.iter_slideshows.next()
        self.ui.slideImage.setPixmap(slide["picture"])
        if slide["description"].has_key(ctx.consts.lang):
            description = slide["description"][ctx.consts.lang]
        else:
            description = slide["description"]["en"]
        self.ui.slideText.setText(description)

    def packageInstallFinished(self):
        yali.postinstall.writeFstab()

        # Configure Pending...
        # run baselayout's postinstall first
        yali.postinstall.initbaselayout()

        # postscripts depend on 03locale...
        yali.util.writeLocaleFromCmdline()

        #Write InitramfsConf
        yali.postinstall.writeInitramfsConf()

        # run dbus in chroot
        yali.util.start_dbus()

        # start configurator thread
        self.pkg_configurator = PkgConfigurator(self.queue, self.mutex)
        self.pkg_configurator.start()

    def execute(self):
        # stop slide show
        self.timer.stop()
        self.poll_timer.stop()
        return True

    def finished(self):
        self.poll_timer.stop()

        if self.has_errors:
            return

        ctx.mainScreen.slotNext()

    def installError(self, error):
        self.has_errors = True
        errorstr = _("""An error occured during the installation of packages.
This may be caused by a corrupted installation medium error:
%s
""") % str(error)
        ctx.interface.exceptionWindow(error, errorstr)
        ctx.logger.error("Package installation failed error with:%s" % error)

class PkgInstaller(Process):

    def __init__(self, queue, mutex, wait_condition, retry_answer):
        Process.__init__(self)
        self.queue = queue
        self.mutex = mutex
        self.wait_condition = wait_condition
        self.retry_answer = retry_answer
        ctx.logger.debug("PkgInstaller started.")

    def run(self):
        ctx.logger.debug("PkgInstaller is running.")
        ui = PisiUI(self.queue)
        ctx.logger.debug("PisiUI is creating..")
        yali.pisiiface.initialize(ui)
        ctx.logger.debug("Pisi initialize is calling..")

        if ctx.flags.collection:
            ctx.logger.debug("Collection Repo added.")
            yali.pisiiface.addRepo(ctx.consts.collection_repo_name, ctx.installData.autoCollection.index)
        else:
            ctx.logger.debug("CD Repo adding.")
            yali.pisiiface.addCdRepo()

        # show progress
        total = len(ctx.packagesToInstall)
        ctx.logger.debug("Sending EventSetProgress")
        data = [EventSetProgress, total*2]
        self.queue.put_nowait(data)
        ctx.logger.debug("Found %d packages in repo.." % total)
        try:
            while True:
                try:
                    yali.pisiiface.install(ctx.packagesToInstall)
                    break # while
                except Exception, msg:
                    # Lock the mutex
                    self.mutex.lock()

                    # Send error message
                    data = [EventRetry, str(msg)]
                    self.queue.put_nowait(data)

                    # wait for the result
                    self.wait_condition.wait(self.mutex)
                    self.mutex.unlock()

                    if not self.retry_answer:
                        raise msg

        except Exception, msg:
            data = [EventError, msg]
            self.queue.put_nowait(data)
            # wait for the result
            self.wait_condition.wait(self.mutex)

        ctx.logger.debug("Package install finished ...")
        # Package Install finished lets configure them
        data = [EventPackageInstallFinished]
        self.queue.put_nowait(data)


class PkgConfigurator(Process):

    def __init__(self, queue, mutex):
        Process.__init__(self)
        self.queue = queue
        self.mutex = mutex
        ctx.logger.debug("PkgConfigurator started.")

    def run(self):
        ctx.logger.debug("PkgConfigurator is running.")
        ui = PisiUI(self.queue)
        yali.pisiiface.initialize(ui=ui, with_comar=True)

        try:
            # run all pending...
            ctx.logger.debug("exec : yali.pisiiface.configurePending() called")
            yali.pisiiface.configurePending()
        except Exception, msg:
            data = [EventError, msg]
            self.queue.put_nowait(data)

       # Remove temporary repository and install add real
        if ctx.flags.collection:
            yali.pisiiface.switchToPardusRepo(ctx.consts.collection_repo_name)
        else:
            yali.pisiiface.switchToPardusRepo(ctx.consts.cd_repo_name)

        data = [EventAllFinished]
        self.queue.put_nowait(data)

class PisiUI(pisi.ui.UI):

    def __init__(self, queue):
        pisi.ui.UI.__init__(self)
        self.queue = queue
        self.last_package = ''

    def notify(self, event, **keywords):
        if event == pisi.ui.installing:
            ctx.logger.debug("PisiUI.notify event: Install")
            data = [EventInstall, keywords['package']]
            self.last_package = keywords['package'].name
            self.queue.put_nowait(data)
        elif event == pisi.ui.configuring:
            ctx.logger.debug("PisiUI.notify event: Configure")
            data = [EventConfigure, keywords['package']]
            self.last_package = keywords['package'].name
            self.queue.put_nowait(data)

    def error(self, msg):
        ctx.logger.debug("PisiUI.error: %s" % unicode(msg))

    def warning(self, msg):
        ctx.logger.debug("PisiUI.warning: %s" % unicode(msg))
