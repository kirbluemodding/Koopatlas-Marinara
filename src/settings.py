import configparser
import os
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

settings_default = """
[Window]
grid_type = 0
background = False
backgroundType = water_lava_view

[File]
LastMapOpen =
OpenLastMap = True

[Meta]
Version = v1a
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

#settings._insure() <- this is worthless as it is already called in main


class KPSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.resize(300, 200)
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle("Settings - Koopatlas Marinara Edition")
        self.setWindowIcon(QIcon('Resources/Icon/Settings.png')) 
        self.resize(500, 350)
        self.setLayout(self.main_layout)

        # create a tab widget
        self.tab = QTabWidget()

        self.loadViewPage()
        self.loadGeneralPage()

        # add pane to the tab widget
        self.tab.addTab(self.general_page, "General")
        self.tab.addTab(self.view_page, "View")
        
        # this is a mess but it's SO MINOR i don't care
        self.main_layout.addWidget(self.tab, 0, 0, 2, 1)
        self.saveButton = QPushButton('Apply')
        self.closeButton = QPushButton('Save and close')
        self.closeButton.clicked.connect(self.cancel)
        self.saveButton.clicked.connect(self.apply)
        self.main_layout.addWidget(self.closeButton, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(self.saveButton, 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)

    def apply(self):
        with open("settings.ini", "w") as f:
            settings.config.write(f)

    def cancel(self, close):
        self.apply()
        self.close()

    def loadGeneralPage(self):

        # Buttons and other crap
        def loadLast():
            if settings.config["File"]["OpenLastMap"] == "True":
                settings.config["File"]["OpenLastMap"] = "False"
            else:
                settings.config["File"]["OpenLastMap"] = "True"

        def clearRecent():
            QMessageBox.information(self, "Not quite...", "This feature is planned for a later release, and so is this setting.")
        
        # general page widget
        self.general_page = QWidget()
        # layout.
        self.general_layout = QVBoxLayout()
        self.general_page.setLayout(self.general_layout)
        # elements (these are just groupboxes)
        # can't be assed to make and run a function for these

        ####################
        # start up groupbox
        ####################
        self.start_up = QGroupBox("Start-up")
        # layout
        self.start_up_layout = QFormLayout()
        self.start_up.setLayout(self.start_up_layout)

        self.loadLast = QCheckBox()
        if settings.config["File"]["OpenLastMap"] == "True":
            self.loadLast.setChecked(True)
        self.loadLast.clicked.connect(loadLast)
        self.start_up_layout.addRow("Load last map open?", self.loadLast)

        self.SUPERTIPS = QCheckBox()
        self.start_up_layout.addRow("Enable tip-of-the-day?", self.SUPERTIPS)
        # no new func. Just call the same one.
        self.SUPERTIPS.clicked.connect(clearRecent)
        self.SUPERTIPS.setCheckable(False)

        # add this!
        self.general_layout.addWidget(self.start_up)

        #########################
        # miscellaneous groupbox
        #########################
        self.miscellaneous = QGroupBox("Miscellaneous")
        # layout
        self.miscellaneous_layout = QFormLayout()
        self.miscellaneous.setLayout(self.miscellaneous_layout)

        self.clearRecent = QPushButton("Clear recent maps")
        self.clearRecent.clicked.connect(clearRecent)
        self.miscellaneous_layout.addRow(self.clearRecent)

        # add this!
        self.general_layout.addWidget(self.miscellaneous)

    def loadViewPage(self):
        
        self.view_page = QWidget()
        self.view_layout = QVBoxLayout()
        self.view_page.setLayout(self.view_layout)

        ##################
        # canvas groupbox
        ##################
        self.canvas = QGroupBox("Map canvas")
        self.canvas_layout = QHBoxLayout()
        self.canvas.setLayout(self.canvas_layout)


        self.bgWaterLavaViewRadio = QRadioButton("Dynamic")
        self.bgOffRadio = QRadioButton("No")
        self.bgCustomRadio = QRadioButton("Custom")
        self.bgLabel = QLabel("Background Color:")
        # one logic thing because it's one option to be clicked JAJA
        if settings.config["Window"]["background"] == "False":
            self.bgOffRadio.setChecked(True)
        elif settings.config["Window"]["background"] == "water_lava_view":
            self.bgWaterLavaViewRadio.setChecked(True)
        elif settings.config["Window"]["background"] == "custom":
            self.bgCustomRadio.setChecked(True)

        self.canvas_layout.addWidget(self.bgLabel)
        self.canvas_layout.addWidget(self.bgOffRadio)
        self.canvas_layout.addWidget(self.bgWaterLavaViewRadio)
        self.canvas_layout.addWidget(self.bgCustomRadio)

        # add this!
        self.view_layout.addWidget(self.canvas)