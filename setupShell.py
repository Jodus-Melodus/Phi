from cx_Freeze import Executable, setup
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = Executable(
    script="shell.py",
    base=base,
    icon="phi.ico"
)

setup(
    name='phiShell',
    description='phi shell',
    executables=[exe],
)