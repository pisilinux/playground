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
import random
import gettext
_ = gettext.translation('yali', fallback=True).ugettext


from PyQt4.Qt import Qt
from PyQt4.Qt import QWidget
from PyQt4.Qt import SIGNAL
from PyQt4.Qt import QHBoxLayout
from PyQt4.Qt import QVBoxLayout
from PyQt4.Qt import QLabel
from PyQt4.Qt import QSpacerItem
from PyQt4.Qt import QSizePolicy
from PyQt4.Qt import QPushButton
from PyQt4.Qt import QDialog
from PyQt4.Qt import QObject
from PyQt4.Qt import QMetaObject
from PyQt4.Qt import QFrame
from PyQt4.Qt import QPainter
from PyQt4.Qt import QColor
from PyQt4.Qt import QPixmap
from PyQt4.Qt import QMessageBox
from PyQt4.Qt import QSize
from PyQt4.Qt import QShortcut
from PyQt4.Qt import QGridLayout
from PyQt4.Qt import QMovie
from PyQt4.Qt import QTimer
from PyQt4.Qt import QBasicTimer

import pisi
import yali
import yali.context as ctx
from yali.gui.Ui.exception import Ui_Exception

class windowTitle(QFrame):
    def __init__(self, parent, closeButton=True):
        QFrame.__init__(self, parent)
        self.setMaximumSize(QSize(9999999,22))
        self.setObjectName("windowTitle")
        self.hboxlayout = QHBoxLayout(self)
        self.hboxlayout.setSpacing(0)
        self.hboxlayout.setContentsMargins(0,0,4,0)

        self.label = QLabel(self)
        self.label.setObjectName("label")
        self.label.setStyleSheet("padding-left:4px; font:bold 11px; color: #FFFFFF;")

        self.hboxlayout.addWidget(self.label)

        spacerItem = QSpacerItem(40,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        if closeButton:
            self.pushButton = QPushButton(self)
            self.pushButton.setFocusPolicy(Qt.NoFocus)
            self.pushButton.setObjectName("pushButton")
            self.pushButton.setStyleSheet("font:bold;")
            self.pushButton.setText("X")

            self.hboxlayout.addWidget(self.pushButton)

        self.dragPosition = None
        self.mainwidget = self.parent()
        self.setStyleSheet("""
            QFrame#windowTitle {background-color:#222222;color:#FFF;}
        """)

        # Initial position to top left
        self.dragPosition = self.mainwidget.frameGeometry().topLeft()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.mainwidget.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.mainwidget.move(event.globalPos() - self.dragPosition)
            event.accept()

class Dialog(QDialog):
    def __init__(self, title, widget=None, closeButton=True, keySequence=None, isDialog=False, icon=None):
        QDialog.__init__(self, ctx.mainScreen)
        self.setObjectName("dialog")

        self.isDialog = isDialog
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.wlayout= QHBoxLayout()

        if icon:
            self.setStyleSheet("""QDialog QLabel{ margin-left:16px;margin-right:10px}
                                  QDialog#dialog {background-image:url(':/images/%s.png');
                                                  background-repeat:no-repeat;
                                                  background-position: top left; padding-left:500px;} """ % icon)

        self.windowTitle = windowTitle(self, closeButton)
        self.setTitle(title)
        self.layout.setMargin(0)
        self.layout.addWidget(self.windowTitle)

        if widget:
            self.addWidget(widget)
            QObject.connect(widget, SIGNAL("finished(int)"), self.reject)
            QObject.connect(widget, SIGNAL("resizeDialog(int,int)"), self.resize)

        if closeButton:
            QObject.connect(self.windowTitle.pushButton, SIGNAL("clicked()"), self.reject)

        if keySequence:
            shortCut = QShortcut(keySequence, self)
            QObject.connect(shortCut, SIGNAL("activated()"), self.reject)

        QMetaObject.connectSlotsByName(self)
        self.resize(10,10)

    def setTitle(self, title):
        self.windowTitle.label.setText(title)

    def addWidget(self, widget):
        self.content = widget
        self.wlayout.addWidget(self.content)
        if self.isDialog:
            widget.setStyleSheet("QMessageBox { background:none }")
            self.layout.addItem(QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding))
            self.layout.setContentsMargins(0, 0, 0, 8)
        self.layout.addLayout(self.wlayout)

    def setCentered(self):
        self.move(ctx.mainScreen.width()/2 - self.width()/2,
                  ctx.mainScreen.height()/2 - self.height()/2)

    def exec_(self):
        QTimer.singleShot(0, self.setCentered)
        return QDialog.exec_(self)

