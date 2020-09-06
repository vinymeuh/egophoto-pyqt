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

from egophoto.metadata.image_info import ImageInfo


class MetadataViewerItem(QWidget):
    def __init__(self, name, value=None):
        super().__init__()
        self._value = QLabel(value)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignLeft)
        label = QLabel(name)
        label.setFixedWidth(70)  # TODO - avoid fixed size
        layout.addWidget(label)
        layout.addWidget(QLabel(":"))
        layout.addWidget(self._value)
        self.setLayout(layout)

    def setValue(self, value: str):
        self._value.setText(value)
        self._value.update()


class MetadataFileGroup(QGroupBox):
    def __init__(self):
        super().__init__(title="Fichier")

        self._name = MetadataViewerItem("Nom")
        self._dir = MetadataViewerItem("Répertoire")
        self._size = MetadataViewerItem("Taille")

        layout = QVBoxLayout()
        layout.addWidget(self._name)
        layout.addWidget(self._dir)
        layout.addWidget(self._size)
        self.setLayout(layout)

    def update(self, data: ImageInfo):
        self._name.setValue(data.file.name)


class MetadataExifGroup(QGroupBox):
    def __init__(self):
        super().__init__(title="Exif")

        self._artist = MetadataViewerItem("Auteur")
        self._copyright = MetadataViewerItem("Copyright")
        self._date = MetadataViewerItem("Date")
        self._make = MetadataViewerItem("Marque")
        self._model = MetadataViewerItem("Appareil")

        layout = QVBoxLayout()
        layout.addWidget(self._artist)
        layout.addWidget(self._copyright)
        layout.addWidget(self._date)
        layout.addWidget(self._make)
        layout.addWidget(self._model)
        self.setLayout(layout)

    def update(self, data: ImageInfo):
        self._artist.setValue(data.tags.exif_artist)
        self._copyright.setValue(data.tags.exif_copyright)
        self._date.setValue(data.tags.exif_date)
        self._make.setValue(data.tags.exif_make)
        self._model.setValue(data.tags.exif_model)


class MetadataXmpGroup(QGroupBox):
    def __init__(self):
        super().__init__(title="XMP")

        self._title = MetadataViewerItem("Titre")
        self._subject = MetadataViewerItem("Sujet")
        self._type = MetadataViewerItem("Type")
        self._person = MetadataViewerItem("Personne(s)")
        self._event = MetadataViewerItem("Evènement")
        self._city = MetadataViewerItem("Ville")
        self._country = MetadataViewerItem("Pays")

        layout = QVBoxLayout()
        layout.addWidget(self._title)
        layout.addWidget(self._subject)
        layout.addWidget(self._type)
        layout.addWidget(self._person)
        layout.addWidget(self._event)
        layout.addWidget(self._city)
        layout.addWidget(self._country)
        self.setLayout(layout)

    def update(self, data: ImageInfo):
        self._title.setValue(data.tags.xmp_title)
        self._subject.setValue(str(data.tags.xmp_subject))
        self._type.setValue(str(data.tags.xmp_type))
        self._person.setValue(str(data.tags.xmp_person))
        self._event.setValue(data.tags.xmp_event)
        self._city.setValue(data.tags.xmp_city)
        self._country.setValue(data.tags.xmp_country)


class MetadataViewer(QWidget):

    def __init__(self):
        super().__init__()

        self._filegroup = MetadataFileGroup()
        self._exifgroup = MetadataExifGroup()
        self._xmpgroup = MetadataXmpGroup()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self._filegroup)
        layout.addWidget(self._exifgroup)
        layout.addWidget(self._xmpgroup)
        self.setLayout(layout)

    def setFile(self, path):
        m = ImageInfo(path)
        self._filegroup.update(m)
        self._exifgroup.update(m)
        self._xmpgroup.update(m)
