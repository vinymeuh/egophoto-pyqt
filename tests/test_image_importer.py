# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

import pytest

import errno
import os.path
import shutil

from tests.conftest import Configuration

from egophoto.exiftool.exiftool import ImageImporter


def test_dry_run():
    importer = ImageImporter(
        source_dir=Configuration.testdata_dir,
        target_dir=Configuration.imported_dir,
    )
    importer.dry_run()
    importer.waitForFinished()
    stdout = importer.readAllStandardOutput().data().decode('utf8')
    print(stdout)
    assert "0 image files updated" in stdout, "dry_run() must not update files"


def test_run():
    try:
        shutil.rmtree(Configuration.imported_dir)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

    importer = ImageImporter(
        source_dir=Configuration.testdata_dir,
        target_dir=Configuration.imported_dir,
    )
    importer.run()
    importer.waitForFinished()
    stdout = importer.readAllStandardOutput().data().decode('utf8')
    print(stdout)

    # images with valid date exif tag must have been imported
    for tc in Configuration.testdata:
        src = tc[0]
        if src != "empty.jpg":
            tgt = os.path.join(Configuration.imported_dir, tc[1])
            assert os.path.exists(tgt), f"Error importing {src} -> {tgt}"