class MessageWindow:
    def __init__(self, title, text, type="ok", default=None, customButtons =None, customIcon=None, run=True, destroyAfterRun=True, detailed=False, longText=""):
        self.rc = None
        self.dialog = None
        self.msgBox = QMessageBox()
        self.doCustom = False
        self.customButtons = customButtons

        icon  = None
        buttons = None

        if type == 'ok':
            buttons = QMessageBox.Ok
            icon = "question"
        elif type == 'error':
            icon = "error"
            buttons =  QMessageBox.Ok
        elif type == 'warning':
            icon = "warning"
            buttons =  QMessageBox.Ok
        elif type == 'okcancel':
            icon = "question"
            buttons = QMessageBox.Ok | QMessageBox.Cancel
        elif type == 'question':
            icon = "question"
            buttons = QMessageBox.Ok | QMessageBox.Cancel
        elif type == 'yesno':
            icon = "question"
            buttons = QMessageBox.Yes | QMessageBox.No
        elif type == 'custom':
            self.doCustom = True
            if customIcon:
                icon = customIcon
            else:
                icon = "question"

        text = "<qt>%s</qt>" % text.replace("\n", " ")
        self.msgBox.setText(text)
        if detailed:
            self.msgBox.setDetailedText(unicode(longText))

        if self.doCustom:
            button = None
            for index, text in enumerate(self.customButtons):
                button = self.msgBox.addButton(text, QMessageBox.ActionRole)
                if default is not None and default == index:
                    self.msgBox.setDefaultButton(button)
        else:
            self.msgBox.setStandardButtons(buttons)

            if default == "no":
                default = QMessageBox.No
            elif default == "yes":
                default = QMessageBox.Yes
            elif default == "ok":
                default = QMessageBox.Ok
            else:
                default = None

        self.msgBox.setDefaultButton(default)

        self.dialog = Dialog(_(title), self.msgBox, closeButton=False, isDialog=True, icon=icon)
        self.dialog.resize(QSize(0,0))
        if run:
            self.run(destroyAfterRun)

    def run(self, destroyAfterRun=True):
        self.rc = self.dialog.exec_()
        if self.msgBox.clickedButton():
            if not self.doCustom:
                if self.msgBox.clickedButton().text() in [_("Ok"), _("Yes")]:
                    self.rc = 1
                elif self.msgBox.clickedButton().text() in [_("Cancel"), _("No")]:
                    self.rc = 0
            else:
                if self.msgBox.clickedButton().text() in self.customButtons:
                    self.rc = self.customButtons.index(self.msgBox.clickedButton().text())

        if destroyAfterRun:
            self.dialog = None

        return self.rc

def QuestionDialog(title, text, info = None, dontAsk = False):
    msgBox = QMessageBox()

    buttonYes = msgBox.addButton(_("Yes"), QMessageBox.ActionRole)
    buttonNo = msgBox.addButton(_("No"), QMessageBox.ActionRole)

    answers = {buttonYes:"yes",
               buttonNo :"no"}
    if dontAsk:
        buttonDontAsk = msgBox.addButton(_("Don't ask again"), QMessageBox.ActionRole)
        answers[buttonDontAsk] = "dontask"

    msgBox.setText(text)
    if not info:
        info = _("Do you want to continue?")
    msgBox.setInformativeText(info)

    dialog = Dialog(_(title), msgBox, closeButton = False, isDialog = True, icon="question")
    dialog.resize(300,120)
    dialog.exec_()

    ctx.mainScreen.processEvents()
    if msgBox.clickedButton() in answers.keys():
        return answers[msgBox.clickedButton()]
    return "no"


