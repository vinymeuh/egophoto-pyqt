# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtWidgets import (
    QTableView,
    QWidget
)


class ImagesListView(QTableView):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
