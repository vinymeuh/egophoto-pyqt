# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from datetime import datetime
import os
import re

import PySide2
from PySide2.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QRect,
    QSize,
    Qt,
)
from PySide2.QtWidgets import (
    QAbstractItemView,
    QListView,
    QStyle,
    QStyledItemDelegate,
)
from PySide2.QtGui import (
    QBrush,
    QImageReader,
    QPixmap,
)

THUMB_SIZE = 150


class ImgGridViewer(QListView):

    pattern = re.compile('.*\.(jpg|jpeg)$', re.IGNORECASE)

    def __init__(self):
        super().__init__(
            iconSize=QSize(THUMB_SIZE, THUMB_SIZE),
            movement=QListView.Static,
            resizeMode=QListView.Adjust,
            selectionMode=QAbstractItemView.ExtendedSelection,
            viewMode=QListView.IconMode,
        )
        self.model = _ImgGridViewerModel()
        self.setModel(self.model)
        self.delegate = _ImgGridViewerDelegate()
        self.setItemDelegate(self.delegate)

    def addItem(self, item):
        self.model.beginResetModel()
        self.model.addItem(item)
        self.model.endResetModel()

    def clear(self):
        self.model.beginResetModel()
        self.model.items = []
        self.delegate.cache = {}
        self.model.endResetModel()

    def fromDirectory(self, path: str):
        self.model.beginResetModel()
        self.model.items = [path + "/" + f for f in os.listdir(path) if self.pattern.match(f)]
        self.model.items.sort()
        self.model.endResetModel()

    def paintEvent(self, e: PySide2.QtGui.QPaintEvent):
        print(f"{e.region()} {e.region()}")
        super().paintEvent(e)


class _ImgGridViewerModel(QAbstractListModel):

    def __init__(self):
        super().__init__()
        self.items = []

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return self.items[index.row()]

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)


class _ImgGridViewerDelegate(QStyledItemDelegate):

    def __init__(self):
        super().__init__()
        self.cache = {}

    def paint(self, painter, option, index):
        _paint_start = datetime.now()
        path = index.data()
        rect = option.rect

        if option.state & QStyle.State_Selected:
            _state = "SELECTED"
            highlight_color = option.palette.highlight().color()
            highlight_color.setAlpha(50)
            highlight_brush = QBrush(highlight_color)
            painter.fillRect(rect, highlight_brush)
        else:
            _state = "NOT SELECTED"

        if path in self.cache.keys():
            img = self.cache[path]
        else:
            img_reader = QImageReader(path)
            original_size = img_reader.size()
            if original_size.width() >= original_size.height():
                scaled_size = QSize(THUMB_SIZE, original_size.height() * THUMB_SIZE / original_size.width())
            else:
                scaled_size = QSize(original_size.width() * THUMB_SIZE / original_size.height(), THUMB_SIZE)
            img_reader.setScaledSize(scaled_size)
            img = img_reader.read()
            self.cache[path] = img

        pixmap = QPixmap.fromImage(img)
        pixmap_rect = QRect(rect.x(), rect.y(), pixmap.size().width(), pixmap.size().height())
        painter.drawPixmap(pixmap_rect, pixmap)

        _paint_time = datetime.now() - _paint_start
        print(f"PAINT - {os.path.basename(path)} - {_state:12s} - {_paint_time.total_seconds()}s")

    def sizeHint(self, option, index):
        return QSize(THUMB_SIZE, THUMB_SIZE)
