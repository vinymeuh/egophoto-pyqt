# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from typing import List

from PySide2.QtCore import (
    QByteArray,
)

from .exiftool import ExifTool


class ExifToolDaemon(ExifTool):

    instance = None

    def start_daemon(self):
        self.start(self.executable, ["-stay_open", "True", "-@", "-"])
        if not self.waitForStarted():
            print("unable to start exiftool daemon")

    def terminate(self) -> None:
        self.write(QByteArray("-stay_open\nFalse\n".encode("utf8")))
        self.waitForFinished()

    def __enter__(self):
        self.start_daemon()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()

    def execute(self, *params: List[str]) -> str:
        return super().execute(*params, "-execute")


def exifToolDaemon(executable: str = "exiftool") -> ExifToolDaemon:
    if ExifToolDaemon.instance is None:
        ExifToolDaemon.instance = ExifToolDaemon(executable)
        ExifToolDaemon.instance.start_daemon()
    return ExifToolDaemon.instance
