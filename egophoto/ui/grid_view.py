# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtCore import (
    Qt,
    Signal,
)
from PySide2.QtWidgets import (
    QHBoxLayout,
    QSplitter,
    QWidget,
)

from egophoto.settings import app_settings
from egophoto.widgets import (
    ImgDirBrowser,
    ImgGridViewer,
)


class GridView(QWidget):
    directorySelected = Signal(str)
    imagesCount = Signal(int)
    image_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_dir = None
        self.current_file = None
        self.imgBrowser = ImgDirBrowser(app_settings.preferences.rootpath_jpeg)
        self.gridViewer = ImgGridViewer()
        self.selected = None

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.imgBrowser)
        splitter.addWidget(self.gridViewer)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.imgBrowser.selected.connect(self._onDirectorySelected)
        self.gridViewer.selectionModel().selectionChanged.connect(self._onImagesSelectionChanged)

    def _onDirectorySelected(self, val):
        if val == self.current_dir:
            return
        self.current_dir = val
        self.gridViewer.fromDirectory(self.current_dir)
        self.directorySelected.emit(self.current_dir)
        self.imagesCount.emit(self.gridViewer.model.rowCount())

    def _onImagesSelectionChanged(self, selected, deselected):
        images = self.gridViewer.selectionModel().selectedIndexes()
        self.selected = [images[i].data(Qt.DisplayRole) for i in range(len(images))]
        if len(self.selected) == 1:
            path = self.selected[0]
            if path != self.current_file:
                self.image_selected.emit(path)
                self.current_file = path
        else:
            self.image_selected.emit("")