def InfoDialog(text, button=None, title=None, icon="info"):
    if not title:
        title = _("Information")
    if not button:
        button = _("OK")

    msgBox = QMessageBox()

    buttonOk = msgBox.addButton(button, QMessageBox.ActionRole)

    msgBox.setText(text)

    dialog = Dialog(_(title), msgBox, closeButton = False, isDialog = True, icon = icon)
    dialog.resize(300,120)
    dialog.exec_()
    ctx.mainScreen.processEvents()

class InformationWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self, ctx.mainScreen)
        self.setObjectName("InformationWindow")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFixedHeight(50)
        self.setMaximumWidth(800)
        self.setStyleSheet("""
            QFrame#frame { border: 1px solid rgba(255,255,255,30);
                           /*border-radius: 4px;*/
                           background-color: rgba(0,0,0,100);}

            QLabel { border:none;
                     color:#FFFFFF;}

            QProgressBar { border: 1px solid white;}

            QProgressBar::chunk { background-color: #F1610D;
                                  width: 0.5px;}
        """)

        self.gridlayout = QGridLayout(self)
        self.frame = QFrame(self)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(10, 0, 10, 0)

        # Spinner
        self.spinner = QLabel(self.frame)
        self.spinner.setMinimumSize(QSize(16, 16))
        self.spinner.setMaximumSize(QSize(16, 16))
        self.spinner.setIndent(6)
        self.movie = QMovie(':/images/working.mng')
        self.spinner.setMovie(self.movie)
        self.movie.start()
        self.horizontalLayout.addWidget(self.spinner)

        # Message
        self.label = QLabel(self.frame)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.icon = QLabel(self.frame)
        self.icon.setFixedWidth(16)
        self.icon.setFixedHeight(16)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.addWidget(self.icon)
        self.horizontalLayout.addWidget(self.label)

        self.gridlayout.addWidget(self.frame,0,0,1,1)

    def update(self, message, type=None, spinner=False):
        fontMetric = self.label.fontMetrics()
        textWidth = fontMetric.width(message)

        if type:
            self.icon.show()
            if type == "error":
                self.icon.setPixmap(QPixmap(":/gui/pics/dialog-error.png"))
                self.setStyleSheet(" QFrame#frame {background-color: rgba(255,0,0,100);} ")

            elif type == "warning":
                self.icon.setPixmap(QPixmap(":/gui/pics/dialog-warning.png"))
                self.setStyleSheet(" QFrame#frame {background-color: rgba(0,0,0,100);} ")

            self.setFixedWidth(textWidth + self.icon.width() + 50)
            self.label.setText(message)

        else:
            self.icon.hide()
            self.setStyleSheet(" QFrame#frame {background-color: rgba(0,0,0,100);} ")
            self.setFixedWidth(textWidth + self.icon.width() + 100)
            self.label.setText(message)

        self.spinner.setVisible(spinner)
        self.move(ctx.mainScreen.width()/2 - self.width()/2,
                  ctx.mainScreen.height() - self.height()/2 - 50)

        self.show()

    def refresh(self):
        ctx.mainScreen.processEvents()

    def show(self):
        QWidget.show(self)
        self.refresh()

    def hide(self):
        QWidget.hide(self)
        self.refresh()

