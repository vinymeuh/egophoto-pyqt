# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os
from typing import Any, List

from PySide2.QtCore import (
    QAbstractItemModel,
    QModelIndex,
    Qt,
)

from egophoto.images_viewer.image import Image


class ImagesDataModel(QAbstractItemModel):

    def __init__(self):
        super().__init__()
        self.images = []

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 1

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.images)

    def parent(self, index: QModelIndex) -> QModelIndex:
        return QModelIndex()

    def index(self, row, column, parent) -> QModelIndex:
        index = self.createIndex(row, column, self.images[row].path)
        if index is None:
            return QModelIndex()
        else:
            return index

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "Fichier"
        return super().headerData(section, orientation, role)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        row = index.row()
        column = index.column()
        image = self.images[row]
        if role == Qt.DisplayRole:
            if column == 0:
                return os.path.basename(image.path)

    def setImages(self, paths: List[str]):
        self.beginResetModel()
        self.images = []
        for path in paths:
            img = Image()
            img.setPath(path)
            self.images.append(img)
        self.endResetModel()
