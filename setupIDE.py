from cx_Freeze import Executable, setup
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

additionalFiles = [
    'frontend',
    'backend',
    'Modules',
    'snippets',
    'Themes',
    'ExamplePrograms',
    'settings.json',
    'shell.py',
    'phi.ico'
]

options = {
    'build_exe': {
        'include_files':additionalFiles,
        'build_exe': 'phIDE'
    }
}

exe = Executable(
    script="phIDE.py",
    base=base,
    icon="phi.ico"
)

setup(
    name='phIDE',
    version='1.4.0',
    description='phi IDE',
    executables=[exe],
    options=options
)