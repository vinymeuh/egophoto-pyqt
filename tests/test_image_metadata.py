import os
import shutil
import subprocess

import pytest

from egophoto.metadata import ImageMetadata

tests_dir = os.path.dirname(os.path.realpath(__file__))
empty_jpeg = os.path.join(tests_dir, "empty.jpg")

testdata = [
    ("empty.jpg", {
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
    ("image1.jpg", {
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
    ("image2.jpg", {
        "categories": ["category1"],
        "persons": ["person1"],
        "tags": ["tag1"],
    }),
    ("image3.jpg", {
        "categories": ["category1", "category2"],
        "persons": ["person1", "person2"],
        "tags": ["tag1", "tag2"],
    }),
]

def test_read_non_existing_file():
    with pytest.raises(FileNotFoundError):
        ImageMetadata("a_not_existing_file.jpg")

@pytest.mark.parametrize("image,expected", testdata, ids=[x[0] for x in testdata])
def test_read_image_metadata(image, expected):
    path = os.path.join(tests_dir, image)
    if image != "empty.jpg":
        shutil.copyfile(empty_jpeg, path)
        exiftool_write(path, expected)
    metadata = ImageMetadata(path)
    assert metadata.path == path

    for key in expected.keys():
        if isinstance(expected[key], list):
            currents = getattr(metadata, key)
            for current in currents:
                assert current in expected[key], f"@{key}: one of current values is not expected"
            for expected_value in expected[key]:
                assert expected_value in currents, f"@{key}: one of expected values not found in expected list"
        else:
            assert getattr(metadata, key) == expected[key], f"@{key}: value does not match"


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
        subprocess.run(args)
