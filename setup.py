from cx_Freeze import Executable, setup
import sys

base = "Win32GUI" if sys.platform == "win32" else None
additionalFiles = [
    "shell.py",
    "ast.json",
    "frontend",
    "backend",
    "snippets",
    "themes",
    "modules",
    "examplePrograms"
]

exe = Executable(
    script="phIDE.py",
    base=base,
    icon="phi.ico"
)

setup(
    name="phIDE",
    version="1.1.2",
    description="phi IDE",
    executables=[exe],
    options={
        "build_exe":{
            "include_files":additionalFiles
        }
    }
)