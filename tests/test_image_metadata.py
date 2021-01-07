import os
import shutil
import subprocess

import pytest

from egophoto.metadata import ImageMetadata



# def test_read_non_existing_file():
#     with pytest.raises(FileNotFoundError):
#         ImageMetadata("a_not_existing_file.jpg")
#
# @pytest.mark.parametrize("image,expected", testdata, ids=[x[0] for x in testdata])
# def test_read_image_metadata(image, expected):
#     path = os.path.join(tests_dir, image)
#     if image != "empty.jpg":
#         shutil.copyfile(empty_jpeg, path)
#         exiftool_write(path, expected)
#     metadata = ImageMetadata(path)
#     assert metadata.path == path
#
#     for key in expected.keys():
#         if isinstance(expected[key], list):
#             currents = getattr(metadata, key)
#             for current in currents:
#                 assert current in expected[key], f"@{key}: one of current values is not expected"
#             for expected_value in expected[key]:
#                 assert expected_value in currents, f"@{key}: one of expected values not found in expected list"
#         else:
#             assert getattr(metadata, key) == expected[key], f"@{key}: value does not match"
