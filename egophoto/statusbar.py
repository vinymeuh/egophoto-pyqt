# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os

from PySide2.QtWidgets import (
    QStatusBar,
)


class StatusBar(QStatusBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filecount = 0
        self.filename = ""

    def setFileCount(self, n: int):
        self.filecount = n
        self.filename = ""
        self.refresh()

    def setFileName(self, s: str):
        self.filename = os.path.basename(s)
        self.refresh()

    def refresh(self):
        if self.filecount <= 1:
            msg = f"{self.filecount} image"
        else:
            msg = f"{self.filecount} images"

        if self.filename != "":
            msg += f"  {self.filename}"

        self.showMessage(msg)
