from PyQt6.QtWidgets import QVBoxLayout, QTabWidget,QMenu
from QtInterfaces.ImagensPixaBay import ImagensPixabay
from QtInterfaces.LimparCache import InterfaceLimparCache
from QtInterfaces.Preferencias import InterfacePreferenciasProjectCreator
from QtInterfaces.ProjectCreator import InterfaceProjectCreator
from QtInterfaces.S3 import InterfaceS3
from PyQt6.QtGui import QAction

class Tabs(QTabWidget):
    def __init__(self):  # Passar a instância de MenuBar
        super().__init__()

        self.InterfaceProjectCreator = InterfaceProjectCreator.Interface()
        
        self.setContentsMargins(10, 20, 10, 10)
        
        abas = {
            "Preferências Criar Projeto": InterfacePreferenciasProjectCreator.Interface(),
            #"Preferências S3": InterfaceS3.Interface(),
            #"Preferências PM3": None,  # Se PM3 não tem um módulo associado
            #"Preferências Imagens Pixabay": ImagensPixabay.Interface(),
            #"Preferências Limpar Cache": InterfaceLimparCache.Interface()
        }
        for nome_aba, modulo in abas.items():
            self.addTab(modulo,nome_aba)
            
        layout = QVBoxLayout()
        layout.addWidget(self)
