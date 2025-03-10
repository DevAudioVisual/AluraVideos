import os
import threading
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QCursor
import requests
from packaging import version
import yaml
from Models.ExtensoesPPRO.GithubDownloader import GithubDownloader
from Models.ExtensoesPPRO.GithubUpdater import GithubUpdater
from Interfaces.MainWindow.LoadingScreen import LoadingScreen
from Util import Tokens, Util
import Util.CustomWidgets as cw

class Interface(cw.Widget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Extensões PPRO")
        
        main_layout = cw.VBoxLayout()
        main_layout.setContentsMargins(10, 20, 10, 10)  # Defina as margens desejadas
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        
        layout = cw.GridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.setContentsMargins(10, 20, 10, 10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        
        if not os.path.isdir(r"C:\Program Files (x86)\Common Files\Adobe\CEP\extensions"):
            label = cw.Label("<font color='red'>Adobe Premiere Pro não encontrado.</font>")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
            label.setObjectName("grande")
            main_layout.addWidget(label)
            self.setLayout(main_layout)
        else:
            label = cw.Label("Faça download das extensões para o Adobe Premiere pro aqui.")
            label.setObjectName("grande")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
            
            global versao_effector,versao_ordinem,versao_notabillity
            

            botao_effector = cw.PushButton(f"{LoadingScreen.versao_effector}")
            botao_ordinem = cw.PushButton(f"{LoadingScreen.versao_ordinem}")
            botao_notabillity = cw.PushButton(f"{LoadingScreen.versao_notabillity}")
            
            botao_effector.setIcon(QIcon(r"Assets\svg\download.svg"))
            botao_ordinem.setIcon(QIcon(r"Assets\svg\download.svg"))
            botao_notabillity.setIcon(QIcon(r"Assets\svg\download.svg"))
            
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
            spacer = cw.SpacerItem(20, 40, cw.SizePolicy.Policy.Minimum, cw.SizePolicy.Policy.Expanding)
            main_layout.addItem(spacer)
            
            # Footer layout
            layoutFooter = cw.VBoxLayout()
            layoutFooter.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
            layoutFooter.setContentsMargins(10, 20, 10, 10)
            
            label_footer = cw.Label("Criadas por Denis Santos para o time de Vídeos da Alura Online.")
            label_footer.setWordWrap(False)
            label_footer.setObjectName("pequeno-normal")
            
            # Add footer label to the footer layout
            layoutFooter.addWidget(label_footer)
            
            # Add footer layout to the main layout at the bottom
            main_layout.addLayout(layoutFooter)
            
            self.setLayout(main_layout)
            
            def updateNames():
                if Tokens.AWS_S3 == None: return
                notas_effector, version_effector = GitRequest("Effector").initRequest()
                notas_ordinem, version_ordinem = GitRequest("Ordinem").initRequest()
                notas_notabillity, version_notabillity = GitRequest("Notability").initRequest()
                
                botao_effector.setText(f"Download Effector V{version_effector}")
                botao_ordinem.setText(f"Download Ordinem V{version_ordinem}")
                botao_notabillity.setText(f"Download Notability V{version_notabillity}")

                versao_atual_ordinem = versaoAtual(r"C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\Ordinem\version.yml")
                versao_atual_effector = versaoAtual(r"C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\Effector\version.yml")
                versao_atual_notability = versaoAtual(r"C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\Notability\version.yml")
                updater = GithubUpdater(versao_atual_ordinem,versao_atual_effector,versao_atual_notability).verificar_atualizacoes()
                
                if updater:
                    for repo, versao in updater.items():
                        if repo == "Effector":
                            if versao_atual_effector != 0:
                                botao_effector.setText(f"Atualizar Effector V{versao}")

                        if repo == "Ordinem": 
                            if versao_atual_ordinem != 0:
                                botao_ordinem.setText(f"Atualizar Ordinem V{versao}")
    
                        if repo == "Notability":      
                            if versao_atual_notability != 0:                 
                                botao_notabillity.setText(f"Atualizar Notability V{versao}")
                            
                        
            threading.Thread(target=updateNames,daemon=True).start()


class GitRequest():
    def __init__(self,repo_name):
        self.repo_owner = "DevAudioVisual"
        self.repo_name = repo_name
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        self.headers = {"Authorization": f"Bearer {Tokens.GITHUB}","Accept": "application/vnd.github+json"}
        
    def initRequest(self):
        try:
            response = requests.get(self.api_url, headers=self.headers)
            response.raise_for_status()
            release_data = response.json()
            latest_tag_name = release_data["tag_name"]
            release_notes = release_data["body"]
            release_version = version.parse(latest_tag_name.lstrip("V"))
            return release_notes, release_version
        except requests.exceptions.RequestException as e:
            Util.LogError(func="PPRO", mensagem=f"Erro na requisição extensão ppro: {self.repo_name} {e}",dialog=False)
            return "Erro", "Erro"

def versaoAtual(arquivo):
    try:
        with open(arquivo, 'r') as f:
            dados = yaml.safe_load(f)
            return dados["Version"]
    except FileNotFoundError:
        return 0