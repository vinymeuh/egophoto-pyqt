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

ATTRIBUTES_MAPPING = [
    ("Fichier", lambda x: os.path.basename(x.path)),
    ("Titre", lambda x: x.title),
    ("Evenement", lambda x: x.event),
    ("Tag(s)", lambda x: x.tags),
    ("Personne(s)", lambda x: x.persons),
    ("Type(s)", lambda x: x.categories),
    ("Ville", lambda x: x.city),
    ("Pays", lambda x: x.country),
]


class ImagesDataModel(QAbstractItemModel):

    def __init__(self):
        super().__init__()
        self.images = []

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(ATTRIBUTES_MAPPING)

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
            return ATTRIBUTES_MAPPING[section][0]
        return super().headerData(section, orientation, role)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        row = index.row()
        column = index.column()
        image = self.images[row]
        if role == Qt.DisplayRole:
            f = ATTRIBUTES_MAPPING[column][1]
            return f(image)

    def setImages(self, paths: List[str]):
        self.beginResetModel()
        self.images = Image.load_batch_from_exiftool(paths)
        self.endResetModel()
