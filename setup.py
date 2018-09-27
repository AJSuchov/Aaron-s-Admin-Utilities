import cx_Freeze
import sys
import os

os.environ['TCL_LIBRARY'] = r'C:\Python36-64\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python36-64\tcl\tk8.6'


base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("Utilities GUI.py", base=base,icon='A.ico')] #add icon later with ,icon='something.ico'

cx_Freeze.setup(
    name = "Aaron's Admin Utilities",
    options = {"build_exe":{"packages":["tkinter"],
                            "include_files":["A.ico","C:/Python36-64/DLLs/tcl86t.dll","C:/Python36-64/DLLs/tk86t.dll"]}},
    version = "0.5",
    description = "Aaron's Admin Utilities",
    executables = executables

    )


