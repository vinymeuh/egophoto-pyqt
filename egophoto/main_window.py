# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
)

from egophoto.settings import app_settings
from egophoto.ui import (
    GridView,
    InfoListWindow,
    SlideShowWindow,
    StatusBar,
)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_dir = None

        self.gridView = GridView()
        self.setCentralWidget(self.gridView)

        self.setStatusBar(StatusBar())

        self.gridView.directorySelected.connect(self.setCurrentDirectory)
        self.gridView.imagesCount.connect(self.statusBar().setFileCount)
        self.gridView.image_selected.connect(self.statusBar().setFileName)

        # Set window size
        app = QApplication.instance()  # don't like using qApp
        geometry = app.desktop().availableGeometry(self)
        self.setMinimumSize(geometry.width() * 0.5, geometry.height() * 0.5)
        self.resize(geometry.width() * 0.6, geometry.height() * 0.6)

    def closeEvent(self, event):
        pass
        #app_settings.save()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            InfoListWindow(self.current_dir).exec_()
        if event.key() == Qt.Key_F2:
            SlideShowWindow().exec_()

    def setCurrentDirectory(self, path: str):
        self.current_dir = path
