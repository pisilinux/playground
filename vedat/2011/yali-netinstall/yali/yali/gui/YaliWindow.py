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
import sys
import codecs
import gettext

_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QResource
from PyQt4.Qt import QWidget
from PyQt4.Qt import SIGNAL
from PyQt4.Qt import QTextBrowser
from PyQt4.Qt import QObject
from PyQt4.Qt import QPixmap
from PyQt4.Qt import QCursor
from PyQt4.Qt import QPixmap
from PyQt4.Qt import Qt
from PyQt4.Qt import QCursor
from PyQt4.Qt import QKeySequence
from PyQt4.Qt import QTimer
from PyQt4.Qt import QGraphicsOpacityEffect
from PyQt4.Qt import QIcon
from PyQt4.Qt import QMenu
from PyQt4.Qt import QSize
from PyQt4.Qt import QShortcut

from QTermWidget import QTermWidget
from pyaspects.weaver import weave_object_method

import yali
import yali.util
import yali.sysutils
import yali.context as ctx
from yali.gui.Ui.main import Ui_YaliMain
from yali.gui.Ui.help import Ui_Help
from yali.gui.YaliDialog import Dialog, QuestionDialog, Tetris
from yali.gui.aspects import enableNavButtonsAspect, disableNavButtonsAspect

from pds.gui import *

class HelpWidget(PAbstractBox):

    def __init__(self, parent):
        PAbstractBox.__init__(self, parent)

        self.ui = Ui_Help()
        self.ui.setupUi(self)

        self._animation = 2
        self._duration = 500

        self.hide()

    def showHelp(self):
        QTimer.singleShot(1, lambda: self.animate(start = TOPCENTER, stop = TOPCENTER))

    def hideHelp(self):
        self.animate(start = CURRENT, stop  = TOPCENTER, direction = OUT)

    def toggleHelp(self):
        if self.isVisible():
            self.hideHelp()
        else:
            self.showHelp()

    def setHelp(self, help):
        QTimer.singleShot(1, self.adjustSize)

