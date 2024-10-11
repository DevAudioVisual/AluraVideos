from PyQt6.QtWidgets import QVBoxLayout, QTabWidget,QMenu
from Config import LoadConfigs
from Models.Vimeo import VimeoUploader
from QtInterfaces.ImagensPixaBay import ImagensPixabay
from QtInterfaces.LimparCache import InterfaceLimparCache
from QtInterfaces.ProjectCreator import InterfaceProjectCreator
from QtInterfaces.Renamer import InterfaceRenamer
from QtInterfaces.S3 import InterfaceS3
from PyQt6.QtGui import QAction

class Tabs(QTabWidget):
    def __init__(self):  # Passar a instância de MenuBar
        super().__init__()