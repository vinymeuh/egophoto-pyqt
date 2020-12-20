# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os
import pathlib
from typing import Dict, List

from PySide2.QtCore import QSettings
from PySide2.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


class Settings(QSettings):

    def __init__(self, parent=None):
        super().__init__(QSettings.IniFormat, QSettings.UserScope, "egophoto", "egophoto", parent)

        self.directory_jpeg = self.value("directories/jpeg", str(pathlib.Path.home()))

        self.xmp_locations: Dict[List[str]] = {}
        if "xmp_locations" in self.childGroups():
            self.beginGroup("xmp_locations")
            countries = self.childKeys()
            for country in countries:
                self.xmp_locations[country] = self.value(country).split(",")
            self.endGroup()

        if not os.path.exists(self.fileName()):
            print(f"configuration file {self.fileName()} initialized")
            self.save()

    def save(self):
        self.setValue("directories/jpeg", self.directory_jpeg)
        self.sync()


class EditSettings(QDialog):

    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setModal(True)
        self.setWindowTitle("Preferences")

        # form
        frm_layout = QFormLayout()
        self.e_directory_jpeg = QLineEdit(self.settings.directory_jpeg)
        frm_layout.addRow("JPEG base directory:", self.e_directory_jpeg)

        self.e_xmp_locations = QTableWidget()
        self.e_xmp_locations.setColumnCount(2)
        self.e_xmp_locations.setHorizontalHeaderLabels(["Country", "Cities"])
        self.e_xmp_locations.setRowCount(len(settings.xmp_locations))
        n = 0
        for k, v in settings.xmp_locations.items():
            self.e_xmp_locations.setItem(n, 0, QTableWidgetItem(k))
            self.e_xmp_locations.setItem(n, 1, QTableWidgetItem(",".join(v)))
        frm_layout.addRow("XMP locations:", self.e_xmp_locations)

        # buttons
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.rejected.connect(self.reject)
        btn_box.accepted.connect(self.save)

        # assemble the dialog
        dlg_layout = QVBoxLayout()
        dlg_layout.addLayout(frm_layout)
        dlg_layout.addWidget(btn_box)
        self.setLayout(dlg_layout)

    def save(self):
        self.settings.directory_jpeg = self.e_directory_jpeg.text()
        self.settings.save()
        self.accept()
