from cx_Freeze import Executable, setup


additionalFiles = [
    'syntax.json',
    'main.py',
    'ast.json',
    'frontend',
    'backend',
    'snippets'
]

setup(
    name='phIDE',
    version='1.1.0',
    description='phi IDE',
    executables=[Executable('phIDE.py')],
    options={
        'build_exe':{
            'include_files':additionalFiles
        }
    }
)