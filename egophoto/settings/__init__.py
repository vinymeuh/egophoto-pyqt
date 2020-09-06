# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from egophoto.settings.preferences import Preferences
from egophoto.settings.uistate import UiState


class Settings:
    def __init__(self):
        self.preferences = Preferences()
        self.uistate = UiState()

        self.preferences.load()
        self.uistate.load()

    def save(self):
        self.preferences.save()
        self.uistate.save()


app_settings = Settings()
