import re
import threading
import Util.CustomWidgets as cw
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QCursor, QAction
from bs4 import BeautifulSoup
from unidecode import unidecode
import requests
from Config import LoadConfigs
from Models.CriarProjeto import CriarProjeto
from QtInterfaces.Interfaces.MainWindow import MainWindow
global Config
import tkinter as tk
from tkinter import filedialog

class Interface(cw.Widget):
    def __init__(self):
        super().__init__() 
        self.df = LoadConfigs.Config.getDataFrame("ConfigCriarProjeto")
        self.config = LoadConfigs.Config.getConfigData("ConfigCriarProjeto")
        self.stacked_widget = cw.StackedWidget(self)
        
        self.campo_videos = cw.LineEdit()
        self.campo_nome = cw.LineEdit()
        
        self.widgetLayoutPrincipal = cw.Widget()
        self.widgetLayoutPrincipal.setLayout(self.layoutPrincipal())
        self.stacked_widget.addWidget(self.widgetLayoutPrincipal)
        
        
        layout = cw.VBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.ultimo_texto = ""
        self.numero = 0
    
    def layoutPrincipal(self):
        layout = cw.GridLayout()

        label_nome = cw.Label("Nome do projeto:")
        label_nome.setObjectName("medio")
        self.campo_nome.setClearButtonEnabled(True)
        self.campo_nome.setPlaceholderText("Digite o nome do projeto")
        #self.campo_nome.setText("00_Novo Projeto")
        
        label_dir = cw.Label("Diretório de criação:")
        label_dir.setObjectName("medio")
        self.campo_dir = cw.LineEdit()
        self.campo_dir.setText(self.config["diretorio_padrao"])
        self.campo_dir.setPlaceholderText("Diga onde o projeto será criado.")
        self.campo_dir.setClearButtonEnabled(True)
        dir_action = self.campo_dir.addAction(QIcon(r"Assets\svg\folder.svg"), cw.LineEdit.ActionPosition.TrailingPosition)
        
        tool_button = self.campo_dir.findChildren(QAction)[0] 
        tool_button.setToolTip("Buscar vídeos")
        
        def open_folder_dialog():
            file_name = filedialog.askdirectory()
            if file_name:
                print(f"Pasta selecionado: {file_name}")
                self.campo_dir.setText(rf"{file_name}")
                self.updateConfig()
        dir_action.triggered.connect(open_folder_dialog)
        
        label_videos = cw.Label("Arquivo de vídeos (Arquivo ZIP ou URL)")
        label_videos.setObjectName("medio")
        self.campo_videos.setPlaceholderText("Digite a URL ou o local dos arquivos.")
        self.campo_videos.setClearButtonEnabled(True)
        #self.campo_videos.findChildren(QAction)[0].setIcon(QIcon(r"Assets\svg\folder.svg"))
        buscar_videos_action = self.campo_videos.addAction(QIcon(r"Assets\svg\folder.svg"), cw.LineEdit.ActionPosition.TrailingPosition)
        
        def open_file_dialog_videos():
            file_name = filedialog.askopenfilename()
            if file_name:
                print(f"Arquivo selecionado: {file_name}")
                self.campo_videos.setText(rf"{file_name}")
        buscar_videos_action.triggered.connect(open_file_dialog_videos)
        BotaoVideosDrop = cw.PushButton("Buscar Nome  ")
        BotaoVideosDrop.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        BotaoVideosDrop.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        BotaoVideosDrop.setIcon(QIcon(r"Assets\Icons\dropbox.ico"))
        BotaoVideosDrop.clicked.connect(self.setNomeProjeto)
        
        checks_vars = {}
        checks = self.df['checks'].iloc[0].items()
        for ch, ci in checks:
            checks_vars[ch] = ci
        
        self.group_processos = cw.GroupBox("Processos")
        self.layout_processos = cw.GridLayout()
        self.group_processos.setLayout(self.layout_processos)
        
        self.check_AbrirPremiere = cw.CheckBox("Abrir Premiere ao finalizar")
        self.check_AbrirPremiere.clicked.connect(self.updateConfig)
        self.check_AbrirPremiere.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.check_AbrirPremiere.setChecked(bool(checks_vars["Abrir_Premiere"]))
        
        self.check_AbrirPasta = cw.CheckBox("Abrir pasta do projeto ao finalizar")
        self.check_AbrirPasta.clicked.connect(self.updateConfig)
        self.check_AbrirPasta.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.check_AbrirPasta.setChecked(bool(checks_vars["Abrir_pasta_do_projeto"]))
        
        self.check_FecharAoCriar = cw.CheckBox("Fechar ao criar")
        self.check_FecharAoCriar.clicked.connect(self.updateConfig)
        self.check_FecharAoCriar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.check_FecharAoCriar.setChecked(bool(self.config["fechar_ao_criar"]))
        
        self.BotaoCriar = cw.PushButton("Criar")
        self.BotaoCriar.clicked.connect(self.create)
         
        layout.addWidget(label_nome,0,0)
        layout.addWidget(self.campo_nome,1,0)     
        
        layout.addWidget(label_dir,2,0)
        layout.addWidget(self.campo_dir,3,0)   
        
        layout.addWidget(label_videos,4,0)
        layout.addWidget(self.campo_videos,6,0)   
        layout.addWidget(BotaoVideosDrop,6,1) 
        
        self.layout_processos.addWidget(self.check_AbrirPremiere,0,0)
        self.layout_processos.addWidget(self.check_AbrirPasta,0,1)
        self.layout_processos.addWidget(self.check_FecharAoCriar,0,2) 
        
        layout.addWidget(self.group_processos,7,0)
        
        self.subpasta_vars = {}
        coluna_atual = 0
        row = 0

        self.subpastas_group_box = cw.GroupBox("Sub-pastas")
        layoutSubpastas = cw.GridLayout()
        self.subpastas_group_box.setLayout(layoutSubpastas)

        #layoutSubpastas.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layoutSubpastas.setContentsMargins(10, 20, 10, 10)

        layout.addWidget(self.subpastas_group_box,9,0,2,2)

        for subpasta, criar in self.df['subpastas'].iloc[0].items():
            checkbox = cw.CheckBox(f"{subpasta}")
            checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.subpasta_vars[subpasta] = checkbox
            checkbox.setChecked(bool(criar))
            checkbox.clicked.connect(self.updateConfig)
            layoutSubpastas.addWidget(checkbox,row,coluna_atual)
            row += 1
            if row == 3:
                row = 0
                coluna_atual += 1
        
        
        layout.addWidget(self.BotaoCriar,15,0,2,2) 

        return layout
    def updateConfig(self):
        config = LoadConfigs.Config.getConfigData("ConfigCriarProjeto")
        
        config["fechar_ao_criar"] = self.check_FecharAoCriar.isChecked()
        config["checks"] = [{
                "Abrir_Premiere": self.check_AbrirPremiere.isChecked(),
                "Abrir_pasta_do_projeto": self.check_AbrirPasta.isChecked()
                }]   
        subpastas = {}
        for subpasta, var in self.subpasta_vars.items():
            subpastas[subpasta] = var.isChecked()
        config["subpastas"] = [subpastas]
        
        config["diretorio_padrao"] = self.campo_dir.text()
                
        LoadConfigs.Config.saveConfigDict("ConfigCriarProjeto",config)
    def create(self):
      CriarProjeto.ProjectCreator(self.campo_videos,
                                  self.campo_nome,
                                  self.subpasta_vars,
                                  self.campo_dir,
                                  self.check_AbrirPasta.isChecked(),
                                  self.check_FecharAoCriar.isChecked(),
                                  self.check_AbrirPremiere.isChecked(),
                                  MainWindow.main_window,
                                  self.stacked_widget
                                  ).create()
    def setNomeProjeto(self):
            if not self.campo_videos.text().startswith("https://www.dropbox.com"):
                cw.MessageBox.warning(None, "Aviso", "Link dropbox inválido ou inexistente.")
                return
            def buscar():
                self.setCursor(Qt.CursorShape.WaitCursor)
                self.campo_nome.setText("Buscando...")
                self.BotaoCriar.setText("Aguarde...")
                self.BotaoCriar.setEnabled(False)
                self.update()
                
                nome = obter_nome_pasta(self.campo_videos.text())
                
                self.setCursor(Qt.CursorShape.ArrowCursor)
                self.campo_nome.setText(limpar_texto(nome))
                self.BotaoCriar.setText("Criar")
                self.BotaoCriar.setEnabled(True)
                self.update()
            threading.Thread(target=buscar,daemon=True).start()
    def setTextCampoVideos(self, text):
        texto = str(text)
        self.campo_videos.setText(texto)
        self.setNomeProjeto()
        self.update()  # Atualiza a interface explicitamente
    def mensagem(self):
        cw.MessageBox.information(None,"Info","Link dropbox detectado na área de transferência!\nInserido em criar projeto.")

      
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


