# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtCore import QObject, QSettings


class UiState(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._file = QSettings(QSettings.NativeFormat, QSettings.UserScope, 'egophoto', 'uistate')

    def load(self):
        pass

    def save(self):
        pass
