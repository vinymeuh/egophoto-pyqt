# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from egophoto.metadata import ImageMetadata

COLUMN_HEADERS = ["Fichier", "Titre", "Evenement", "Tag(s)", "Personne(s)", "Type(s)", "Ville", "Pays"]


class PhotoInformationListWindow(QDialog):

    def __init__(self, images: List[str], parent=None):
        super().__init__(parent)
        self.setModal(True)

        table = QTableWidget()
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setColumnCount(len(COLUMN_HEADERS))
        table.setHorizontalHeaderLabels(COLUMN_HEADERS)

        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)

        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        table.setRowCount(len(images))
        for row in range(len(images)):
            path = images[row]
            metadata = ImageMetadata(path)
            table.setItem(row, 0, QTableWidgetItem(os.path.basename(path)))
            table.setItem(row, 1, QTableWidgetItem(metadata.title))
            table.setItem(row, 2, QTableWidgetItem(metadata.event))
            table.setItem(row, 3, QTableWidgetItem(" ".join(metadata.tags)))
            table.setItem(row, 4, QTableWidgetItem(" ".join(metadata.persons)))
            table.setItem(row, 5, QTableWidgetItem(" ".join(metadata.categories)))
            table.setItem(row, 6, QTableWidgetItem(metadata.city))
            table.setItem(row, 7, QTableWidgetItem(metadata.country))
        table.resizeColumnsToContents()
        table.setFixedWidth(table.horizontalHeader().length() + table.verticalHeader().width()+15)
        table.setFixedHeight(480)

        layout = QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)
