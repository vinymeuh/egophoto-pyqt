# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os
from datetime import datetime

import exiftool

_et = exiftool.ExifTool()
_et.start()

TAGS = [
    "exif:Artist",
    "exif:Copyright",
    "exif:DateTimeOriginal",
    "exif.LensInfo",
    "exif:LensModel",
    "exif:Make",
    "exif:Model",
    "exif:Software",
    "xmp-dc:Subject",
    "xmp-dc:Title",
    "xmp-dc:Type",
    "xmp-iptcext:Event",
    "xmp-iptcext:LocationShownCity",
    "xmp-iptcext:LocationShownCountryName",
    "xmp-iptcext:PersonInImage",
    "xmp-xmp:Rating",
]


class ImageMetadata:
    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise FileNotFoundError
        self.path = path

        metadata = _et.get_tags(TAGS, path)

        self.artist = metadata.get('EXIF:Artist')
        self.camera_make = metadata.get('EXIF:Make')
        self.camera_model = metadata.get('EXIF:Model')
        self.categories = _as_list(metadata.get('XMP:Type', []))
        self.city = metadata.get('XMP:LocationShownCity')
        self.copyright = metadata.get('EXIF:Copyright')
        self.country = metadata.get('XMP:LocationShownCountryName')
        self.event = metadata.get('XMP:Event')
        self.lens = metadata.get('EXIF:LensModel') or metadata.get('EXIF:LensInfo')
        self.persons = _as_list(metadata.get('XMP:PersonInImage', []))
        self.score = metadata.get('XMP:Rating', 0)
        self.software = metadata.get('EXIF:Software')
        self.tags = _as_list(metadata.get('XMP:Subject', []))
        self.title = metadata.get('XMP:Title')

        self._date = metadata.get('EXIF:DateTimeOriginal')
        print(self._date)

    @property
    def date(self):
        if self._date is None:
            return None
        else:
            date = datetime.strptime(self._date, "%Y:%m:%d %H:%M:%S")  # date format according to Exif specifications
            return date.strftime("%Y-%m-%d %H:%M:%S")


def _as_list(value):
    if isinstance(value, list):
        return value
    else:
        return [value]
