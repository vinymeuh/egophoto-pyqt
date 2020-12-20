# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import sys

from PySide2.QtCore import QFile, QTextStream
from PySide2.QtWidgets import QApplication

from egophoto.main_window import MainWindow

# noinspection PyUnresolvedReferences
import egophoto.resources

# create the app
app = QApplication(sys.argv)
app.setApplicationName("EgoPhoto")
app.setDesktopFileName("egophoto.desktop")

# initialize the app style
app.setStyle("Fusion")
qss_file = QFile(":/qss/stylesheet.qss")
if qss_file.exists():
    qss_file.open(QFile.ReadOnly | QFile.Text)
    stylesheet = QTextStream(qss_file).readAll()
    app.setStyleSheet(stylesheet)
    qss_file.close()

# create the main window
mw = MainWindow()
mw.show()

# start the event loop
sys.exit(app.exec_())
