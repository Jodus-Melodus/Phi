from cx_Freeze import Executable, setup
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

additionalFiles = [
    'syntax.json',
    'snippets',
    'shell.py',
    'settings.json',
    'phi-theme.json'
]

exe = Executable(
    script="phIDE.py",
    base=base,
    icon="phi.ico"
)

setup(
    name='phIDE',
    version='1.2.0',
    description='phi IDE',
    executables=[exe],
    options={
        'build_exe':{
            'include_files':additionalFiles
        }
    }
)