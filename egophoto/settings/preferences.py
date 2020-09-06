# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtCore import QObject, QSettings


class Preferences(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'egophoto', 'egophoto')

        self.rootpath_jpeg: str = None

    def load(self):
        self.rootpath_jpeg = self._settings.value('directories/jpeg')

    def save(self):
        self._settings.setValue('directories/jpeg', self.rootpath_jpeg)
        self._settings.sync()
