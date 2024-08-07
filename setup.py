from cx_Freeze import Executable, setup
import sys

base = "Win32GUI" if sys.platform == "win32" else None

additionalFiles = [
    "shell.py",
    "settings.json",
    "ast.json",
    "themes",
    "snippets",
    "modules",
    "frontend",
    "backend",
    "ExamplePrograms",
    "phi.ico"
]

exe = Executable(
    script="phIDE.py",
    base=base,
    icon="phi.ico"
)

setup(
    name="phIDE",
    version="1.8.0",
    description="phi IDE",
    executables=[exe],
    options={
        "build_exe":{
            "include_files":additionalFiles
        }
    }
)
