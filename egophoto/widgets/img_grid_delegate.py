# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os
from datetime import datetime

from PySide2.QtCore import (
    QRect,
    QSize,
    Qt,
)
from PySide2.QtWidgets import (
    QStyle,
    QStyledItemDelegate,
)
from PySide2.QtGui import (
    QColor,
    QImageReader,
    QPainterPath,
    QPen,
    QPixmap,
)

IMAGE_THUMB_RATIO = 0.9
IMAGE_THUMB_OFFSET = 0.5 * (1 - IMAGE_THUMB_RATIO)

class ImgGridDelegate(QStyledItemDelegate):

    def __init__(self, thumb_size: int):
        super().__init__()
        self.thumb_size = thumb_size    # size of image thumbnail + borders
        self.thumb_cache = {}

    def paint(self, painter, option, index):
        _paint_start = datetime.now()
        path = index.data()
        rect = option.rect

        # retrieve or prepare image thumbnail
        if path in self.thumb_cache.keys():
            img = self.thumb_cache[path]
        else:
            img_reader = QImageReader(path)
            original_size = img_reader.size()
            if original_size.width() >= original_size.height():
                scaled_size = QSize(
                    IMAGE_THUMB_RATIO * self.thumb_size,
                    original_size.height() * self.thumb_size / original_size.width()
                )
            else:
                scaled_size = QSize(
                    original_size.width() * self.thumb_size / original_size.height(),
                    IMAGE_THUMB_RATIO * self.thumb_size
                )
            img_reader.setScaledSize(scaled_size)
            img = img_reader.read()
            self.thumb_cache[path] = img

        # draw thumbnail centered in rect
        pixmap = QPixmap.fromImage(img)
        if pixmap.size().width() >= pixmap.size().height():
            pixmap_rect = QRect(
                rect.x()+IMAGE_THUMB_OFFSET*self.thumb_size,
                rect.y()+0.5*(self.thumb_size-pixmap.size().height()),
                pixmap.size().width(),
                pixmap.size().height()
            )
        else:
            pixmap_rect = QRect(
                rect.x()+0.5*(self.thumb_size-pixmap.size().width()),
                rect.y()+IMAGE_THUMB_OFFSET*self.thumb_size,
                pixmap.size().width(),
                pixmap.size().height()
            )
        painter.drawPixmap(pixmap_rect, pixmap)

        # draw the rectangle around the whole thumbnail
        pen = QPen(qApp.palette().window().color())
        painter.setPen(pen)
        rect_border = QPainterPath()
        rect_border.addRect(rect)
        painter.drawPath(rect_border)

        # draw the selection rectangle around the image if any
        if option.state & QStyle.State_Selected:
            _state = "SELECTED"
            painter.setBrush(Qt.NoBrush)
            pen = QPen(option.palette.highlight().color())
            pen.setWidth(2)
            painter.setPen(pen)
            rect_border = QPainterPath()
            rect_border.addRect(pixmap_rect)
            painter.drawPath(rect_border)
        else:
            _state = "NOT SELECTED"

        _paint_time = datetime.now() - _paint_start
        #print(f"PAINT - {os.path.basename(path)} - {_state:12s} - {_paint_time.total_seconds()}s")

    def sizeHint(self, option, index):
        return QSize(self.thumb_size, self.thumb_size)
