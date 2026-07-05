# This script is part of the Encrypt Add-on for Anki.
# Source: https://github.com/Eltaurus-Lt/Anki-Encrypt
# 
# Copyright © 2025-2026 Eltaurus
# Contact: 
#     Email: Eltaurus@inbox.lt
#     GitHub: github.com/Eltaurus-Lt
#     Anki Forums: forums.ankiweb.net/u/Eltaurus
#     about: https://eltaurus-lt.github.io/about/me.html
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
from anki.hooks import addHook
from aqt import dialogs, mw, gui_hooks
from aqt.utils import tooltip
from aqt.qt import *
import hashlib
from . import Manage_Note_Types

addon_path = os.path.dirname(__file__)

class EncryptDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter string to encrypt")

        layout = QVBoxLayout()

        self.password_input = QLineEdit("")
        layout.addWidget(self.password_input)

        font_metrics = QFontMetrics(self.password_input.font())
        line_height = font_metrics.lineSpacing()
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.button_ok = QPushButton("OK")
        button_layout.addWidget(self.button_ok)
        self.button_ok.clicked.connect(self.accept)

        self.button_cancel = QPushButton("Cancel")
        button_layout.addWidget(self.button_cancel)
        self.button_cancel.clicked.connect(self.reject)        

        layout.addLayout(button_layout)

        # Set size limits
        self.setMinimumWidth(15 * line_height)
        self.setMaximumHeight(2 * line_height)

        # Set layout
        self.setLayout(layout)

    def get_password(self):
        return self.password_input.text()

def Encrypt(editor):
    note = editor.note
    field = note.keys()[editor.currentField]

    dialog = EncryptDialog()
    if not dialog.exec():
        return
    
    password = dialog.get_password()
    salt = os.urandom(16)
    hashstring = hashlib.sha256(salt + password.encode('utf-8')).hexdigest()

    note[field] = salt.hex() + hashstring
    # if note.id != 0:
    #     mw.col.update_note(note)
    editor.loadNoteKeepingFocus()


def setupEditorButtonsFilter(buttons, editor):

    buttons.insert(0,
        editor.addButton(
            icon=os.path.join(addon_path, "encrypt.svg"),
            cmd='Encrypt',
            func=Encrypt,
            tip="Insert an encrypted string"
        )
    )

    return buttons


# gui_hooks.editor_did_init_buttons.append(setupEditorButtonsFilter)
addHook("setupEditorButtons", setupEditorButtonsFilter)
