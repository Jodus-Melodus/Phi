from cx_Freeze import Executable, setup

exe = Executable(
    script="shell.py",
    icon="phi.ico"
)

setup(
    name='phiShell',
    version='1.3.0',
    description='phi shell',
    executables=[exe],
)