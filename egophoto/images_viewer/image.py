# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os
from datetime import datetime
from typing import List

from egophoto.exiftool.exiftool import ExifTool

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
    def load_batch_from_exiftool(cls, paths):
        exiftool_args = ["-G", "-j"] + ["-" + t for t in TAGS] + paths
        et = ExifTool()
        images_json_list = et.execute_json(exiftool_args)

        images = []
        for image_json in images_json_list:
            image = Image(image_json['SourceFile'])
            # EXIF
            image.artist = image_json.get("EXIF:Artist")
            image.copyright = image_json.get("EXIF:Copyright")
            image.camera_make = image_json.get("EXIF:Make")
            image.camera_model = image_json.get("EXIF:Model")
            image._date = image_json.get('EXIF:DateTimeOriginal')
            image.lens = image_json.get('EXIF:LensModel') or image_json.get('EXIF:LensInfo')
            image.software = image_json.get("EXIF:Software")
            # XMP
            image.categories = _as_list(image_json.get('XMP:Type', []))
            image.city = image_json.get("XMP:LocationShownCity")
            image.country = image_json.get("XMP:LocationShownCountryName")
            image.event = image_json.get("XMP:Event")
            image.persons = _as_list(image_json.get('XMP:PersonInImage', []))
            image.score = image_json.get("XMP:Rating", 0)
            image.tags = _as_list(image_json.get('XMP:Subject', []))
            image.title = image_json.get("XMP:Title")

            images.append(image)
        return images


def _as_list(value):
    if isinstance(value, list):
        return value
    else:
        return [value]
