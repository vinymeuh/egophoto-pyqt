# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from functools import partial
from typing import List

from PySide2.QtCore import (
    QPoint,
    Qt,
)
from PySide2.QtWidgets import (
    QAction,
    QActionGroup,
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QSplitter,
    QWidget,
)

import egophoto.about
import egophoto.import_images
import egophoto.images_selector
import egophoto.settings
import egophoto.ui

from egophoto.images_viewer import ImagesViewer


class MainWindow(QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.settings = egophoto.settings.Settings()

        self.images: List[str] = []
        self.imagesSelector = egophoto.images_selector.ImagesSelector(self.settings.directory_jpeg)
        self.imagesViewer = ImagesViewer()

        # set window size
        app = QApplication.instance()
        geometry = app.desktop().availableGeometry(self)
        self.setMinimumSize(geometry.width() * 0.5, geometry.height() * 0.5)
        self.resize(geometry.width() * 0.7, geometry.height() * 0.7)

        # setup the ui
        self.setWindowTitle("EgoPhoto")
        self._setCentralWidget()
        self._setCreateActions()
        self._setMenuBar()
        self.setStatusBar(egophoto.ui.StatusBar())

        # signals
        self.imagesSelector.imageListUpdated.connect(self.displayImages)

    def closeEvent(self, event):
        pass

    def _setCentralWidget(self) -> None:
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.imagesSelector)
        splitter.addWidget(self.imagesViewer)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        layout = QHBoxLayout()
        layout.addWidget(splitter)
        layout.setSpacing(0)

        cw = QWidget()
        cw.setLayout(layout)
        self.setCentralWidget(cw)

    def _setCreateActions(self) -> None:
        self.aboutAction = QAction("A propos", self)
        self.aboutAction.triggered.connect(lambda: egophoto.about.About(self).exec_())

        self.exitAction = QAction("Quitter", self)
        self.exitAction.triggered.connect(self.close)

        self.importAction = QAction("Importer des images ...", self)
        self.importAction .triggered.connect(lambda: egophoto.import_images.ImportImagesDialog(self.settings, self).exec_())

        self.settingsAction = QAction("Configuration", self)
        self.settingsAction.triggered.connect(lambda: egophoto.settings.EditSettings(self.settings, self).exec_())

        self.viewGridAction = QAction("Vignette")
        self.viewGridAction.setCheckable(True)
        self.viewGridAction.setChecked(True)
        self.viewGridAction.triggered.connect(self.imagesViewer.displayGridView)
        self.viewListAction = QAction("Liste")
        self.viewListAction.setCheckable(True)
        self.viewListAction.triggered.connect(self.imagesViewer.displayListView)
        view_action_group = QActionGroup(self)
        view_action_group.addAction(self.viewGridAction)
        view_action_group.addAction(self.viewListAction)

    def _setMenuBar(self) -> None:
        menu = self.menuBar()
        # File
        file_menu = menu.addMenu("Fichier")
        file_menu.addAction(self.importAction)
        file_menu.addSeparator()
        file_menu.addAction(self.exitAction)
        # View
        view_menu = menu.addMenu("Vue")
        view_menu.addAction(self.viewGridAction)
        view_menu.addAction(self.viewListAction)
        # Tools
        tools_menu = menu.addMenu("Outils")
        tools_menu.addAction(self.settingsAction)
        # Help
        help_menu = menu.addMenu("Aide")
        help_menu.addAction(self.aboutAction)

    def editXMPLocation(self, country="", city=""):
        print(self.imagesGrid.selected)
        egophoto.ui.EditXMPLocationWindow(country, city).exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            self.viewGridAction.setChecked(True)
            self.imagesViewer.displayGridView()
        if event.key() == Qt.Key_F2:
            self.viewListAction.setChecked(True)
            self.imagesViewer.displayListView()

    def displayImages(self, images: List[str]):
        self.images = images
        self.imagesViewer.setImages(images)
        self.statusBar().setFileCount(len(images))

    def showImageContextMenu(self, point: QPoint):
        menu = QMenu(self)

        xmp_location = menu.addMenu("Lieu")
        xmp_location.addAction("Editer", partial(self.editXMPLocation))
        xmp_location.addSeparator()
        for country in self.settings.xmp_locations.keys():
            submenu = xmp_location.addMenu(country)
            for city in self.settings.xmp_locations.get(country):
                submenu.addAction(city, partial(self.editXMPLocation, country, city))

        xmp_type = menu.addMenu("Type")
        xmp_type.addAction("Editer")

        menu.exec_(self.imagesGrid.mapToGlobal(point))
