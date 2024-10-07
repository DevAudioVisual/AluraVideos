from PyQt6.QtWidgets import QSpacerItem, QVBoxLayout, QLayout, QWidget, QGridLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QCursor

from Models.ExtensoesPPRO.GithubDownloader import GithubDownloader

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Extensões PPRO")
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 20, 10, 10)  # Defina as margens desejadas
        
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.setContentsMargins(10, 20, 10, 10)
        
        label = QLabel("Faça download das extensões para o Adobe Premiere pro aqui.")
        label.setObjectName("grande")
        
        label_effector = QLabel("Descrição effector")
        label_effector.setObjectName("medio")
        botao_effector = QPushButton("Download Effector  ")
        botao_effector.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        label_ordinem = QLabel("Descrição effector")
        label_ordinem.setObjectName("medio")
        botao_ordinem = QPushButton("Download Ordinem  ")
        botao_ordinem.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        label_notabillity = QLabel("Descrição effector")
        label_notabillity.setObjectName("medio")
        botao_notabillity = QPushButton("Download Notabillity  ")
        botao_notabillity.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        botao_effector.setIcon(QIcon(r"Assets\Icons\download.ico"))
        botao_ordinem.setIcon(QIcon(r"Assets\Icons\download.ico"))
        botao_notabillity.setIcon(QIcon(r"Assets\Icons\download.ico"))
        
        botao_effector.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        botao_ordinem.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        botao_notabillity.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        download_path = r"C:\Program Files (x86)\Common Files\Adobe\CEP\extensions"
        botao_effector.clicked.connect(lambda: GithubDownloader("DevAudioVisual","Effector").download_sourcecode(download_path))
        botao_ordinem.clicked.connect(lambda: GithubDownloader("DevAudioVisual","Ordinem").download_sourcecode(download_path))
        botao_notabillity.clicked.connect(lambda: GithubDownloader("DevAudioVisual","Notability").download_sourcecode(download_path))
        
        layout.addWidget(label, 0, 0)
        #layout.addWidget(label_effector, 1, 0)
        layout.addWidget(botao_effector, 2, 0)
        #layout.addWidget(label_ordinem, 3, 0)
        layout.addWidget(botao_ordinem, 4, 0)
        #layout.addWidget(label_notabillity, 5, 0)
        layout.addWidget(botao_notabillity, 6, 0)
        
        main_layout.addLayout(layout)

        # Spacer to push footer to the bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer)
        
        # Footer layout
        layoutFooter = QVBoxLayout()
        layoutFooter.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        layoutFooter.setContentsMargins(10, 20, 10, 10)
        
        label_footer = QLabel("Criadas por Denis Santos para o time de Vídeos da Alura Online.")
        label_footer.setObjectName("pequeno")
        
        # Add footer label to the footer layout
        layoutFooter.addWidget(label_footer)
        
        # Add footer layout to the main layout at the bottom
        main_layout.addLayout(layoutFooter)
        
        self.setLayout(main_layout)
