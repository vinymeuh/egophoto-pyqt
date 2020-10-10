# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtCore import (
    Qt,
)
from PySide2.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget
)

from egophoto.metadata.image_metadata import ImageMetadata


class ImgTagViewerItem(QWidget):
    def __init__(self, name: str, value: str = ""):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignLeft)

        label = QLabel(name)
        label.setFixedWidth(70)  # TODO - avoid fixed size
        self._value = QLabel(value)
        layout.addWidget(label)
        layout.addWidget(QLabel(":"))
        layout.addWidget(self._value)

    def clear(self):
        self._value.clear()

    def setValue(self, value: str):
        self._value.setText(value)
        self._value.update()


class ImgTagViewer(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignTop)
        file_group = QGroupBox(title="Fichier")
        exif_group = QGroupBox(title="Exif")
        xmp_group = QGroupBox(title="XMP")
        layout.addWidget(file_group)
        layout.addWidget(exif_group)
        layout.addWidget(xmp_group)

        # file_group
        self._name = ImgTagViewerItem("Nom")
        self._dir = ImgTagViewerItem("Répertoire")
        self._size = ImgTagViewerItem("Taille")
        file_layout = QVBoxLayout()
        file_group.setLayout(file_layout)
        file_layout.addWidget(self._name)
        file_layout.addWidget(self._dir)
        file_layout.addWidget(self._size)

        # exif_group
        self._artist = ImgTagViewerItem("Auteur")
        self._copyright = ImgTagViewerItem("Copyright")
        self._date = ImgTagViewerItem("Date")
        self._make = ImgTagViewerItem("Marque")
        self._model = ImgTagViewerItem("Appareil")
        exif_layout = QVBoxLayout()
        exif_group.setLayout(exif_layout)
        exif_layout.addWidget(self._artist)
        exif_layout.addWidget(self._copyright)
        exif_layout.addWidget(self._date)
        exif_layout.addWidget(self._make)
        exif_layout.addWidget(self._model)

        # xmp_group
        self._title = ImgTagViewerItem("Titre")
        self._subject = ImgTagViewerItem("Sujet")
        self._type = ImgTagViewerItem("Type")
        self._person = ImgTagViewerItem("Personne(s)")
        self._event = ImgTagViewerItem("Evènement")
        self._city = ImgTagViewerItem("Ville")
        self._country = ImgTagViewerItem("Pays")
        xmp_layout = QVBoxLayout()
        xmp_group.setLayout(xmp_layout)
        xmp_layout.addWidget(self._title)
        xmp_layout.addWidget(self._subject)
        xmp_layout.addWidget(self._type)
        xmp_layout.addWidget(self._person)
        xmp_layout.addWidget(self._event)
        xmp_layout.addWidget(self._city)
        xmp_layout.addWidget(self._country)

    def clear(self):
        # file_group
        self._name.clear()
        # exif_group
        self._artist.clear()
        self._copyright.clear()
        self._date.clear()
        self._make.clear()
        self._model.clear()
        # xmp_group
        self._title.clear()
        self._subject.clear()
        self._type.clear()
        self._person.clear()
        self._event.clear()
        self._city.clear()
        self._country.clear()

    def setFile(self, path):
        info = ImageMetadata(path)

        # file_group
        self._name.setValue(info.file.name)
        # exif_group
        self._artist.setValue(info.tags.artist)
        self._copyright.setValue(info.tags.copyright)
        self._date.setValue(info.tags.date)
        self._make.setValue(info.tags.camera_make)
        self._model.setValue(info.tags.camera_model)
        # xmp_group
        self._title.setValue(info.tags.title)
        self._subject.setValue(str(info.tags.tags))
        self._type.setValue(str(info.tags.categories))
        self._person.setValue(str(info.tags.persons))
        self._event.setValue(info.tags.event)
        self._city.setValue(info.tags.city)
        self._country.setValue(info.tags.country)
