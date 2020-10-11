# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os
from typing import List

from PySide2.QtCore import (
    QSize,
    Qt,
)
from PySide2.QtGui import (
    QFont,
    QImageReader,
    QPixmap,
)
from PySide2.QtWidgets import (
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from egophoto.metadata import ImageMetadata

THUMB_SIZE = 300


class PhotoInformationWindow(QDialog):

    bold = QFont("", weight=QFont.Bold)

    def __init__(self, path: str, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle(f"EgoPhoto - {os.path.basename(path)}")

        metadata = ImageMetadata(path)

        # Photo groupbox
        photoGBx = QGroupBox("Photo")
        layout = QHBoxLayout()
        layout.setSpacing(0)

        subbox = QWidget()
        sublayout = QVBoxLayout()
        sublayout.setSpacing(0)
        lbl = QLabel(metadata.date)
        lbl.setFont(PhotoInformationWindow.bold)
        sublayout.addWidget(lbl)
        sublayout.addWidget(QLabel(f"{ metadata.city } ({metadata.country})"))
        sublayout.addWidget(QLabel(f"{metadata.score}/5"))   # TODO
        sublayout.addStretch()
        subbox.setLayout(sublayout)
        subbox.setMinimumWidth(THUMB_SIZE)

        img_reader = QImageReader(path)
        original_size = img_reader.size()
        if original_size.width() >= original_size.height():
            scaled_size = QSize(THUMB_SIZE, original_size.height() * THUMB_SIZE / original_size.width())
        else:
            scaled_size = QSize(original_size.width() * THUMB_SIZE / original_size.height(), THUMB_SIZE)
        img_reader.setScaledSize(scaled_size)
        img = img_reader.read()
        imgLbl = QLabel()
        imgLbl.setPixmap(QPixmap.fromImage(img))

        layout.addWidget(subbox, Qt.AlignTop)
        layout.addWidget(imgLbl)
        photoGBx.setLayout(layout)

        # Categorization groupbox
        categoryGBx = createGroupBox(
            "Catégorisation",
            ["Evenement:", "Personnes:", "Tags:", "Type:"],
            [f"{metadata.event or ''}", " ".join(metadata.persons), " ".join(metadata.tags), " ".join(metadata.categories)]
        )

        # Camera groupbox
        cameraGBx = QGroupBox("Prise de vue")
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(QLabel(metadata.camera_model))
        layout.addWidget(QLabel(metadata.lens))
        cameraGBx.setLayout(layout)

        # Author groupbox
        authorGBx = createGroupBox(
            "Auteur",
            ["Artiste:", "Copyright:"],
            [metadata.artist, metadata.copyright]
        )

        # File groupbox
        fileGBx = createGroupBox(
            "Fichier",
            ["Logiciel:"],
            [metadata.software]
        )

        # Final widget
        layout = QVBoxLayout()
        title = QLabel(metadata.title)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(photoGBx)
        layout.addWidget(categoryGBx)
        layout.addWidget(cameraGBx)
        layout.addWidget(authorGBx)
        layout.addWidget(fileGBx)
        self.setLayout(layout)


def createGroupBox(title: str, labels: List[str], values: List[str]) -> QGroupBox:
    box = QGroupBox(title)
    layout = QGridLayout()
    layout.setSpacing(0)

    max_length = 8 * max(len(label) for label in labels)    # TODO: compute from font size
    print(max_length)
    label0 = QLabel(labels[0])
    label0.setFixedWidth(max_length)
    layout.addWidget(label0, 0, 0)
    layout.addWidget(QLabel(values[0]), 0 , 1)

    for i in range(1, len(labels)):
        layout.addWidget(QLabel(labels[i]), i, 0)
        layout.addWidget(QLabel(values[i]), i, 1)

    box.setLayout(layout)
    return box