##
# Widget for YaliWindow (you can call it MainWindow too ;).
class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)
        # Set pixmaps resource before Main Window initialized
        self._resource = os.path.join(ctx.consts.theme_dir, ctx.flags.theme, ctx.consts.pixmaps_resource_file)
        if os.path.exists(self._resource):
            resource = QResource()
            resource.registerResource(self._resource)
        else:
            raise yali.Error, _("Pixmaps resources file doesn't exists")

        self.ui = Ui_YaliMain()
        self.ui.setupUi(self)

        self.font = 10
        self.animation_type = None

        self.screens = None
        self.screens_content = None

        self.pds_helper = HelpWidget(self.ui.scrollAreaWidgetContents)

        # shortcut to open help
        self.help_shortcut = QShortcut(QKeySequence(Qt.Key_F1), self)

        # shortcut to open debug window
        #self.debugShortCut = QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_F2),self)

        # something funny
        self.tetris_shortcut = QShortcut(QKeySequence(Qt.Key_F6), self)
        self.cursor_shortcut = QShortcut(QKeySequence(Qt.Key_F7), self)
        self.theme_shortcut  = QShortcut(QKeySequence(Qt.Key_F8), self)

        # shortcut to open a console
        self.console_shortcut = QShortcut(QKeySequence(Qt.Key_F11), self)


        # set style
        self._style = os.path.join(ctx.consts.theme_dir, ctx.flags.theme, ctx.consts.style_file)
        if os.path.exists(self._style):
            self.updateStyle()
        else:
            raise yali.Error, _("Style file doesn't exists")

        # set screens content
        release_file = os.path.join(ctx.consts.branding_dir, ctx.flags.branding, ctx.consts.release_file)
        if os.path.exists(release_file):
            self.screens_content = yali.util.parse_branding_screens(release_file)
        else:
            raise yali.Error, _("Release file doesn't exists")


        # move one step at a time
        self.step_increment = 1

        # ToolButton Popup Menu
        self.menu = QMenu()
        self.shutdown = self.menu.addAction(QIcon(QPixmap(":/images/system-shutdown.png")), _("Turn Off Computer"))
        self.reboot = self.menu.addAction(QIcon(QPixmap(":/images/system-reboot.png")), _("Restart Computer"))
        self.restart = self.menu.addAction(QIcon(QPixmap(":/images/system-yali-reboot.png")), _("Restart YALI"))
        #self.menu.setDefaultAction(self.shutdown)
        self.ui.system_menu.setMenu(self.menu)
        self.ui.system_menu.setDefaultAction(self.shutdown)

        # Main Slots
        self.connect(self.help_shortcut, SIGNAL("activated()"), self.pds_helper.toggleHelp)
        #self.connect(self.debugShortCut,    SIGNAL("activated()"), self.toggleDebug)
        self.connect(self.console_shortcut, SIGNAL("activated()"), self.toggleConsole)
        self.connect(self.cursor_shortcut, SIGNAL("activated()"), self.toggleCursor)
        self.connect(self.theme_shortcut, SIGNAL("activated()"), self.toggleTheme)
        self.connect(self.tetris_shortcut, SIGNAL("activated()"), self.toggleTetris)
        self.connect(self.ui.buttonNext, SIGNAL("clicked()"), self.slotNext)
        self.connect(self.ui.buttonBack, SIGNAL("clicked()"), self.slotBack)
        self.connect(self.ui.toggleHelp, SIGNAL("clicked()"), self.pds_helper.toggleHelp)
        if not ctx.flags.install_type == ctx.STEP_FIRST_BOOT:
            self.connect(self.ui.releaseNotes, SIGNAL("clicked()"), self.showReleaseNotes)
        else:
            self.ui.releaseNotes.hide()
        self.connect(self.menu, SIGNAL("triggered(QAction*)"), self.slotMenu)

        self.cmb = _("right")
        self.dont_ask_again = False
        self.terminal = None
        self.tetris = None

        self.ui.helpContentFrame.hide()

        self.effect = QGraphicsOpacityEffect(self)
        self.ui.mainStack.setGraphicsEffect(self.effect)
        self.effect.setOpacity(1.0)

        self.anime = QTimer(self)
        self.connect(self.anime, SIGNAL("timeout()"), self.animate)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton and not self.dont_ask_again:
            if self.cmb == _("left"):
                ocmb = _("right")
            else:
                ocmb = _("left")
            reply = QuestionDialog(_("Mouse Settings"),
                                   _("You just clicked the <b>%s</b> mouse button.") % self.cmb,
                                   _("Do you want to switch to the <b>%s</b> handed configuration?") % ocmb,
                                   dontAsk = True)
            if reply == "yes":
                yali.sysutils.setMouse(self.cmb)
                self.cmb = ocmb
            elif reply == "dontask":
                self.dont_ask_again = True

    def updateStyle(self):
        self.setStyleSheet(file(self._style).read())
        self.font = 10

    def setFontPlus(self):
        self.increaseFontSize(1)

    def setFontMinus(self):
        self.increaseFontSize(-1)

    def increaseFontSize(self, num):
        # We have to edit style sheet to set new fonts
        # Because if you use a style sheet in your application
        # ::setFont gets useless :( http://doc.trolltech.com/4.5/qapplication.html#setFont
        old = "QWidget{font:%dpt;}" % self.font
        self.font = self.font + num
        new = "QWidget{font:%dpt;}" % self.font
        self.setStyleSheet(self.styleSheet().replace(old, new))

    def slotMenu(self, action):
        if action == self.shutdown:
            reply = QuestionDialog(_("Warning"),
                                   _("Are you sure you want to shut down your computer now?"))
            if reply == "yes":
                yali.util.shutdown()
        elif action == self.reboot:
            reply = QuestionDialog(_("Warning"),
                                   _("Are you sure you want to restart your computer now?"))
            if reply == "yes":
                yali.util.reboot()
        else:
            reply = QuestionDialog(_("Warning"),
                                   _("Are you sure you want to restart the YALI installer now?"))
            if reply == "yes":
                os.execv("/usr/bin/yali-bin", sys.argv)

    def toggleTheme(self):
        "This easter egg will be implemented later"
        """
        if self._style == os.path.join(ctx.consts.theme_dir, "%s/style.qss" % ctx.flags.theme):
            if os.path.join(ctx.consts.theme_dir, "%s/style.glass.qss" % ctx.flags.theme):
                self._style = os.path.join(ctx.consts.theme_dir, "%s/style.glass.qss" % ctx.flags.theme)
        else:
            self._style = os.path.join(ctx.consts.theme_dir, "%s/style.qss" % ctx.flags.theme)
        self.updateStyle()
        """

    def toggleConsole(self):
        if not self.terminal:
            terminal = QTermWidget()
            terminal.setScrollBarPosition(QTermWidget.ScrollBarRight)
            terminal.setColorScheme(1)
            terminal.sendText("export TERM='xterm'\nclear\n")
            self.terminal = Dialog(_("Terminal"), terminal, True, QKeySequence(Qt.Key_F11))
            self.terminal.resize(700, 500)
        self.terminal.exec_()

    def toggleTetris(self):
        self.tetris = Dialog(_("Tetris"), None, True, QKeySequence(Qt.Key_F6))
        _tetris = Tetris(self.tetris)
        self.tetris.addWidget(_tetris)
        self.tetris.resize(240, 500)
        _tetris.start()
        self.tetris.exec_()

    def toggleCursor(self):
        if self.cursor().shape() == QCursor(Qt.ArrowCursor).shape():
            raw = QPixmap(":/gui/pics/pardusman-icon.png")
            raw.setMask(raw.mask())
            self.setCursor(QCursor(raw, 2, 2))
        else:
            self.unsetCursor()

    # show/hide help text
    def slotToggleHelp(self):
        self.ui.helpContentFrame.setFixedHeight(self.ui.helpContent.height())
        if self.ui.helpContentFrame.isVisible():
            self.ui.helpContentFrame.hide()
        else:
            self.ui.helpContentFrame.show()
        widget = self.ui.mainStack.currentWidget()
        widget.update()

    # show/hide debug window
    def toggleDebug(self):
        if ctx.debugger.isVisible():
            ctx.debugger.hideWindow()
        else:
            ctx.debugger.showWindow()

    # returns the id of current stack
    def getCurrent(self, index):
        new_index   = self.ui.mainStack.currentIndex() + index
        total_index = self.ui.mainStack.count()
        if new_index < 0: new_index = 0
        if new_index > total_index: new_index = total_index
        return new_index

    # move to id numbered step
    def setCurrent(self, index=None):
        if index:
            self.stackMove(index)

    # execute next step
    def slotNext(self, dry_run=False):
        widget = self.ui.mainStack.currentWidget()
        ret = True
        if not dry_run:
            ret = widget.execute()
        if ret:
            self.pds_helper.hideHelp()
            self.ui.toggleHelp.setChecked(False)
            self.stackMove(self.getCurrent(self.step_increment))
            self.step_increment = 1

    # execute previous step
    def slotBack(self):
        widget = self.ui.mainStack.currentWidget()
        if widget.backCheck():
            self.stackMove(self.getCurrent(self.step_increment * -1))
        self.pds_helper.hideHelp()
        self.ui.toggleHelp.setChecked(False)
        self.step_increment = 1

    # move to id numbered stack
    def stackMove(self, index):
        if not index == self.ui.mainStack.currentIndex() or index == 0:
            self.effect.setOpacity(0.0)
            self.animation_type = "fade-in"
            self.anime.start(50)
            self.ui.mainStack.setCurrentIndex(index)
            widget = self.ui.mainStack.currentWidget()
            # Hack to fix goodbye screen help content
            # BUG:#15860, #15444
            if widget.name == "goodbye":
                widget_id = "%s%s" % (widget.name, ctx.flags.install_type)
            else:
                widget_id = widget.name

            widget_icon = self.screens_content[widget_id][0]

            if self.screens_content[widget_id][1].has_key(ctx.consts.lang):
                widget_title = self.screens_content[widget_id][1][ctx.consts.lang]
            else:
                widget_title = self.screens_content[widget_id][1]["en"]

            if self.screens_content[widget_id][2].has_key(ctx.consts.lang):
                widget_help = self.screens_content[widget_id][2][ctx.consts.lang]
            else:
                widget_help = self.screens_content[widget_id][2]["en"]

            self.ui.screenName.setText(widget_title)
            self.pds_helper.ui.helpContent.setText(widget_help)
            self.pds_helper.setHelp(widget_help)
            self.ui.screenIcon.setPixmap(QPixmap(":/gui/pics/%s.png" % (widget_icon)))

            ctx.mainScreen.processEvents()
            widget.update()
            ctx.mainScreen.processEvents()
            widget.shown()

    def animate(self):
        if self.animation_type == "fade-in":
            if self.effect.opacity() < 1.0:
                self.effect.setOpacity(self.effect.opacity() + 0.2)
            else:
                self.anime.stop()
        if self.animation_type == "fade-out":
            if self.effect.opacity() > 0.0:
                self.effect.setOpacity(self.effect.opacity() - 0.2)
            else:
                self.anime.stop()

    def createWidgets(self, screens=[]):
        if not self.screens:
            self.screens = screens
        self.ui.mainStack.removeWidget(self.ui.page)

        for screen in screens:
            #if ctx.flags.debug:
                # debug all screens.
            #    weave_all_object_methods(ctx.aspect, screen)

            # enable navigation buttons before shown
            weave_object_method(enableNavButtonsAspect, screen, "shown")
            # disable navigation buttons before the execute.
            weave_object_method(disableNavButtonsAspect, screen, "execute")
            try:
                self.ui.mainStack.addWidget(screen())
            except Exception, msg:
                rc = ctx.interface.messageWindow(_("Error"),
                                                 _("An error occurred when attempting "
                                                    "to load screens:%s") % msg,
                                                 type="custom", customIcon="error",
                                                 customButtons=[_("Exit")])
                if not rc:
                    sys.exit(0)

        #weave_all_object_methods(ctx.aspect, self)
        self.stackMove(ctx.flags.startup)

    # Enable/Disable buttons
    def disableNext(self):
        self.ui.buttonNext.setEnabled(False)

    def disableBack(self):
        self.ui.buttonBack.setEnabled(False)

    def enableNext(self):
        self.ui.buttonNext.setEnabled(True)

    def enableBack(self):
        self.ui.buttonBack.setEnabled(True)

    def isNextEnabled(self):
        return self.ui.buttonNext.isEnabled()

    def isBackEnabled(self):
        return self.ui.buttonBack.isEnabled()

    # processEvents
    def processEvents(self):
        QObject.emit(self, SIGNAL("signalProcessEvents"))

    def showReleaseNotes(self):
        # make a release notes dialog
        dialog = Dialog(_('Release Notes'), ReleaseNotes(self), self)
        dialog.resize(500, 400)
        dialog.exec_()

class ReleaseNotes(QTextBrowser):

    def __init__(self, *args):
        QTextBrowser.__init__(self, *args)

        self.setStyleSheet("background:white;color:black;")

        try:
            self.setText(codecs.open(self.loadFile(), "r", "UTF-8").read())
        except Exception, msg:
            ctx.logger.error(_(msg))

    def loadFile(self):
        releasenotes_path = os.path.join(ctx.consts.source_dir,"release-notes/releasenotes-%s.html" % ctx.consts.lang)

        if not os.path.exists(releasenotes_path):
            releasenotes_path = os.path.join(ctx.consts.source_dir, "release-notes", "releasenotes-en.html")
        if os.path.exists(releasenotes_path):
            return releasenotes_path
        raise Exception, _("Release notes could not be loaded.")
