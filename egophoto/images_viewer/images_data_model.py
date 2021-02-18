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

HEADERS = [
    "Fichier",
    "Titre",
    "Evenement",
    "Tag(s)",
    "Personne(s)",
    "Type(s)",
    "Ville",
    "Pays",
]


class ImagesDataModel(QAbstractItemModel):

    def __init__(self):
        super().__init__()
        self.images = []

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(HEADERS)

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
            return HEADERS[section]
        return super().headerData(section, orientation, role)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        row = index.row()
        column = index.column()
        image = self.images[row]
        if role == Qt.DisplayRole:
            if column == 0:
                return os.path.basename(image.path)
            if column == 1:
                return image.title
            if column == 2:
                return image.event
            if column == 3:
                return " ".join(image.tags)
            if column == 4:
                return " ".join(image.persons)
            if column == 5:
                return " ".join(image.categories)
            if column == 6:
                return image.city
            if column == 7:
                return image.country

    def setImages(self, paths: List[str]):
        self.beginResetModel()
        self.images = Image.load_batch_from_exiftool(paths)
        self.endResetModel()
