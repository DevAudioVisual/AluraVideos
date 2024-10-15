from PyQt6.QtWidgets import QLabel, QVBoxLayout, QLineEdit, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from QtInterfaces.Interfaces.Preferencias import Tabs

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        #self.setWindowTitle("Configurações")
        
        self.setContentsMargins(10, 20, 10, 10)
        
        titulo = QLabel("Preferências de usuário")
        titulo.setObjectName("grande")
        
        pesquisar = QLineEdit()
        pesquisar.setPlaceholderText("Pesquisar (EM BREVE)")
        pesquisar.addAction(QIcon("Assets\Icons\search.ico"),QLineEdit.ActionPosition.TrailingPosition)
        pesquisar.setClearButtonEnabled(True)
        
        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addWidget(pesquisar)
        layout.addWidget(Tabs.Tabs())
        
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.setContentsMargins(10, 0, 10, 10)
        
        self.setLayout(layout)
