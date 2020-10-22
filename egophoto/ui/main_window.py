# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from functools import partial
from typing import List

from PySide2.QtCore import (
    QPoint,
    Qt,
)
from PySide2.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QSplitter,
    QWidget,
)

from egophoto.settings import app_settings
from egophoto.ui import (
    EditXMPLocationWindow,
    PhotoInformationListWindow,
    PhotoInformationWindow,
    SlideShowWindow,
    StatusBar,
)
from egophoto.widgets import (
    ImagesSelector,
    ImagesGrid,
)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EgoPhoto")

        # attributes
        self.imagesSelector = ImagesSelector(app_settings.preferences.rootpath_jpeg)
        self.imagesGrid = ImagesGrid()
        self.images: List[str] = []
        """List of image paths displayed by the images grid"""

        # set window size
        app = QApplication.instance()  # don't like using qApp
        geometry = app.desktop().availableGeometry(self)
        self.setMinimumSize(geometry.width() * 0.5, geometry.height() * 0.5)
        self.resize(geometry.width() * 0.6, geometry.height() * 0.6)

        # central widget
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.imagesSelector)
        splitter.addWidget(self.imagesGrid)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        layout = QHBoxLayout()
        layout.addWidget(splitter)
        layout.setSpacing(0)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # status bar
        self.setStatusBar(StatusBar())

        # signals
        self.imagesSelector.imageListUpdated.connect(self.loadImagesGrid)
        self.imagesGrid.customContextMenuRequested.connect(self.showImageContextMenu)

    def closeEvent(self, event):
        pass
        #app_settings.save()

    def editXMPLocation(self, country="", city=""):
        print(self.imagesGrid.selected)
        EditXMPLocationWindow(country, city).exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            PhotoInformationListWindow(self.images).exec_()
        if event.key() == Qt.Key_F2:
            SlideShowWindow().exec_()

    def loadImagesGrid(self, images: List[str]):
        self.images = images
        self.imagesGrid.setImages(images)
        self.statusBar().setFileCount(len(images))

    def showImageContextMenu(self, point: QPoint):
        menu = QMenu(self)

        menu.addAction("Informations", partial(self.showInformations))
        menu.addSeparator()

        xmp_location = menu.addMenu("Lieu")
        xmp_location.addAction("Editer", partial(self.editXMPLocation))
        xmp_location.addSeparator()
        for country in app_settings.preferences.xmp_locations.keys():
            submenu = xmp_location.addMenu(country)
            for city in app_settings.preferences.xmp_locations.get(country):
                submenu.addAction(city, partial(self.editXMPLocation, country, city))

        xmp_type = menu.addMenu("Type")
        xmp_type.addAction("Editer")

        menu.exec_(self.imagesGrid.mapToGlobal(point))

    def showInformations(self):
        print(self.imagesGrid.selected)
        PhotoInformationWindow(self.imagesGrid.selected[0]).exec_()  # TODO
