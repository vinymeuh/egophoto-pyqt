# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os
from datetime import datetime

from PySide2.QtCore import (
    QRect,
    QSize,
)
from PySide2.QtWidgets import (
    QStyle,
    QStyledItemDelegate,
)
from PySide2.QtGui import (
    QBrush,
    QImageReader,
    QPixmap,
)


class ImgGridDelegate(QStyledItemDelegate):

    def __init__(self, thumb_size: int):
        super().__init__()
        self.thumb_cache = {}
        self.thumb_size = thumb_size

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

        if path in self.thumb_cache.keys():
            img = self.thumb_cache[path]
        else:
            img_reader = QImageReader(path)
            original_size = img_reader.size()
            if original_size.width() >= original_size.height():
                scaled_size = QSize(self.thumb_size, original_size.height() * self.thumb_size / original_size.width())
            else:
                scaled_size = QSize(original_size.width() * self.thumb_size / original_size.height(), self.thumb_size)
            img_reader.setScaledSize(scaled_size)
            img = img_reader.read()
            self.thumb_cache[path] = img

        pixmap = QPixmap.fromImage(img)
        pixmap_rect = QRect(rect.x(), rect.y(), pixmap.size().width(), pixmap.size().height())
        painter.drawPixmap(pixmap_rect, pixmap)

        _paint_time = datetime.now() - _paint_start
        print(f"PAINT - {os.path.basename(path)} - {_state:12s} - {_paint_time.total_seconds()}s")

    def sizeHint(self, option, index):
        return QSize(self.thumb_size, self.thumb_size)
