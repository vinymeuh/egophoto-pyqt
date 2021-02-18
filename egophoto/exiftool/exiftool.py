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
        #self.setProcessChannelMode(QProcess.MergedChannels)
        self.executable = executable

    def execute(self, *params: List[str]) -> str:
        self.start(self.executable, *params)
        self.waitForFinished()
        stdout = self.readAllStandardOutput().data().decode('utf8')
        return stdout

    def execute_json(self, *params: List[str]) -> Any:
        output = self.execute(*params)
        jsondoc = ""
        try:
            jsondoc = json.loads(output)
        except Exception as e:
            print(f"execute_json: {e}, output={output}*****\n")
        return jsondoc
