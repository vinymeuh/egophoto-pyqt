# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtCore import (
    Signal,
)
from PySide2.QtWidgets import (
    QTabWidget,
    QVBoxLayout,
)

from egophoto.images_selector.directory_browser_tab import DirectoryBrowserTab


class ImagesSelector(QTabWidget):
    imageListUpdated = Signal(list)

    def __init__(self, browser_dir_root: str):
        super().__init__(
            tabPosition=QTabWidget.West,
            tabBarAutoHide=False,
        )
        self.setLayout(QVBoxLayout())

        dirBrowserTab = DirectoryBrowserTab(browser_dir_root)
        # TODO: Album browser
        # TODO: Search browser

        self.addTab(dirBrowserTab, "Répertoires")
        self.setCurrentIndex(0)

        dirBrowserTab.imageListUpdated.connect(self._reemitImageListUpdated)

    def _reemitImageListUpdated(self, val):
        self.imageListUpdated.emit(val)
