import configparser
import os
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

settings_default = """
[Window]
grid_type = 0
water_lava_view = False

[File]
LastMapOpen =
OpenLastMap =
"""

class settings:
    config = configparser.ConfigParser()

    @staticmethod
    def _insure():
        if os.path.isfile("settings.ini"):
            print("Loading settings file")
        else:
            with open("settings.ini", "w") as f:
                f.write(settings_default)
            print("The settings file seems to be missing. Making a new one...")

        settings.config.read('settings.ini')

    @staticmethod
    def _onexit():
        with open("settings.ini", "w") as f:
            settings.config.write(f)

#settings._insure()


class KPSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings - Koopatlas Marinara Edition")
        self.setWindowIcon(QIcon('Resources/Icon/Settings.png')) 
        self.resize(500, 350)
        main_layout = QGridLayout(self)
        self.setLayout(main_layout)

        # create a tab widget
        tab = QTabWidget(self)

        general_page = QWidget(self)
        general_layout = QFormLayout()
        general_page.setLayout(general_layout)
        general_layout.addRow("Load last map open", QCheckBox(self))

        appearence_page = QWidget(self)
        appearence_layout = QFormLayout()
        appearence_page.setLayout(appearence_layout)
        appearence_layout.addRow("Grid Type", QComboBox(self))
        appearence_layout.addRow("Show Wii Zoom", QCheckBox(self))
        appearence_layout.addRow("Water/Lava Colors", QCheckBox(self))

        # add pane to the tab widget
        tab.addTab(general_page, "General")
        tab.addTab(appearence_page, "Appearence")

        main_layout.addWidget(tab, 0, 0, 2, 1)
        main_layout.addWidget(QPushButton('Save'), 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(QPushButton('Cancel'), 2, 0, alignment=Qt.AlignmentFlag.AlignRight)