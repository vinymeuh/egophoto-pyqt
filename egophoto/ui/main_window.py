# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtWidgets import (
    QApplication,
    QStackedWidget,
    QMainWindow,
)

from egophoto.settings import app_settings
from egophoto.ui.grid_view import GridView
from egophoto.ui.statusbar import StatusBar


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStatusBar(StatusBar())

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_view = GridView()
        self.central_widget.addWidget(self.grid_view)
        self.grid_view.directory_selected.connect(self.statusBar().setFileCount)
        self.grid_view.image_selected.connect(self.statusBar().setFileName)

        # Set window size
        app = QApplication.instance()  # don't like using qApp
        geometry = app.desktop().availableGeometry(self)
        self.setMinimumSize(geometry.width() * 0.4, geometry.height() * 0.4)
        self.resize(geometry.width() * 0.5, geometry.height() * 0.5)

    def closeEvent(self, event):
        app_settings.save()
