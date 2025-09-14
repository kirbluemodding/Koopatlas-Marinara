#!/usr/bin/env python2

# Koopatlas Marinara Edition
# A project by Treeki and Tempus
# Based off of Koopatlas Updated by RoadrunnerWMC
# Further upgraded by Kirblue with support from friends
# Started September 12th 2025

import os, os.path, sys


def module_path():
    """
    This will get us the program's directory, even if we are frozen
    using PyInstaller
    """

    if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):  # PyInstaller
        if sys.platform == 'darwin':  # macOS
            # sys.executable is /x/y/z/reggie.app/Contents/MacOS/reggie
            # We need to return /x/y/z/reggie.app/Contents/Resources/

            macos = os.path.dirname(sys.executable)
            if os.path.basename(macos) != 'MacOS':
                return None

            return os.path.join(os.path.dirname(macos), 'Resources')

        else:  # Windows, Linux
            return os.path.dirname(sys.executable)

    if __name__ == '__main__':
        return os.path.dirname(os.path.abspath(__file__))

    return None


path = module_path()
if path is not None:
    os.chdir(path)


if hasattr(sys, 'frozen'):
    sys.path.append(os.path.join(os.path.dirname(sys.executable), 'src'))
else:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))



from common import *

if __name__ == '__main__':
    KP.run()

