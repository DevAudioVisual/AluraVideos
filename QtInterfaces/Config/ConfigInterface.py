from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QTabWidget, QToolBar, QWidget, QPushButton
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from QtInterfaces.ProjectCreator import InterfaceProjectCreator
from Util import Util

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configurações")
