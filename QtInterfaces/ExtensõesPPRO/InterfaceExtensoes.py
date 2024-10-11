import threading
from PyQt6.QtWidgets import QSpacerItem, QVBoxLayout, QLayout, QWidget, QGridLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QIcon, QCursor
import requests
from packaging import version
from Models.ExtensoesPPRO.GithubDownloader import GithubDownloader
from QtInterfaces.LoadingScreen import LoadingScreen
from Util import Util

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
        
        global versao_effector,versao_ordinem,versao_notabillity
        
        label_effector = QLabel("Descrição effector")
        label_effector.setObjectName("medio")
        botao_effector = QPushButton(f"{LoadingScreen.versao_effector}")
        botao_effector.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        label_ordinem = QLabel("Descrição effector")
        label_ordinem.setObjectName("medio")
        botao_ordinem = QPushButton(f"{LoadingScreen.versao_ordinem}")
        botao_ordinem.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        label_notabillity = QLabel("Descrição effector")
        label_notabillity.setObjectName("medio")
        botao_notabillity = QPushButton(f"{LoadingScreen.versao_notabillity}")
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
        label_footer.setObjectName("pequeno-normal")
        
        # Add footer label to the footer layout
        layoutFooter.addWidget(label_footer)
        
        # Add footer layout to the main layout at the bottom
        main_layout.addLayout(layoutFooter)
        
        self.setLayout(main_layout)
        
        def updateNames():
            botao_effector.setText(f"Download Effector {GitRequest("Effector").initRequest()}")
            botao_ordinem.setText(f"Download Ordinem {GitRequest("Ordinem").initRequest()}")
            botao_notabillity.setText(f"Download Notability {GitRequest("Notability").initRequest()}")
 
        threading.Thread(target=updateNames,daemon=True).start()


class GitRequest():
    def __init__(self,repo_name):
        self.repo_owner = "DevAudioVisual"
        self.repo_name = repo_name
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        self.headers = {"Accept": "application/vnd.github+json"}
        
    def initRequest(self):
        try:
            response = requests.get(self.api_url, headers=self.headers)
            response.raise_for_status()
            release_data = response.json()
            latest_tag_name = release_data["tag_name"]
            release_notes = release_data["body"]
            release_version = version.parse(latest_tag_name.lstrip("V"))
            return release_version
        except requests.exceptions.RequestException as e:
            Util.LogError(func="PPRO", mensagem=f"Erro na requisição extensão ppro: {self.repo_name} {e}")
            return "Erro"