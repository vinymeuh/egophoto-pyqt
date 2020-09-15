# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from datetime import datetime
import os
import re

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
    ImgGridViewerDelegate,
    ImgTagViewer,
)


class GridView(QWidget):
    directory_selected = Signal(int)
    image_selected = Signal(str)

    pattern = re.compile('.*\.(jpg|jpeg)$', re.IGNORECASE)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file = None

        dirBrowser = ImgDirBrowser(app_settings.preferences.rootpath_jpeg)
        dirBrowser.selected.connect(self._onSelectDirectory)

        self._gridViewer = ImgGridViewer()
        self._gridViewer.setItemDelegate(ImgGridViewerDelegate())
        self._gridViewer.clicked.connect(self._onSelectImage)

        self._tagViewer = ImgTagViewer()

        # assembly of the three widgets
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(dirBrowser)
        splitter.addWidget(self._gridViewer)
        splitter.addWidget(self._tagViewer)

        layout = QHBoxLayout()
        layout.addWidget(splitter)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def _onSelectDirectory(self, val):
        images = [val + "/" + f for f in os.listdir(val) if self.pattern.match(f)]
        images.sort()
        self.directory_selected.emit(len(images))

        self._gridViewer.clear()
        self._tagViewer.clear()
        load_start = datetime.now()
        for path in images:
            self._gridViewer.addItem(path)
        load_time = datetime.now() - load_start
        print(f"{len(images)} images, load time: {load_time.total_seconds()}")

    def _onSelectImage(self):
        selected = self._gridViewer.selectedItems()
        if len(selected) == 1:
            path = selected[0].data(Qt.DisplayRole)
            if path != self.current_file:
                self._tagViewer.setFile(path)
                self.image_selected.emit(path)
        else:
            self._tagViewer.clear()
            self.image_selected.emit("")
