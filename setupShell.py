from cx_Freeze import Executable, setup

options = {
    'build_exe': {
        'build_exe': 'Shell',
    },
}

exe = Executable(
    script="shell.py",
    icon="phi.ico"
)

setup(
    name='phiShell',
    version='1.4.0',
    description='phi shell',
    executables=[exe],
    options=options
)