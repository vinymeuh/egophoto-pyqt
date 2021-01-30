# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtCore import (
    QProcess
)


class ImageImporter(QProcess):

    def __init__(self, source_dir, target_dir, executable: str = "exiftool", parent=None):
        super().__init__(parent)
        self.setProcessChannelMode(QProcess.MergedChannels)
        self.executable = executable
        self.source_dir = source_dir
        self.target_dir = target_dir

    def dry_run(self):
        exiftool_args = [
            "-d", f"{self.target_dir}/%Y/%Y-%m-%d/%Y%m%d_%H%M%S_%%f.%%e",
            "-testname<CreateDate",
            "-testname<DateTimeOriginal",
            self.source_dir,
        ]
        self.start(self.executable, exiftool_args)

    def run(self):
        exiftool_args = [
            "-o", "/dummy",
            "-d", f"{self.target_dir}/%Y/%Y-%m-%d/%Y%m%d_%H%M%S_%%f.%%e",
            "-testname<CreateDate",
            "-filename<DateTimeOriginal",
            self.source_dir
        ]
        self.start(self.executable, exiftool_args)
