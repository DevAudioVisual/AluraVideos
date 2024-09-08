import os
import sys
from cx_Freeze import setup, Executable
import Util.Util as Util
# qt_platforms_path = os.path.join(os.environ['VIRTUAL_ENV'], 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins', 'platforms')
build_exe_options = {
    "packages": ["os", "shutil", "tkinter", "patoolib", "numpy", "pandas", "pystray", "PyQt6", "requests", "six", "setuptools"],
    "include_files": ["ffmpeg", "Templates", "Assets"],
    "include_msvcr": True,
    "includes": ["PyQt6.sip"],
    "bin_includes": ["msvcp140.dll", "tbb12.dll"],
    "bin_path_includes": ["C:\\Windows\\System32","C:\\Windows\\SysWOW64", "C:\\Arquivos de Programas\\Intel\\TBB\\bin","C:\\Program Files (x86)\\Intel\\oneAPI\\tbb\\2021.13\\bin"]
}


# Adiciona a opção de base "Win32GUI" para esconder a janela de console no Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Adiciona o ícone ao executável
executables = [
    Executable(
        "Main.py",
        base=base,
        icon=r"Assets\Images\icon.ico",
        target_name="AluraVideos"
    )
]

setup(
    name="AluraVideos",
    version=Util.version,
    description="Software oficial time Videos", 
    options={"build_exe": build_exe_options},
    executables=executables,
)
