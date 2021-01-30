# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from typing import List

from egophoto.exiftool.exiftool_daemon import exifToolDaemon

TAGS = [
    "exif:Artist",
    "exif:Copyright",
    #"exif:DateTimeOriginal",
    #"exif.LensInfo",
    "exif:LensModel",
    # "exif:Make",
    # "exif:Model",
    # "exif:Software",
    # "xmp-dc:Subject",
    # "xmp-dc:Title",
    # "xmp-dc:Type",
    # "xmp-iptcext:Event",
    "XMP:LocationShownCity",
    "XMP:LocationShownCountryName",
    # "xmp-iptcext:PersonInImage",
    "XMP:Rating",
]
TAGS_CMDLINE = ["-G"] + ["-" + t for t in TAGS] + [""]


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

    @classmethod
    def load_from_exiftool(cls, path):
        et = exifToolDaemon()
        TAGS_CMDLINE[len(TAGS_CMDLINE)-1] = path
        img_tags = et.execute_json(*TAGS_CMDLINE)[0]
        print(img_tags)

        img = Image(path)
        img.artist = img_tags.get("EXIF:Artist", "")
        img.city = img_tags.get("XMP:LocationShownCity", "")
        img.country = img_tags.get("XMP:LocationShownCountryName", "")
        return img
