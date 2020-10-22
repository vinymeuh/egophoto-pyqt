# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtCore import (
    QAbstractListModel,
    QModelIndex,
    Qt,
)


class ImgGridModel(QAbstractListModel):

    def __init__(self):
        super().__init__()
        self.items = []

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return self.items[index.row()]

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)
