# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os
from typing import Dict, List

from PySide2.QtCore import QSettings


class Preferences(QSettings):
    def __init__(self, parent=None):
        super().__init__(
            QSettings.IniFormat,
            QSettings.UserScope,
            'egophoto',
            'egophoto',
            parent)
        self.confdir = os.path.dirname(self.fileName())

        self.rootpath_jpeg: str = None

        self.xmp_locations: Dict[List[str]] = {}
        if "xmp_locations" in self.childGroups():
            self.beginGroup("xmp_locations")
            countries = self.childKeys()
            for country in countries:
                self.xmp_locations[country] = self.value(country)
            self.endGroup()

    def load(self):
        self.rootpath_jpeg = self.value('directories/jpeg')

    def save(self):
        self.setValue('directories/jpeg', self.rootpath_jpeg)
        self.sync()
