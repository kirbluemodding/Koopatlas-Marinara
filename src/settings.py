import configparser
import os

# this fuckin hack.
error_missing = """
--------------------------------
------ Koopatlas Marinara ------
--------------------------------

Error: Missing config file!
Don't fret; this is normal and only happens on your first time using the program or when you delete "koopatlas.ini".
This is automatically fixed.
--------------------------------
Please run windows_run.bat again. This should only happen once, otherwise report as a bug: https://github.com/kirbluemodding/Koopatlas-Marinara/issues
"""

# more than likely a way to generate this.
preferances_default = """
[Window]
grid_type = 0

[Jaja]
WHAT = null
"""
class settings:
    config = configparser.ConfigParser()
    config.read('koopatlas.ini')

    def _insure():
        if os.path.isfile("koopatlas.ini"):
            print("Config file found, loading")
        else:
            f = open("koopatlas.ini", "x")
            f.write(preferances_default)
            raise Exception(error_missing)

    def _onexit():
        with open("koopatlas.ini", "w") as f:
            settings.config.write(f)


