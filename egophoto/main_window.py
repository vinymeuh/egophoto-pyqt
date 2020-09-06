# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from datetime import datetime
import os
import re

from PySide2.QtCore import (
    Qt
)
from PySide2.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QSplitter,
    QWidget
)

from egophoto.metadata.image_info import ImageInfo
from egophoto.settings import app_settings
from egophoto.widgets.catalog_browser import CatalogBrowser
from egophoto.widgets.grid_viewer import GridViewer, GridViewerDelegate
from egophoto.widgets.metadata_viewer import MetadataViewer

class MainWindow(QMainWindow):

    pattern = re.compile('.*\.(jpg|jpeg)$', re.IGNORECASE)

    def __init__(self):
        super().__init__()

        # Model
        self._jpeg_path = app_settings.preferences.rootpath_jpeg
        self._imgFileDir = None
        self._imgFileName = None

        # View
        self._setupMenu()
        self._setupStatusBar()
        self._setupImgBrowser()
        self.setCentralWidget(self._imgBrowser)

        # Set window size
        self._app = QApplication.instance()  # don't like using qApp
        geometry = self._app.desktop().availableGeometry(self)
        self.setMinimumSize(geometry.width() * 0.4, geometry.height() * 0.4)
        self.resize(geometry.width() * 0.5, geometry.height() * 0.5)

    def closeEvent(self, event):
        app_settings.save()

    def _setupImgBrowser(self):
        # left panel (catalog browser)
        leftPanelWidget = CatalogBrowser(self._jpeg_path)
        leftPanelWidget.selected.connect(self._onSelectCatalog)

        # central panel (image thumbnails)
        self._imgGridWidget = GridViewer()
        self._imgGridWidget.setItemDelegate(GridViewerDelegate())
        self._imgGridWidget.clicked.connect(self._onSelectImage)

        # right panel (image metadata)
        self._metadataViewer = MetadataViewer()

        # assembly of the three panels
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(leftPanelWidget)
        splitter.addWidget(self._imgGridWidget)
        splitter.addWidget(self._metadataViewer)

        imgBrowserLayout = QHBoxLayout()
        imgBrowserLayout.addWidget(splitter)
        imgBrowserLayout.setSpacing(0)
        imgBrowserLayout.setContentsMargins(0, 0, 0, 0)
        self._imgBrowser = QWidget()
        self._imgBrowser.setLayout(imgBrowserLayout)

    def _setupMenu(self):
        pass

    def _setupStatusBar(self):
        self.statusBar()

    def _onSelectCatalog(self, val):
        self._imgFileDir = val
        images = [val + "/" + f for f in os.listdir(val) if self.pattern.match(f)]
        images.sort()

        self._imgGridWidget.clear()
        load_start = datetime.now()
        for path in images:
            self._imgGridWidget.addItem(path)
        load_time = datetime.now() - load_start
        print(f"{len(images)} images, load time: {load_time.total_seconds()}")

    def _onSelectImage(self):
        selected = self._imgGridWidget.selectedItems()
        if len(selected) == 1:
            path = selected[0].data(Qt.DisplayRole)
            if path != self._imgFileName:
                self._metadataViewer.setFile(path)
        else:
            print(selected)
