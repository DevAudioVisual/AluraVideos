from PyQt6.QtWidgets import QTabWidget
from QtInterfaces.Interfaces.Renamer import InterfaceRenamerSheets, InterfaceRenamerVideos

class Tabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setMovable(True)
        self.setTabsClosable(False)

        self.setContentsMargins(10, 10, 10, 10)

        self.addTab(InterfaceRenamerSheets.Interface(),"Renomear por Sheets")
        self.addTab(InterfaceRenamerVideos.Interface(),"Renomear por Referência")
            
   