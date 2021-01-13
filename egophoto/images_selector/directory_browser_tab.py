# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os
import re
from datetime import datetime

from PySide2.QtCore import (
    QDir,
    QModelIndex,
    Signal,
)
from PySide2.QtWidgets import (
    QFileSystemModel,
    QPushButton,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

FILE_PATTERN = re.compile('.*\.(jpg|jpeg)$', re.IGNORECASE)


class DirectoryBrowserTab(QWidget):

    imageListUpdated = Signal(list)

    def __init__(self, browser_dir_root: str, parent=None):
        super().__init__(parent)
        self.browser_dir_root = browser_dir_root

        self.dirTreeModel = QFileSystemModel()
        self.dirTreeModel.setRootPath(QDir.rootPath())
        self.dirTreeModel.setFilter(QDir.NoDotAndDotDot | QDir.Dirs)

        self.dirTreeView = QTreeView()
        self.dirTreeView.setModel(self.dirTreeModel)
        self.dirTreeView.setRootIndex(self.dirTreeModel.index(self.browser_dir_root))

        self.dirTreeView.setHeaderHidden(True)
        self.dirTreeView.setColumnHidden(1, True)
        self.dirTreeView.setColumnHidden(2, True)
        self.dirTreeView.setColumnHidden(3, True)

        layout = QVBoxLayout()
        layout.addWidget(self.dirTreeView)
        button = QPushButton("Dernier en date")
        layout.addWidget(button)
        self.setLayout(layout)
        self.dirTreeView.clicked.connect(self._onDirectorySelected)
        button.clicked.connect(self._onButtonClicked)

    def _onButtonClicked(self):
        for year in range(datetime.now().year, 1999, -1):
            year_dir = self.browser_dir_root + "/" + str(year)
            if os.path.isdir(year_dir):
                dirs = [f.path for f in os.scandir(year_dir) if f.is_dir()]
                if len(dirs) > 0:
                    dirs.sort(reverse=True)
                    index = self.dirTreeModel.index(dirs[0])
                    self.dirTreeView.setCurrentIndex(index)
                    self.dirTreeView.scrollTo(index)
                    self._onDirectorySelected(index)
                    break

    def _onDirectorySelected(self, val: QModelIndex):
        dir_path = self.dirTreeModel.filePath(val)
        images = [dir_path + "/" + f for f in os.listdir(dir_path) if FILE_PATTERN.match(f)]
        images.sort()
        self.imageListUpdated.emit(images)
