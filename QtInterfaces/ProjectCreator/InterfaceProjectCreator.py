import re
import threading
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QCheckBox,QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QCursor
from bs4 import BeautifulSoup
from unidecode import unidecode
import requests
from Config import LoadConfigs
from Models.CriarProjeto import CriarProjeto
from QtInterfaces.MainWindow import MainWindow
global Config

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        
        df = LoadConfigs.Config.getDataFrame("ConfigCriarProjeto")
        config = LoadConfigs.Config.getConfigData("ConfigCriarProjeto")
        
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.setContentsMargins(10, 20, 10, 10)

        label_nome = QLabel("Nome do projeto:")
        label_nome.setObjectName("medio")
        self.campo_nome = QLineEdit()
        self.campo_nome.setText("00_Novo Projeto")
        
        label_dir = QLabel("Diretório do projeto:")
        label_dir.setObjectName("medio")
        self.campo_dir = QLineEdit()
        self.campo_dir.setText(config["diretorio_padrao"])
        BotaoDir = QPushButton("Buscar  ")
        BotaoDir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        BotaoDir.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        BotaoDir.setIcon(QIcon(r"Assets\Images\folder.png"))
        def open_folder_dialog():
            file_name = QFileDialog.getExistingDirectory(self, "Selecione uma pasta")
            if file_name:
                print(f"Pasta selecionado: {file_name}")
                self.campo_dir.setText(rf"{file_name}")
        BotaoDir.clicked.connect(open_folder_dialog)
        
        label_videos = QLabel("Arquivo de vídeos (Arquivo ZIP ou URL)")
        label_videos.setObjectName("medio")
        self.campo_videos = QLineEdit()
        BotaoVideos = QPushButton("Buscar  ")
        BotaoVideos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        BotaoVideos.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        BotaoVideos.setIcon(QIcon(r"Assets\Images\folder.png"))
        def open_file_dialog_videos():
            file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo", "", "Todos os Arquivos (*)")
            if file_name:
                print(f"Arquivo selecionado: {file_name}")
                self.campo_videos.setText(rf"{file_name}")
        BotaoVideos.clicked.connect(open_file_dialog_videos)
        BotaoVideosDrop = QPushButton("Buscar Nome  ")
        BotaoVideosDrop.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        BotaoVideosDrop.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        BotaoVideosDrop.setIcon(QIcon(r"Assets\Images\dropbox.ico"))
        def setNomeProjeto():
            if not self.campo_videos.text().startswith("https://www.dropbox.com"):
                QMessageBox.warning(None, "Aviso", "Link dropbox inválido ou inexistente.")
                return
            def buscar():
                self.campo_nome.setText("Buscando...")
                self.BotaoCriar.setText("Aguarde...")
                self.BotaoCriar.setEnabled(False)
                self.setCursor(Qt.CursorShape.WaitCursor)
                nome = obter_nome_pasta(self.campo_videos.text())
                self.campo_nome.setText(limpar_texto(nome))
                self.BotaoCriar.setText("Criar")
                self.BotaoCriar.setEnabled(True)
                self.setCursor(Qt.CursorShape.ArrowCursor)
            threading.Thread(target=buscar,daemon=True).start()
        BotaoVideosDrop.clicked.connect(setNomeProjeto)
        
        checks_vars = {}
        checks = df['checks'].iloc[0].items()
        for ch, ci in checks:
            checks_vars[ch] = ci
        
        self.check_AbrirPremiere = QCheckBox("Abrir Premiere ao finalizar")
        self.check_AbrirPremiere.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.check_AbrirPremiere.setChecked(bool(checks_vars["Abrir_Premiere"]))
        
        self.check_AbrirPasta = QCheckBox("Abrir pasta do projeto ao finalizar")
        self.check_AbrirPasta.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.check_AbrirPasta.setChecked(bool(checks_vars["Abrir_pasta_do_projeto"]))
        
        label_SubPastas = QLabel("Sub-pastas para criar:")
        label_SubPastas.setObjectName("medio")
        
        self.BotaoCriar = QPushButton("Criar")
        self.BotaoCriar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.BotaoCriar.clicked.connect(self.create)
        self.check_FecharAoCriar = QCheckBox("Fechar ao criar")
        self.check_FecharAoCriar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.check_FecharAoCriar.setChecked(bool(config["fechar_ao_criar"]))
         
        layout.addWidget(label_nome,0,0)
        layout.addWidget(self.campo_nome,1,0)     
        
        layout.addWidget(label_dir,2,0)
        layout.addWidget(self.campo_dir,3,0)   
        layout.addWidget(BotaoDir,3,1) 
        
        layout.addWidget(label_videos,4,0)
        layout.addWidget(self.campo_videos,6,0)   
        layout.addWidget(BotaoVideos,6,1) 
        layout.addWidget(BotaoVideosDrop,6,2) 
        
        
        
        layoutAbrirPremiereEfecharPastas = QGridLayout()
        layoutAbrirPremiereEfecharPastas.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layoutAbrirPremiereEfecharPastas.setContentsMargins(10, 20, 10, 10)
        
        layoutAbrirPremiereEfecharPastas.addWidget(self.check_AbrirPremiere,0,0)
        layoutAbrirPremiereEfecharPastas.addWidget(self.check_AbrirPasta,0,1)
        
        layout.addLayout(layoutAbrirPremiereEfecharPastas,7,0)
        
        layout.addWidget(label_SubPastas,8,0)
        self.subpasta_vars = {}
        coluna_atual = 0
        row = 0

        layoutSubpastas = QGridLayout()
        layoutSubpastas.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layoutSubpastas.setContentsMargins(10, 20, 10, 10)
        layout.addLayout(layoutSubpastas,9,0)

        for subpasta, criar in df['subpastas'].iloc[0].items():
            checkbox = QCheckBox(f"{subpasta}")
            checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.subpasta_vars[subpasta] = checkbox
            checkbox.setChecked(bool(criar))
            layoutSubpastas.addWidget(checkbox,row,coluna_atual)
            row += 1
            if row == 3:
                row = 0
                coluna_atual += 1
        
        
        layout.addWidget(self.BotaoCriar,15,0,2,2) 
        layout.addWidget(self.check_FecharAoCriar,15,2) 


        self.setLayout(layout)
        
    def create(self):
      CriarProjeto.ProjectCreator(self.campo_videos,
                                  self.campo_nome,
                                  self.subpasta_vars,
                                  self.campo_dir,
                                  self.check_AbrirPasta,
                                  self.check_FecharAoCriar,
                                  self.check_AbrirPremiere,
                                  MainWindow.main_window
                                  ).create()
      
def obter_nome_pasta(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            title_tag = soup.find('title')

            if title_tag:
                title_text = title_tag.get_text()
                texto = str(title_text).replace("Dropbox - ", "").replace(" - Simplify your life", "")
                return texto
            else:
                return 'Erro'
        else:
            return 'Erro'
    except Exception as e:
        return 'Erro'


def limpar_texto(texto):
    # Normaliza os acentos usando unidecode
    texto_normalizado = unidecode(texto)

    # Remove caracteres especiais, mantendo apenas letras e números
    texto_limpo = re.sub(r'[^a-zA-Z0-9\s-]', '', texto_normalizado)

    # Substitui "ç" por "c"
    texto_limpo = texto_limpo.replace('ç', 'c')

    return texto_limpo