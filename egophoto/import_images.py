# Copyright 2020 VinyMeuh. All rights reserved.
# Use of the source code is governed by a MIT-style license that can be found in the LICENSE file.

from PySide2.QtWidgets import (
    QAbstractButton,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from egophoto.settings import Settings
from egophoto.exiftool.image_importer import ImageImporter


class ImportImagesDialog(QDialog):

    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setModal(True)
        self.resize(1200, 600)  # TODO: compute from desktop or main_window geometry
        self.setWindowTitle("Import Images")

        self.dir_from = self.settings.directory_input
        self.dir_to = self.settings.directory_raw

        # form
        frm_layout = QFormLayout()
        frm_layout.addRow("Import from:", QLabel(self.dir_from))

        self.e_target_choice = QComboBox()
        self.e_target_choice.addItems(["JPEGs", "RAWs"])
        self.e_target_choice.setCurrentText("RAWs")
        self.e_target_choice.currentIndexChanged.connect(self.current_target_changed)
        frm_layout.addRow("Import to:", self.e_target_choice)

        # text frame to display exiftool output
        self.exiftool_preview = QTextEdit()
        self.exiftool_preview.setReadOnly(True)
        preview_box = QGroupBox("Preview output")
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self.exiftool_preview)
        preview_box.setLayout(preview_layout)

        self.exiftool_import = QTextEdit()
        self.exiftool_import.setReadOnly(True)
        import_box = QGroupBox("Import output")
        import_layout = QVBoxLayout()
        import_layout.addWidget(self.exiftool_import)
        import_box.setLayout(import_layout)

        # buttons
        self.import_button = QPushButton("Import")
        self.import_button.setProperty("ActionRole", "import")
        self.button_box = QDialogButtonBox(QDialogButtonBox.Close)
        self.button_box.addButton(self.import_button, QDialogButtonBox.ActionRole)
        self.button_box.clicked.connect(self.button_clicked)

        # assemble the dialog
        dlg_layout = QVBoxLayout()
        dlg_layout.addLayout(frm_layout)
        dlg_layout.addWidget(preview_box)
        dlg_layout.addWidget(import_box)
        dlg_layout.addWidget(self.button_box)
        self.setLayout(dlg_layout)

        # run exiftool in dry run mode
        if self.dir_from != "" and self.dir_to != "":
            self.import_task()

    def current_target_changed(self, i: int):
        if i == 0:
            self.dir_to = self.settings.directory_jpeg
        else:
            self.dir_to = self.settings.directory_raw
        self.import_task()

    def button_clicked(self, button: QAbstractButton):
        sb = self.button_box.standardButton(button)
        if sb == QDialogButtonBox.StandardButton.Close:
            self.reject()
        if sb == QDialogButtonBox.StandardButton.NoButton:
            role = button.property("ActionRole")
            if role == "import":
                self.e_target_choice.setEnabled(False)
                self.import_button.setEnabled(False)
                self.import_task(preview=False)

    def import_task(self, preview=True):
        importer = ImageImporter(
            source_dir=self.dir_from,
            target_dir=self.dir_to,
        )
        if preview is True:
            importer.dry_run()
        else:
            importer.run()
        importer.waitForFinished()
        stdout = importer.readAllStandardOutput().data().decode('utf8')
        if preview is True:
            self.exiftool_preview.setText(stdout)
        else:
            self.exiftool_import.setText(stdout)
