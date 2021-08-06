
import sys
from cx_Freeze import setup, Executable
setup(  name = "Bumblebee",
        version = "9.1",
        description = "Double click to open the file ",
        author = "https://indybytes.com/",
        executables = [Executable("Bumblebee.py")])