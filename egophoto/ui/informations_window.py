# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os

from PySide2.QtCore import (
    QSize,
    Qt,
)
from PySide2.QtGui import (
    QFont,
)
from PySide2.QtWidgets import (
    QDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QVBoxLayout,
)

from egophoto.metadata import ImageMetadata


class InformationsWindow(QDialog):

    bold = QFont("", weight=QFont.Bold)

    def __init__(self, path: str, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle(f"EgoPhoto - {os.path.basename(path)}")

        metadata = ImageMetadata(path)

        box1 = QGroupBox("Photos")
        layout = QVBoxLayout()
        layout.setSpacing(0)
        lbl = QLabel(metadata.date)
        lbl.setFont(InformationsWindow.bold)
        layout.addWidget(lbl)
        layout.addWidget(QLabel(f"{ metadata.city } ({metadata.country})"))
        layout.addWidget(QLabel(f"{metadata.score}/5"))   # TODO
        box1.setLayout(layout)

        box2 = QGroupBox("Catégorisation")
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(QLabel(f"Evenement: {metadata.event or ''}"))
        layout.addWidget(QLabel(f"Personnes: {str(metadata.persons)}"))
        layout.addWidget(QLabel(f"Tags     : {str(metadata.tags)}"))
        layout.addWidget(QLabel(f"Type     : {str(metadata.categories)}"))
        box2.setLayout(layout)

        box3 = QGroupBox("Prise de vue")
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(QLabel(metadata.camera_model))
        layout.addWidget(QLabel(metadata.lens))
        box3.setLayout(layout)

        box4 = QGroupBox("Auteur")
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.addWidget(QLabel("Artiste:"), 0, 0)
        layout.addWidget(QLabel(metadata.artist), 0, 1)
        layout.addWidget(QLabel("Copyright"), 1, 0)
        layout.addWidget(QLabel(metadata.copyright), 1, 1)
        box4.setLayout(layout)

        box5 = QGroupBox("Fichier")
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(QLabel(f"DéRAWtiseur: {metadata.software}"))
        box5.setLayout(layout)

        layout = QVBoxLayout()
        title = QLabel(metadata.title)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(box1)
        layout.addWidget(box2)
        layout.addWidget(box3)
        layout.addWidget(box4)
        layout.addWidget(box5)
        self.setLayout(layout)