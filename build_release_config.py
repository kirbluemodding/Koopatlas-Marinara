import os.path

# Everything highly specific to Koopatlas is in this file, to make it
# simpler to copypaste the build_release script across all of the
# NSMBW-related projects that use the same technologies (Reggie, Puzzle,
# BRFNTify, etc)

PROJECT_NAME = 'Koopatlas Marinara'
FULL_PROJECT_NAME = "Koopatlas Marinara - Newer's Fantastic World Map Editor"
PROJECT_VERSION = '1.0'

WIN_ICON = os.path.join('Resources', 'Koopatlas.ico')
MAC_ICON = os.path.join('Resources', 'Koopatlas.icns')
MAC_BUNDLE_IDENTIFIER = 'com.realismstudios.koopatlas-marinara'

SCRIPT_FILE = 'koopatlas.py'
DATA_FOLDERS = ['Resources', 'Tilesets']
DATA_FILES = ['readme.md', 'LICENSE']
EXTRA_IMPORT_PATHS = ['src']

USE_PYQT = True
USE_NSMBLIB = False

EXCLUDE_HASHLIB = False

# macOS only
AUTO_APP_BUNDLE_NAME = SCRIPT_FILE.split('.')[0] + '.app'
FINAL_APP_BUNDLE_NAME = FULL_PROJECT_NAME + '.app'
