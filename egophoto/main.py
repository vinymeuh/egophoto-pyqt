# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import sys

from PySide2.QtWidgets import QApplication

from egophoto.main_window import MainWindow


def main():
    app = QApplication([])
    app.setApplicationName("EgoPhoto")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
