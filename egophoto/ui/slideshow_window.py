# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QDialog,
)


class SlideShowWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showMaximized()
        #self.showFullScreen()
