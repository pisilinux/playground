#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# Qt Stuff
from PyQt4.QtGui import qApp
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QPalette
from PyQt4.QtGui import QFontMetrics
from PyQt4.QtGui import QItemDelegate
from PyQt4.QtGui import QStyleFactory
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtGui import QStyleOptionButton
from PyQt4.QtGui import QStyledItemDelegate
from PyQt4.QtGui import QStyleOptionViewItemV4

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import QRect
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import QPoint
from PyQt4.QtCore import QVariant

from pmutils import *
from packagemodel import *
from webdialog import WebDialog
from rowanimator import RowAnimator

import config

DARKRED = QColor('darkred')
WHITE = QColor('white')
RED = QColor('red')
GRAY = QColor('gray')
BLUE = QColor('blue')
LIGHTBLUE = QColor('#DEE5F2')
DARKVIOLET = QColor('#3B414F')
LIGHTGREEN = QColor('#F1F5EC')
DARKGREEN = QColor('#32775F')
CHECK_ICON = 'add'
RECT = QRect()
DETAIL_LINE_OFFSET = 36
ICON_PADDING = 0
ROW_HEIGHT = 52
ICON_SIZE = 2

class PackageDelegate(QStyledItemDelegate):

    AppStyle = qApp.style

    def __init__(self, parent=None, mainWindow=None, showDetailsButton=True, animatable=True):
        super(PackageDelegate, self).__init__(parent)
        self.webDialog = WebDialog(mainWindow)
        self.show_details_button = showDetailsButton

        self.rowAnimator = RowAnimator(parent.packageList)
        self.defaultIcon = KIcon(('package-x-generic', 'package_applications'), 32)
        self.defaultInstalledIcon = QIcon(KIconLoader.loadOverlayed(('package-x-generic', 'package_applications'), CHECK_ICON, 32))
        self.animatable = animatable
        self._max_height = ROW_HEIGHT

        self._rt_0 = QIcon(":/data/star_0.png")
        self._rt_1 = QIcon(":/data/star_1.png")

        self.types = {'critical':(RED,     i18n('critical')),
                      'security':(DARKRED, i18n('security'))}

        self.font = Pds.settings('font','Sans,10').split(',')[0]

        self.normalFont = QFont(self.font, 10, QFont.Normal)
        self.boldFont = QFont(self.font, 11, QFont.Bold)
        self.normalDetailFont = QFont(self.font, 9, QFont.Normal)
        self.boldDetailFont = QFont(self.font, 9, QFont.Bold)
        self.tagFont = QFont(self.font, 7, QFont.Normal)

        self.tagFontFM = QFontMetrics(self.tagFont)
        self.boldFontFM = QFontMetrics(self.boldFont)
        self.boldDetailFontFM = QFontMetrics(self.boldDetailFont)
        self.normalFontFM = QFontMetrics(self.normalFont)
        self.normalDetailFontFM = QFontMetrics(self.normalDetailFont)

        self._titles = {'description': i18n("Description:"),
                        'website'    : i18n("Website:"),
                        'release'    : i18n("Release:"),
                        'repository' : i18n("Repository:"),
                        'size'       : i18n("Package Size:"),
                        'installVers': i18n("Installed Version:")}

        self._titleFM = {}
        for key, value in self._titles.items():
            self._titleFM[key] = self.boldDetailFontFM.width(value) + ICON_SIZE + 3

        self.baseWidth = self.boldFontFM.width(max(self._titles.values(), key=len)) + ICON_SIZE
        self.parent = parent.packageList

        # Base style for some of important features
        # self.plastik = QStyleFactory.create('plastique')

    def paint(self, painter, option, index):
        if not index.isValid():
            return super(PackageDelegate, self).paint(painter, option, index)

        if index.flags() & Qt.ItemIsUserCheckable:
            if index.column() == 0:
                self.paintCheckBoxColumn(painter, option, index)
            else:
                self.paintInfoColumn(painter, option, index)
        else:
            self.paintInfoColumn(painter, option, index, width_limit = 10)

    def paintCheckBoxColumn(self, painter, option, index):
        opt = QStyleOptionViewItemV4(option)

        buttonStyle = QStyleOptionButton()
        buttonStyle.state = QStyle.State_On if index.model().data(index, Qt.CheckStateRole) == QVariant(Qt.Checked) else QStyle.State_Off

        if option.state & QStyle.State_MouseOver or option.state & QStyle.State_HasFocus:
            buttonStyle.state |= QStyle.State_HasFocus

        buttonStyle.rect = opt.rect.adjusted(4, -opt.rect.height() + ROW_HEIGHT, 0, 0)
        PackageDelegate.AppStyle().drawControl(QStyle.CE_CheckBox, buttonStyle, painter, None)

    def paintInfoColumn(self, painter, option, index, width_limit = 0):
        left = option.rect.left() + 3
        top = option.rect.top()
        width = option.rect.width() - width_limit

        pixmap = QPixmap(option.rect.size())
        pixmap.fill(Qt.transparent)

        p = QPainter(pixmap)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.translate(-option.rect.topLeft())

        textInner = 2 * ICON_PADDING + ROW_HEIGHT - 10
        itemHeight = ROW_HEIGHT + 2 * ICON_PADDING

        margin = left + ICON_PADDING - 10

        title = index.model().data(index, NameRole).toString()
        summary = index.model().data(index, SummaryRole).toString()
        ptype = str(index.model().data(index, TypeRole).toString())
        rate = int(index.model().data(index, RateRole).toInt()[0])
        installed = index.model().data(index, InstalledRole).toBool()

        # We need to request update if its not possible to get meta data about the package
        try:
            # Get Package Icon if exists
            _icon = index.model().data(index, Qt.DecorationRole).toString()
        except:
            p.end()
            painter.drawPixmap(option.rect.topLeft(), pixmap)
            self.parent.requestUpdate()
            return

        icon = None

        if _icon:
            overlay = [CHECK_ICON] if installed else []
            KIconLoader._forceCache = True
            pix = KIconLoader.loadOverlayed(_icon, overlay, 32)
            if not pix.isNull():
                icon = QIcon(pix.scaled(QSize(32, 32), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            KIconLoader._forceCache = False

        if not icon:
            icon = self.defaultIcon if not installed else self.defaultInstalledIcon

        # Paint the Icon
        icon.paint(p, margin, top + ICON_PADDING, ROW_HEIGHT, ROW_HEIGHT, Qt.AlignCenter)

        fix_pos = 0
        if index.model().columnCount() <= 1:
            fix_pos = 22

        if config.USE_APPINFO:
            # Rating Stars
            for _rt_i in range(5):
                self._rt_0.paint(p, width + 10 * _rt_i - 30 - fix_pos, top + ROW_HEIGHT / 4, 10, 10, Qt.AlignCenter)
            for _rt_i in range(rate):
                self._rt_1.paint(p, width + 10 * _rt_i - 30 - fix_pos, top + ROW_HEIGHT / 4, 10, 10, Qt.AlignCenter)

        foregroundColor = option.palette.color(QPalette.Text)
        p.setPen(foregroundColor)

        # Package Name
        p.setFont(self.boldFont)
        p.drawText(left + textInner, top, width - textInner, itemHeight / 2, Qt.AlignBottom | Qt.AlignLeft, title)

        tagWidth = 0

        _component_width = 0
        if self.parent.showComponents:
            component = str(index.model().data(index, ComponentRole).toString())
            widthOfTitle = self.boldFontFM.width(title) + 6 + left + textInner

            p.setFont(self.tagFont)
            rect = self.tagFontFM.boundingRect(option.rect, Qt.TextWordWrap, component)
            p.setPen(LIGHTGREEN)
            p.setBrush(LIGHTGREEN)
            p.drawRoundRect(widthOfTitle , top + 12, rect.width() + 4, rect.height(), 10, 10)
            p.setPen(DARKGREEN)
            p.drawText(widthOfTitle + 2, top + 12, rect.width(), rect.height(), Qt.AlignCenter, component)
            p.setPen(foregroundColor)
            _component_width = rect.width() + 8

        if self.parent.showIsA:
            isa = str(index.model().data(index, IsaRole).toString())
            if not isa == '':
                widthOfTitle = self.boldFontFM.width(title) + 6 + left + textInner + _component_width

                p.setFont(self.tagFont)
                rect = self.tagFontFM.boundingRect(option.rect, Qt.TextWordWrap, isa)
                p.setPen(LIGHTBLUE)
                p.setBrush(LIGHTBLUE)
                p.drawRoundRect(widthOfTitle , top + 12, rect.width() + 4, rect.height(), 10, 10)
                p.setPen(DARKVIOLET)
                p.drawText(widthOfTitle + 2, top + 12, rect.width(), rect.height(), Qt.AlignCenter, isa)
                p.setPen(foregroundColor)
                _component_width += rect.width() + 8

        if ptype not in ('None', 'normal'):
            widthOfTitle = self.boldFontFM.width(title) + 6 + left + textInner + _component_width
            p.setFont(self.tagFont)
            rect = self.tagFontFM.boundingRect(option.rect, Qt.TextWordWrap, self.types[ptype][1])
            p.setPen(self.types[ptype][0])
            p.setBrush(self.types[ptype][0])
            p.drawRoundRect(widthOfTitle, top + 12, rect.width() + 4, rect.height(), 10, 10)
            p.setPen(WHITE)
            p.drawText(widthOfTitle + 2, top + 12, rect.width(), rect.height(), Qt.AlignCenter, self.types[ptype][1])
            p.setPen(foregroundColor)
            tagWidth = rect.width()

        # Package Summary
        p.setFont(self.normalFont)
        foregroundColor.setAlpha(160)
        p.setPen(foregroundColor)
        elided_summary = self.normalFontFM.elidedText(summary, Qt.ElideRight, width - textInner - tagWidth - 22)
        p.drawText(left + textInner, top + itemHeight / 2, width - textInner, itemHeight / 2, Qt.TextDontClip, elided_summary)
        foregroundColor.setAlpha(255)
        p.setPen(foregroundColor)

        buttonStyle = None
        if self.rowAnimator.currentRow() == index.row():
            description = index.model().data(index, DescriptionRole).toString()
            size = index.model().data(index, SizeRole).toString()
            homepage = index.model().data(index, HomepageRole).toString()
            installedVersion = str(index.model().data(index, InstalledVersionRole).toString())
            version = index.model().data(index, VersionRole)

            # Package Detail Label
            position = top + ROW_HEIGHT

            p.setFont(self.normalDetailFont)
            baseRect = QRect(left, position, width - 8, option.rect.height())
            rect = self.normalDetailFontFM.boundingRect(baseRect, Qt.TextWordWrap | Qt.TextDontClip, description)
            p.drawText(left + 2, position, width - 8, rect.height(), Qt.TextWordWrap | Qt.TextDontClip, description)

            # Package Detail Homepage
            position += rect.height() + 4

            p.setFont(self.boldDetailFont)
            p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['website'])

            p.setFont(self.normalDetailFont)
            homepage = self.normalDetailFontFM.elidedText(homepage, Qt.ElideRight, width - self._titleFM['website'])
            rect = self.normalDetailFontFM.boundingRect(option.rect, Qt.TextSingleLine, homepage)
            self.rowAnimator.hoverLinkFilter.link_rect = QRect(left + self._titleFM['website'] + 2, position + 2 + 32, rect.width(), rect.height())

            p.setPen(option.palette.color(QPalette.Link))
            p.drawText(left + self._titleFM['website'], position, width, rect.height(), Qt.TextSingleLine, homepage)
            p.setPen(foregroundColor)

            # Package Detail Version
            position += rect.height()

            p.setFont(self.boldDetailFont)
            p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['release'])

            p.setFont(self.normalDetailFont)
            rect = self.normalDetailFontFM.boundingRect(option.rect, Qt.TextWordWrap, version.toString())
            p.drawText(left + self._titleFM['release'], position, width, rect.height(), Qt.TextWordWrap, version.toString())

            if not installedVersion == '':
                position += rect.height()

                p.setFont(self.boldDetailFont)
                p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['installVers'])

                p.setFont(self.normalDetailFont)
                rect = self.normalDetailFontFM.boundingRect(option.rect, Qt.TextWordWrap, installedVersion)
                p.drawText(left + self._titleFM['installVers'], position, width, rect.height(), Qt.TextWordWrap, installedVersion)

            # Package Detail Repository
            repository = index.model().data(index, RepositoryRole).toString()
            if not repository == '':
                repository = i18n('Unknown')  if repository == 'N/A' else repository
                position += rect.height()

                p.setFont(self.boldDetailFont)
                p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['repository'])

                p.setFont(self.normalDetailFont)
                p.drawText(left + self._titleFM['repository'], position, width, itemHeight / 2, Qt.TextWordWrap, repository)

            # Package Detail Size
            position += rect.height()

            p.setFont(self.boldDetailFont)
            p.drawText(left + ICON_SIZE , position, width - textInner, itemHeight / 2, Qt.AlignLeft, self._titles['size'])

            p.setFont(self.normalDetailFont)
            p.drawText(left + self._titleFM['size'], position, width, itemHeight / 2, Qt.TextWordWrap, size)
            position += rect.height()
            self.rowAnimator.max_height = position - top + 8

            # Package More info button
            opt = QStyleOptionViewItemV4(option)

            buttonStyle = QStyleOptionButton()
            if option.state & QStyle.State_MouseOver or option.state & QStyle.State_HasFocus:
                buttonStyle.state |= QStyle.State_HasFocus
            buttonStyle.state |= QStyle.State_Enabled
            buttonStyle.text = i18n("Details")

            buttonStyle.rect = QRect(width - 100, position - 22, 100, 22)

        p.end()

        # FIXME
        # if option.state & QStyle.State_HasFocus and self.animatable:
        #     option.state |= QStyle.State_MouseOver
            # Use Plastique style to draw focus rect like MouseOver effect of Oxygen.
            # self.plastik.drawPrimitive(QStyle.PE_FrameLineEdit, option, painter, None)

        if not self.rowAnimator.running() and buttonStyle:
            if self.show_details_button and (installed or config.USE_APPINFO):
                PackageDelegate.AppStyle().drawControl(QStyle.CE_PushButton, buttonStyle, painter, None)
                self.rowAnimator.hoverLinkFilter.button_rect = QRect(buttonStyle.rect)

        painter.drawPixmap(option.rect.topLeft(), pixmap)
        del pixmap

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonRelease and index.column() == 0 and index.flags() & Qt.ItemIsUserCheckable:
            toggled = Qt.Checked if model.data(index, Qt.CheckStateRole) == QVariant(Qt.Unchecked) else Qt.Unchecked
            return model.setData(index, toggled, Qt.CheckStateRole)
        __event = QItemDelegate(self).editorEvent(event, model, option, index)
        animate_requested = False
        if event.type() == QEvent.MouseButtonRelease and self.animatable:
            if self.rowAnimator.row == index.row():
                epos = event.pos()
                if self.rowAnimator.hoverLinkFilter.link_rect.contains(QPoint(epos.x(), epos.y() + 32)):
                    url = QUrl(model.data(index, HomepageRole).toString())
                    QDesktopServices.openUrl(url)
                    return __event
                elif self.rowAnimator.hoverLinkFilter.button_rect.contains(epos, True):
                    self.showPackageDetails(model, index)
                    return __event
            animate_requested = True
        elif event.type() == QEvent.KeyPress and self.animatable:
            # KeyCode 32 : Space key
            if event.key() == 32 and index.column() == index.model().columnCount() - 1:
                animate_requested = True
        if not unicode(model.data(index, DescriptionRole).toString()) == '' and animate_requested:
            self.rowAnimator.animate(index.row())
        return __event

    def showPackageDetails(self, model, index):

        def _getter(role):
            return model.data(index, role).toString()

        name = _getter(NameRole)
        summary = _getter(SummaryRole)
        description = _getter(DescriptionRole)
        installed = model.data(index, InstalledRole).toBool()
        self.webDialog.showPackageDetails(name, installed, summary, description)

    def sizeHint(self, option, index):
        if self.rowAnimator.currentRow() == index.row() and not index.row() == 0:
            return self.rowAnimator.size()
        else:
            width = ICON_SIZE if index.column() == 0 else 0
            return QSize(width, ROW_HEIGHT)

    def setAnimatable(self, animatable):
        self.animatable = animatable

    def reset(self):
        self.rowAnimator.reset()
