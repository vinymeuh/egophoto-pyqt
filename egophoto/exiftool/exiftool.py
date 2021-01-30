# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from typing import Any, List

import json

from PySide2.QtCore import (
    QProcess,
)


class ExifTool(QProcess):

    def __init__(self, executable: str = "exiftool", parent=None):
        super().__init__(parent)
        self.setProcessChannelMode(QProcess.MergedChannels)
        self.executable = executable

    def execute(self, *params: List[str]) -> str:
        params_str = "\n".join(params) + "\n"
        self.write(params_str.encode("utf8"))
        self.waitForReadyRead()

        output = ""
        while self.canReadLine():
            buf = self.readLine()
            buf_str = buf.data().decode("utf8")
            if buf_str.endswith("{ready}\n"):
                break
            output += buf_str
        return output

    def execute_json(self, *params: List[str]) -> Any:
        output = self.execute("-j", *params)
        return json.loads(output)
