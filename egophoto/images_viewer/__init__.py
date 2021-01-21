# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from typing import List

from PySide2.QtWidgets import (
    QStackedWidget,
    QWidget
)

from egophoto.images_viewer.images_data_model import ImagesDataModel
from egophoto.images_viewer.images_grid_view import ImagesGridView
from egophoto.images_viewer.images_list_view import ImagesListView


class ImagesViewer(QStackedWidget):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.model = ImagesDataModel()

        self.gridView = ImagesGridView()
        self.gridView.setModel(self.model)

        self.listView = ImagesListView()
        self.listView.setModel(self.model)

        self.addWidget(self.gridView)
        self.addWidget(self.listView)
        self.setCurrentIndex(0)

    def setImages(self, paths: List[str]):
        self.model.setImages(paths)

    def displayGridView(self):
        self.setCurrentIndex(0)

    def displayListView(self):
        self.setCurrentIndex(1)
        self.listView.resizeColumnsToContents()
