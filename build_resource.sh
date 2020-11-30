#!/usr/bin/env bash

python resources/qss/build_qss.py
rm -f egophoto/resources.py
pyside2-rcc --verbose resources/resources.qrc -o egophoto/resources.py
