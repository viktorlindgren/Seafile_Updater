from distutils.core import setup
import py2exe,os
import sys

name = "Seafile Updater"
pathsrc = ".." + os.sep + "src" + os.sep
sys.path.insert(0, pathsrc)

main = pathsrc + "Check4SeafileUpdate.py"

setup(
	name = name,
	windows = [main])
