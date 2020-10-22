# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from typing import List

from PySide2.QtCore import (
    QSize,
    Qt,
)
from PySide2.QtWidgets import (
    QAbstractItemView,
    QListView,
)

from egophoto.widgets.images_grid_model import ImgGridModel
from egophoto.widgets.images_grid_delegate import ImgGridDelegate


class ImagesGrid(QListView):

    def __init__(self, thumb_size=150):
        super().__init__(
            iconSize=QSize(thumb_size, thumb_size),
            movement=QListView.Static,
            resizeMode=QListView.Adjust,
            selectionMode=QAbstractItemView.ExtendedSelection,
            viewMode=QListView.IconMode,
        )
        self.selected = None

        self.model = ImgGridModel()
        self.setModel(self.model)
        self.delegate = ImgGridDelegate(thumb_size)
        self.setItemDelegate(self.delegate)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # signals
        self.selectionModel().selectionChanged.connect(self._onImagesSelectionChanged)

    def setImages(self, images: List[str]):
        self.images = images
        self.model.beginResetModel()
        self.model.items = images
        self.model.endResetModel()

    def clear(self):
        self.model.beginResetModel()
        self.model.items = []
        self.delegate.thumb_cache = {}
        self.model.endResetModel()

    def _onImagesSelectionChanged(self, selected, deselected):
        images = self.selectionModel().selectedIndexes()
        self.selected = [images[i].data(Qt.DisplayRole) for i in range(len(images))]
