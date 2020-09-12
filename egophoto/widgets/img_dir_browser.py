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

    def __init__(self, rootpath_jpeg=None):
        QWidget.__init__(self)

        self._rootpath_jpeg = rootpath_jpeg
        self._dirTreeView = None
        self._dirTreeModel = None

        button = QPushButton("Dernier répertoire")
        button.clicked.connect(self._onButtonClicked)

        self._dirTreeModel = QFileSystemModel()
        self._dirTreeModel.setRootPath(QDir.rootPath())
        self._dirTreeModel.setFilter(QDir.NoDotAndDotDot | QDir.Dirs)
        self._dirTreeView = QTreeView()
        self._dirTreeView.setModel(self._dirTreeModel)
        self._dirTreeView.setHeaderHidden(True)
        self._dirTreeView.setColumnHidden(1, True)
        self._dirTreeView.setColumnHidden(2, True)
        self._dirTreeView.setColumnHidden(3, True)
        self._dirTreeView.clicked.connect(self._onSelectDirectory)

        # select first catalog entry
        self._dirTreeView.setRootIndex(self._dirTreeModel.index(self._rootpath_jpeg))

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(button)
        splitter.addWidget(self._dirTreeView)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Albums"), 0, Qt.AlignTop)
        layout.addWidget(splitter)

        self.setLayout(layout)

    def _onButtonClicked(self):
        year = datetime.now().year
        year_dir = self._rootpath_jpeg + "/" + str(year)
        dirs = [f.path for f in os.scandir(year_dir) if f.is_dir()]
        if len(dirs) > 0:
            dirs.sort(reverse=True)
            dir_idx = self._dirTreeModel.index(dirs[0])
            self._dirTreeView.setCurrentIndex(dir_idx)
            self._onSelectDirectory(dir_idx)

    def _onSelectDirectory(self, val):
        self.selected.emit(self._dirTreeModel.filePath(val))
