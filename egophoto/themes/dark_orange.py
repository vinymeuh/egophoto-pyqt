# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os

from PySide2.QtGui import (
    QColor,
    QPalette,
)
from PySide2.QtWidgets import QApplication

QSS = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dark_orange.qss")


def setThemeDarkOrange(app: QApplication):
    app.setStyle('Fusion')

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#727272"))
    palette.setColor(QPalette.Highlight, QColor("#ffaa00"))
    app.setPalette(palette)

    with open(QSS, "r") as qss:
        app.setStyleSheet(qss.read())
