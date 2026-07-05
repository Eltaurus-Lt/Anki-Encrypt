# This script is part of the Encrypt Add-on for Anki.
# Source: https://github.com/Eltaurus-Lt/Anki-Encrypt
# 
# Copyright © 2026 Eltaurus
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


from aqt import mw
from anki import stdmodels
from anki.models import ModelManager
from aqt.utils import tr, getText

import os

addons_folder = mw.addonManager.addonsFolder()
addon_name = mw.addonManager.addonFromModule(__name__)

def load(file_path):
    full_path = os.path.join(addons_folder, addon_name, os.path.normpath(file_path))
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as file:
            return file.read()

def insertJS(script_name):
    return (
            '\n'
            '\n'
            '<script>\n'
            f'{load("Note Types/scripts/"+script_name+".js")}\n'
            '</script>'
           )

def encrypt_note_type(col):

    noteTypeName, ok = getText(tr.actions_name(), default = "Encrypt (Lτ)")

    if not ok:
        return col.models.current()

    mm = col.models
    noteType = mm.new(noteTypeName)

    # Fields
    mm.addField(noteType, mm.newField("Account"))
    mm.addField(noteType, mm.newField("Password (Encrypted)"))
    mm.addField(noteType, mm.newField("hint"))

    # Card Type
    cardType = mm.newTemplate("Password test")
    cardType["qfmt"] = (
                        '<div class="acc">\n'
                        '  {{Account}}\n'
                        '</div>\n'
                        '\n'
                        '<div class="hint">{{hint}}</div>\n'
                        '\n'
                        '{{type:Password (Encrypted)}}\n'
                        '\n'
                        '<script>\n'
                        '  document.getElementById("typeans").setAttribute("type","password")\n'
                        '</script>'
                       )
    cardType["afmt"] = (
                        '<div class="hide-answer">\n'
                        '  {{FrontSide}}\n'
                        '</div>\n'
                        f'{insertJS("CheckAnswer")}'
                       )
    noteType["css"] = (f'{load("Note Types/Encrypt.css")}')
    mm.addTemplate(noteType, cardType)

    # Add to the collection
    mm.add(noteType)
    mm.save(noteType)

    return noteType


# monkey-patch to the note manager
orig_get_stock_notetypes = stdmodels.get_stock_notetypes

def patched_get_stock_notetypes(*args, **kwargs):
    models = orig_get_stock_notetypes(*args, **kwargs)
    model_names = [model[0] for model in models]
    encrypt_index = model_names.index('Basic (Lτ)')+1 if "Basic (Lτ)" in model_names else 4
    models.insert(encrypt_index, ("Encrypt (Lτ)", encrypt_note_type))
    return models

stdmodels.get_stock_notetypes = patched_get_stock_notetypes