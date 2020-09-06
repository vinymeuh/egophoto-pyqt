# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtCore import (
    QRect,
    QSize,
    Qt,
)
from PySide2.QtWidgets import (
    QAbstractItemView,
    QListView,
    QListWidget,
    QStyle,
    QStyledItemDelegate,
)
from PySide2.QtGui import (
    QBrush,
    QImageReader,
    QPixmap,
)

THUMB_SIZE = 150


class GridViewer(QListWidget):

    def __init__(self):
        QListWidget.__init__(self,
                             iconSize=QSize(THUMB_SIZE, THUMB_SIZE),
                             movement=QListView.Static,
                             resizeMode=QListView.Adjust,
                             selectionMode=QAbstractItemView.ExtendedSelection,
                             viewMode=QListView.IconMode,
                             )


class GridViewerDelegate(QStyledItemDelegate):

    def __init__(self):
        super().__init__()

    def paint(self, painter, option, index):
        path = index.data(Qt.DisplayRole)
        rect = option.rect

        imgr = QImageReader(path)
        original_size = imgr.size()
        if original_size.width() >= original_size.height():
            scaled_size = QSize(THUMB_SIZE, original_size.height() * THUMB_SIZE / original_size.width())
        else:
            scaled_size = QSize(original_size.width() * THUMB_SIZE / original_size.height(), THUMB_SIZE)

        imgr.setScaledSize(scaled_size)
        img = imgr.read()
        pixmap = QPixmap.fromImage(img)
        pixmap_rect = QRect(rect.x(), rect.y(), pixmap.size().width(), pixmap.size().height())
        painter.drawPixmap(pixmap_rect, pixmap)

        if option.state & QStyle.State_Selected:
            highlight_color = option.palette.highlight().color()
            highlight_color.setAlpha(50)
            highlight_brush = QBrush(highlight_color)
            painter.fillRect(rect, highlight_brush)

    def sizeHint(self, option, index):
        return QSize(THUMB_SIZE, THUMB_SIZE)
