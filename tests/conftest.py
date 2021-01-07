# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import pytest

import errno
import os
import shutil
import subprocess


# Configuration class is used to share data between tests
class Configuration:
    tests_dir = os.path.dirname(os.path.realpath(__file__))
    empty_jpeg = os.path.join(tests_dir, "empty.jpg")
    testdata_dir = os.path.join(tests_dir, "testdata")
    imported_dir = os.path.join(tests_dir, "imported")
    testdata = [
        ("empty.jpg", None, {
            "artist": None,
            "camera_make": None,
            "camera_model": None,
            "categories": [],
            "city": None,
            "copyright": None,
            "country": None,
            "date": None,
            "event": None,
            "score": 0,
            "lens": None,
            "persons": [],
            "software": None,
            "tags": [],
            "title": None,
        }),
        ("image1.jpg", "2020/2020-02-02/20200202_120021_image1.jpg", {
            "artist": "Meuh Meuh",
            "camera_make": "NIKON CORPORATION",
            "camera_model": "NIKON D7000",
            "categories": ["black & white"],
            "city": "paris",
            "copyright": "Meuh Meuh",
            "country": "france",
            "date": "2020-02-02 12:00:21",
            "event": "birthday",
            "score": 1,
            "software": "RawTherapee",
            "tags": ["cake", "candle"],
            "title": "The Big Party",
        }),
        ("image2.jpg", "2020/2020-02-02/20200202_120025_image2.jpg", {
            "categories": ["category1"],
            "date": "2020-02-02 12:00:25",
            "persons": ["person1"],
            "tags": ["tag1"],
        }),
        ("image3.jpg", "2020/2020-01-02/20200102_091030_image3.jpg", {
            "categories": ["category1", "category2"],
            "date": "2020-01-02 09:10:30",
            "persons": ["person1", "person2"],
            "tags": ["tag1", "tag2"],
        }),
    ]


@pytest.fixture(scope="session", autouse=True)
def prepare_test_images():
    try:
        os.makedirs(Configuration.testdata_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    for tc in Configuration.testdata:
        image = tc[0]
        image_tags = tc[2]
        image_path = os.path.join(Configuration.testdata_dir, image)
        shutil.copyfile(Configuration.empty_jpeg, image_path)
        if image != "empty.jpg":
            exiftool_write(image_path, image_tags)


def exiftool_write(path, tags):
    args = ["exiftool", path, "-overwrite_original"]
    for tag in tags:
        if tag == "artist":
            args.append(f"-exif:Artist={tags[tag]}")
        if tag == "camera_make":
            args.append(f"-exif:Make={tags[tag]}")
        if tag == "camera_model":
            args.append(f"-exif:Model={tags[tag]}")
        if tag == "categories":
            for value in tags[tag]:
                args.append(f"-xmp:Type={value}")
        if tag == "city":
            args.append(f"-xmp:LocationShownCity={tags[tag]}")
        if tag == "copyright":
            args.append(f"-exif:Copyright={tags[tag]}")
        if tag == "country":
            args.append(f"-xmp:LocationShownCountryName={tags[tag]}")
        if tag == "date":
            exif_date = tags[tag].replace("-", ":")
            args.append(f"-exif:DateTimeOriginal={exif_date}")
        if tag == "event":
            args.append(f"-xmp:Event={tags[tag]}")
        if tag == "persons":
            for value in tags[tag]:
                args.append(f"-xmp:PersonInImage={value}")
        if tag == "score":
            args.append(f"-xmp:Rating={tags[tag]}")
        if tag == "software":
            args.append(f"-exif:Software={tags[tag]}")
        if tag == "tags":
            for value in tags[tag]:
                args.append(f"-xmp:Subject={value}")
        if tag == "title":
            args.append(f"-xmp:Title={tags[tag]}")

    if len(args) > 3:
        subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
