# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os
from datetime import datetime
from typing import List

from egophoto.exiftool.exiftool_daemon import exifToolDaemon

TAGS = [
    "EXIF:Artist",
    "EXIF:Copyright",
    "EXIF:DateTimeOriginal",
    "EXIF:LensInfo",
    "EXIF:LensModel",
    "EXIF:Make",
    "EXIF:Model",
    "EXIF:Software",
    "XMP:Subject",
    "XMP:Title",
    "XMP:Type",
    "XMP:Event",
    "XMP:LocationShownCity",
    "XMP:LocationShownCountryName",
    "XMP:PersonInImage",
    "XMP:Rating",
]
TAGS_CMDLINE = ["-G"] + ["-" + t for t in TAGS] + [""]


class Image:

    def __init__(self, path: str = ""):
        self.path = path
        # raw EXIF tags
        self.artist: str = ""
        self.copyright: str = None
        self.camera_make: str = None
        self.camera_model: str = None
        self._date = None
        self.lens: str = None
        self.software: str = None
        # raw XMP tags
        self.categories: List[str] = []
        self.city: str = None
        self.country: str = None
        self.event: str = None
        self.persons: List[str] = []
        self.score: int = 0
        self.tags: List[str] = []
        self.title: str = None

    @property
    def date(self):
        if self._date is None:
            return None
        else:
            date = datetime.strptime(self._date, "%Y:%m:%d %H:%M:%S")  # date format according to Exif specifications
            return date.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def load_from_exiftool(cls, path):
        if not os.path.isfile(path):
            raise FileNotFoundError
        et = exifToolDaemon()
        TAGS_CMDLINE[len(TAGS_CMDLINE)-1] = path
        img_tags = et.execute_json(*TAGS_CMDLINE)[0]

        img = Image(path)
        # EXIF
        img.artist = img_tags.get("EXIF:Artist")
        img.copyright = img_tags.get("EXIF:Copyright")
        img.camera_make = img_tags.get("EXIF:Make")
        img.camera_model = img_tags.get("EXIF:Model")
        img._date = img_tags.get('EXIF:DateTimeOriginal')
        img.lens = img_tags.get('EXIF:LensModel') or img_tags.get('EXIF:LensInfo')
        img.software = img_tags.get("EXIF:Software")
        # XMP
        img.categories = _as_list(img_tags.get('XMP:Type', []))
        img.city = img_tags.get("XMP:LocationShownCity")
        img.country = img_tags.get("XMP:LocationShownCountryName")
        img.event = img_tags.get("XMP:Event")
        img.persons = _as_list(img_tags.get('XMP:PersonInImage', []))
        img.score = img_tags.get("XMP:Rating", 0)
        img.tags = _as_list(img_tags.get('XMP:Subject', []))
        img.title = img_tags.get("XMP:Title")

        return img


def _as_list(value):
    if isinstance(value, list):
        return value
    else:
        return [value]
