# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from typing import List


class Image:

    def __init__(self, path: str = ""):
        self.path = path
        # attributes for raw metadata tags
        self.artist: str = ""
        self.camera_make: str = ""
        self.camera_model: str = ""
        self.categories: List[str] = []
        self.city: str = ""
        self.copyright: str = ""
        self.country: str = ""
        self.event: str = ""
        self.lens: str = ""
        self.persons: List[str] = []
        self.score: int = 0
        self.software: str = ""
        self.tags: List[str] = []
        self.title: str = ""
        # attributes derived from a raw metadata tag
        self._date = ""
