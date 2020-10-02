# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)


class EditXMPLocationWindow(QDialog):

    def __init__(self, country: str = "", city: str = "", parent=None):
        super().__init__(parent)
        self.setModal(True)

        self.city = QLineEdit(city)
        self.country = QLineEdit(country)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Ville:"))
        row1.addStretch()
        row1.addWidget(self.city)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Pays:"))
        row2.addStretch()
        row2.addWidget(self.country)

        row3 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        row3.addWidget(self.buttonBox)

        layout = QVBoxLayout()
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        self.setLayout(layout)
