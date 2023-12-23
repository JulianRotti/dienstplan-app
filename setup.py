from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but some might need fine-tuning
build_exe_options = {"packages": ["os", "pandas", "kivy"], "excludes": ["tkinter"]}

# Base=None means the application is not a console application
base = None

setup(
    name = "Matzes ShiftMaster",
    version = "0.1",
    description = "Create a shift plan",
    options = {"build_exe": build_exe_options},
    executables = [Executable("app.py", base=base)]
)
