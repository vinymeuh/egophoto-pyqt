# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os
from datetime import datetime

from PySide2.QtCore import (
    QDir,
    Signal
)
from PySide2.QtWidgets import (
    QFileSystemModel,
    QPushButton,
    QTabWidget,
    QTreeView,
    QVBoxLayout,
    QWidget
)


class ImgDirBrowser(QWidget):
    selected = Signal(str)

    def __init__(self, root_path=None):
        super().__init__()

        self.root_path = root_path
        self.dirTreeView = QTreeView()
        self.dirTreeModel = QFileSystemModel()

        self.dirTreeModel.setRootPath(QDir.rootPath())
        self.dirTreeModel.setFilter(QDir.NoDotAndDotDot | QDir.Dirs)

        self.dirTreeView.setModel(self.dirTreeModel)
        self.dirTreeView.setHeaderHidden(True)
        self.dirTreeView.setColumnHidden(1, True)
        self.dirTreeView.setColumnHidden(2, True)
        self.dirTreeView.setColumnHidden(3, True)
        self.dirTreeView.clicked.connect(self._onSelectDirectory)

        # select first catalog entry
        self.dirTreeView.setRootIndex(self.dirTreeModel.index(self.root_path))

        # initialize tabs
        tabs = QTabWidget(
            tabPosition=QTabWidget.North, tabBarAutoHide=False
        )
        tab1 = QWidget()
        tab2 = QWidget()
        tabs.setCurrentIndex(0)

        tabs.addTab(tab1, "Répertoires")
        #tabs.addTab(tab2, "Albums")
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(tabs)

        # tab1
        layout1 = QVBoxLayout()
        button = QPushButton("Dernier en date")
        button.clicked.connect(self._onButtonClicked)
        layout1.addWidget(button)
        layout1.addWidget(self.dirTreeView)
        tab1.setLayout(layout1)

    def _onButtonClicked(self):
        year = datetime.now().year
        year_dir = self.root_path + "/" + str(year)
        dirs = [f.path for f in os.scandir(year_dir) if f.is_dir()]
        if len(dirs) > 0:
            dirs.sort(reverse=True)
            index = self.dirTreeModel.index(dirs[0])
            self.dirTreeView.setCurrentIndex(index)
            self.dirTreeView.scrollTo(index)
            self._onSelectDirectory(index)

    def _onSelectDirectory(self, val):
        self.selected.emit(self.dirTreeModel.filePath(val))