class ProgressWindow(QWidget):
    def __init__(self, message):
        QWidget.__init__(self, ctx.mainScreen)
        self.setObjectName("ProgressWindow")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFixedHeight(50)
        self.setMaximumWidth(800)
        self.setStyleSheet("""
            QFrame#frame { border: 1px solid rgba(255,255,255,30);
                           /*border-radius: 4px;*/
                           background-color: rgba(255,0,0,100);}

            QLabel { border:none;
                     color:#FFFFFF;}

            QProgressBar { border: 1px solid white;}

            QProgressBar::chunk { background-color: #F1610D;
                                  width: 0.5px;}
        """)

        self.gridlayout = QGridLayout(self)
        self.frame = QFrame(self)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(6, 0, 0, 0)

        # Spinner
        self.spinner = QLabel(self.frame)
        self.spinner.setMinimumSize(QSize(16, 16))
        self.spinner.setMaximumSize(QSize(16, 16))
        self.spinner.setIndent(6)
        self.movie = QMovie(':/images/working.mng')
        self.spinner.setMovie(self.movie)
        self.movie.start()
        self.horizontalLayout.addWidget(self.spinner)

        # Message
        self.label = QLabel(self.frame)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.horizontalLayout.addWidget(self.label)
        self.gridlayout.addWidget(self.frame,0,0,1,1)

        self.update(message)

    def update(self, message):
        self.spinner.setVisible(True)
        fontMetric = self.label.fontMetrics()
        textWidth = fontMetric.width(message)
        self.setFixedWidth(textWidth + 100)
        self.label.setText(message)
        self.move(ctx.mainScreen.width()/2 - self.width()/2,
                  ctx.mainScreen.height() - self.height()/2 - 50)
        self.show()

    def refresh(self):
        ctx.mainScreen.processEvents()

    def show(self):
        QWidget.show(self)
        self.refresh()

    def pop(self):
        QWidget.hide(self)
        self.refresh()

class ExceptionWidget(QWidget):
    def __init__(self, traceback, rebootButton=False):
        QWidget.__init__(self, None)
        self.ui = Ui_Exception()
        self.ui.setupUi(self)
        self.ui.traceback.setText(traceback)
        self.ui.traceback.hide()
        self.ui.rebootButton.hide()
        self.connect(self.ui.showBackTrace, SIGNAL("clicked()"), self.showBackTrace)
        self.connect(self.ui.rebootButton,  SIGNAL("clicked()"), yali.util.reboot)

    def showBackTrace(self):
        self.ui.traceback.show()
        self.ui.rebootButton.show()
        self.ui.showBackTrace.hide()
        self.emit(SIGNAL("resizeDialog(int,int)"), 440, 440)

class ExceptionWindow:
    def __init__(self, error, traceback):
        self.rc = None
        self.dialog = None
        self.dialog = Dialog(_("Error reporting"), ExceptionWidget(traceback, rebootButton=True), icon="error")
        self.dialog.resize(300,160)
        self.run()

    def run(self):
        self.rc = self.dialog.exec_()


