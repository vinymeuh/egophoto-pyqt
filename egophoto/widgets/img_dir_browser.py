# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os
from datetime import datetime

from PySide2.QtCore import (
    Qt,
    QDir,
    Signal
)
from PySide2.QtWidgets import (
    QFileSystemModel,
    QLabel,
    QPushButton,
    QSplitter,
    QTreeView,
    QVBoxLayout,
    QWidget
)


class ImgDirBrowser(QWidget):
    selected = Signal(str)

    def __init__(self, root_path=None):
        QWidget.__init__(self)

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

        button = QPushButton("Dernier répertoire")
        button.clicked.connect(self._onButtonClicked)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(button)
        splitter.addWidget(self.dirTreeView)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Albums"), 0, Qt.AlignTop)
        layout.addWidget(splitter)
        self.setLayout(layout)

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
