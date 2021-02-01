# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import os

import pytest

from tests.conftest import Configuration

from egophoto.images_viewer.image import Image


def test_read_non_existing_file():
    with pytest.raises(FileNotFoundError):
        Image.load_from_exiftool("a_not_existing_file.jpg")


@pytest.mark.parametrize("src_path, dummy, expected", Configuration.testdata)
def test_load_from_exiftool(src_path, dummy, expected):
    path = os.path.join(Configuration.testdata_dir, src_path)
    image = Image.load_from_exiftool(path)
    for key in expected.keys():
        if isinstance(expected[key], list):
            currents = getattr(image, key)
            for current in currents:
                assert current in expected[key], f"@{key}: one of current values is not expected"
            for expected_value in expected[key]:
                assert expected_value in currents, f"@{key}: one of expected values not found in expected list"
        else:
            assert getattr(image, key) == expected[key], f"@{key}: value does not match"
