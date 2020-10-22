# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import sys

from PySide2.QtWidgets import QApplication

from egophoto.ui.main_window import MainWindow
import egophoto.resources

from PySide2.QtCore import QFile, QTextStream


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("EgoPhoto")

    app.setStyle("Fusion")

    qss_file = QFile(":/qss/stylesheet.qss")
    if qss_file.exists():
        qss_file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = QTextStream(qss_file).readAll()
        app.setStyleSheet(stylesheet)
        qss_file.close()

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
