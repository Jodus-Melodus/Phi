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

exe = Executable(
    script="phIDE.py",
    base=base,
    icon="phi.ico"
)

setup(
    name='phIDE',
    version='1.3.1',
    description='phi IDE',
    executables=[exe],
    options={
        'build_exe':{
            'include_files':additionalFiles
        }
    }
)