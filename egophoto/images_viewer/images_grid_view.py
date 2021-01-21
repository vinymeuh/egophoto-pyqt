# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtCore import (
    QSize,
    Qt,
)
from PySide2.QtWidgets import (
    QAbstractItemView,
    QListView,
)

from egophoto.images_viewer.images_grid_view_delegate import ImagesGridViewDelegate


class ImagesGridView(QListView):

    def __init__(self, thumb_size=150):
        super().__init__(
            iconSize=QSize(thumb_size, thumb_size),
            movement=QListView.Static,
            resizeMode=QListView.Adjust,
            selectionMode=QAbstractItemView.ExtendedSelection,
            viewMode=QListView.IconMode,
        )
        self.selected = None

        self.delegate = ImagesGridViewDelegate(thumb_size)
        self.setItemDelegate(self.delegate)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
