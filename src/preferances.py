import configparser
import os
# more than likely a way to generate this.
preferances_default = """
[Window]
grid_type = none

"""
class preferances:
    def _load():
        if os.path.exists("koopatlas.ini"):
            print("Config file exists. Opening.")
            config = configparser.ConfigParser()
            config.read('koopatlas.ini')
            #config["Preferences"]["test"] = "Jaja"

            with open("koopatlas.ini", "w") as f:
                config.write(f)
        else:
            print("Preferences file does not exist. Creating a new one")
            prefFile = open("koopatlas.ini", "x")
            prefFile.write(preferances_default)