# Tetris from http://zetcode.com/tutorials/pyqt4/thetetrisgame
class Tetris(QFrame):
    BoardWidth = 10
    BoardHeight = 22
    Speed = 300

    def __init__(self, parent):
        QFrame.__init__(self, parent)

        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False
        self.curPiece = Shape()
        self.nextPiece = Shape()
        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()

        self.nextPiece.setRandomShape()
        self._parent = parent

    def message(self, string):
        self._parent.setTitle(string)

    def shapeAt(self, x, y):
        return self.board[(y * Tetris.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):
        self.board[(y * Tetris.BoardWidth) + x] = shape

    def squareWidth(self):
        return self.contentsRect().width() / Tetris.BoardWidth

    def squareHeight(self):
        return self.contentsRect().height() / Tetris.BoardHeight

    def start(self):
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clearBoard()

        self.message("Score : %s" % self.numLinesRemoved)
        self.newPiece()
        self.timer.start(Tetris.Speed, self)

    def pause(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        if self.isPaused:
            self.timer.stop()
            self.message("Paused")
        else:
            self.timer.start(Tetris.Speed, self)
            self.message("Score : %s" % self.numLinesRemoved)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - Tetris.BoardHeight * self.squareHeight()

        for i in range(Tetris.BoardHeight):
            for j in range(Tetris.BoardWidth):
                shape = self.shapeAt(j, Tetris.BoardHeight - i - 1)
                if shape != Tetrominoes.NoShape:
                    self.drawSquare(painter,
                        rect.left() + j * self.squareWidth(),
                        boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != Tetrominoes.NoShape:
            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                    boardTop + (Tetris.BoardHeight - y - 1) * self.squareHeight(),
                    self.curPiece.shape())

    def keyPressEvent(self, event):
        if not self.isStarted or self.curPiece.shape() == Tetrominoes.NoShape:
            QWidget.keyPressEvent(self, event)
            return

        key = event.key()
        if key == Qt.Key_P:
            self.pause()
            return
        if self.isPaused:
            return
        elif key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)
        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)
        elif key == Qt.Key_Down or key == Qt.Key_Space:
            self.dropDown()
        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotatedLeft(), self.curX, self.curY)
        elif key == Qt.Key_D:
            self.oneLineDown()
        else:
            QWidget.keyPressEvent(self, event)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
            else:
                self.oneLineDown()
        else:
            QFrame.timerEvent(self, event)

    def clearBoard(self):
        for i in range(Tetris.BoardHeight * Tetris.BoardWidth):
            self.board.append(Tetrominoes.NoShape)

    def dropDown(self):
        newY = self.curY
        while newY > 0:
            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break
            newY -= 1

        self.pieceDropped()

    def oneLineDown(self):
        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()

    def pieceDropped(self):
        for i in range(4):
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines()

        if not self.isWaitingAfterLine:
            self.newPiece()

    def removeFullLines(self):
        numFullLines = 0

        rowsToRemove = []

        for i in range(Tetris.BoardHeight):
            n = 0
            for j in range(Tetris.BoardWidth):
                if not self.shapeAt(j, i) == Tetrominoes.NoShape:
                    n = n + 1

            if n == 10:
                rowsToRemove.append(i)

        rowsToRemove.reverse()

        for m in rowsToRemove:
            for k in range(m, Tetris.BoardHeight):
                for l in range(Tetris.BoardWidth):
                    self.setShapeAt(l, k, self.shapeAt(l, k + 1))

        numFullLines = numFullLines + len(rowsToRemove)

        if numFullLines > 0:
            self.numLinesRemoved = self.numLinesRemoved + numFullLines

            self.message("Score : %s" % self.numLinesRemoved)
            self.isWaitingAfterLine = True
            self.curPiece.setShape(Tetrominoes.NoShape)
            self.update()

    def newPiece(self):
        self.curPiece = self.nextPiece
        self.nextPiece.setRandomShape()
        self.curX = Tetris.BoardWidth / 2 + 1
        self.curY = Tetris.BoardHeight - 1 + self.curPiece.minY()

        if not self.tryMove(self.curPiece, self.curX, self.curY):
            self.curPiece.setShape(Tetrominoes.NoShape)
            self.timer.stop()
            self.isStarted = False
            self.message("Game over")

    def tryMove(self, newPiece, newX, newY):
        for i in range(4):
            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)
            if x < 0 or x >= Tetris.BoardWidth or y < 0 or y >= Tetris.BoardHeight:
                return False
            if self.shapeAt(x, y) != Tetrominoes.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()
        return True

    def drawSquare(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2, 
            self.squareHeight() - 2, color)

        painter.setPen(color.light())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.dark())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
            x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1, 
            y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)

class Tetrominoes(object):
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7

class Shape(object):
    coordsTable = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))
    )

    def __init__(self):
        self.coords = [[0,0] for i in range(4)]
        self.pieceShape = Tetrominoes.NoShape

        self.setShape(Tetrominoes.NoShape)

    def shape(self):
        return self.pieceShape

    def setShape(self, shape):
        table = Shape.coordsTable[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def setRandomShape(self):
        self.setShape(random.randint(1, 7))

    def x(self, index):
        return self.coords[index][0]

    def y(self, index):
        return self.coords[index][1]

    def setX(self, index, x):
        self.coords[index][0] = x

    def setY(self, index, y):
        self.coords[index][1] = y

    def minX(self):
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m

    def maxX(self):
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

    def minY(self):
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

    def maxY(self):
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m

    def rotatedLeft(self):
        if self.pieceShape == Tetrominoes.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape
        for i in range(4):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result

    def rotatedRight(self):
        if self.pieceShape == Tetrominoes.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape
        for i in range(4):
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result
