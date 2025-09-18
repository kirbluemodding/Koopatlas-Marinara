import configparser
import os

settings_default = """
[Window]
grid_type = 0
water_lava_view =

[File]
LastMapOpen =
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

settings._insure()
