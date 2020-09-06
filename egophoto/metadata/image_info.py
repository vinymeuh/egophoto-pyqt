# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os

import exiftool

_et = exiftool.ExifTool()
_et.start()

TAGS = [
    "exif:Artist",
    "exif:Copyright",
    "exif:DateTimeOriginal",
    "exif:Make",
    "exif:Model",
    "xmp-dc:Subject",
    "xmp-dc:Title",
    "xmp-dc:Type",
    "xmp-iptcext:Event",
    "xmp-iptcext:LocationShownCity",
    "xmp-iptcext:LocationShownCountryName",
    "xmp-iptcext:PersonInImage",
]


class FileInfo:
    def __init__(self, path: str):
        self.name: str = os.path.basename(path)
        self.dir: str = os.path.dirname(path)
        self.bytes: int = os.path.getsize(path)
        self.raw_name: str
        self.raw_dir: str


class Tags:
    def __init__(self, path: str):
        tags = _et.get_tags(TAGS, path)
        print(tags)
        self.exif_artist = tags.get('EXIF:Artist')
        self.exif_copyright = tags.get('EXIF:Copyright')
        self.exif_date = tags.get('EXIF:DateTimeOriginal')
        self.exif_make = tags.get('EXIF:Make')
        self.exif_model = tags.get('EXIF:Model')
        self.xmp_subject = tags.get('XMP:Subject', '')
        self.xmp_title = tags.get('XMP:Title')
        self.xmp_type = tags.get('XMP:Type', '')
        self.xmp_person = tags.get('XMP:PersonInImage', '')
        self.xmp_event = tags.get('XMP:Event')
        self.xmp_country = tags.get('XMP:LocationShownCountryName')
        self.xmp_city = tags.get('XMP:LocationShownCity')


class ImageInfo:
    def __init__(self, path: str):
        if not os.path.isfile(path):
            return
        self.path = path
        self.file = FileInfo(path)
        self.tags = Tags(path)

