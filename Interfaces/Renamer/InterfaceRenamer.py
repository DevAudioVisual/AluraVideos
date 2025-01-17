import os
import re
import threading
from Models.Renamer import BuscarPlanilha
from Models.Renamer.Renomear import Renomear
import Util.CustomWidgets as cw
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from tkinter import filedialog

class Interface(cw.Widget):
    def __init__(self):
        super().__init__() 
        
        self.carregando = False
        
        self.setContentsMargins(10, 10, 10, 10)
        
        self.entrada_videos = {}
        self.dados = {}
                
        self.label_videos = cw.Label("Arquivos para renomear:")
        self.campo_videos = cw.LineEdit()
        self.campo_videos.setPlaceholderText("Busque pelos arquivos para renomear")
        self.campo_videos.setClearButtonEnabled(True)
        self.action_campo_videos = self.campo_videos.addAction(QIcon(r"Assets\svg\folder.svg"),cw.LineEdit.ActionPosition.TrailingPosition)
        self.action_campo_videos.setToolTip("Buscar")
        self.action_campo_videos.triggered.connect(self.buscarVideos)
        
        self.label_sheets = cw.Label("Referência")
        self.campo_sheets = cw.LineEdit()
        self.campo_sheets.setPlaceholderText("Diga a referência")
        self.campo_sheets.setClearButtonEnabled(True)
        
        self.action_campo_sheets = self.campo_sheets.addAction(QIcon(r"Assets\Images\forms.png"),cw.LineEdit.ActionPosition.TrailingPosition)
        self.action_campo_sheets.setToolTip("Buscar planilha")     
        def threadBuscarPlanilha():
            BuscarPlanilha.buscar_na_planilha(self.carregando,self.campo_formato,self.campo_sheets,self.campo_id,self.dados)
            self.atualizar_entradas_videos()  
        self.action_campo_sheets.triggered.connect(lambda: threading.Thread(target=threadBuscarPlanilha,daemon=True).start())
        
        self.action_campo_sheets = self.campo_sheets.addAction(QIcon(r"Assets\svg\folder.svg"),cw.LineEdit.ActionPosition.TrailingPosition)
        self.action_campo_sheets.setToolTip("Buscar arquivos")
        self.action_campo_sheets.triggered.connect(lambda: self.setFileVideos())
        
        self.label_id = cw.Label("ID do curso:")
        self.campo_id = cw.LineEdit()
        self.campo_id.setPlaceholderText("Digite o ID do curso ou busque pela planilha")
        self.campo_id.setClearButtonEnabled(True)
        
        self.label_sufixo = cw.Label("Sufixo:")
        self.campo_sufixo = cw.LineEdit()
        self.campo_sufixo.setPlaceholderText("Digite um sufixo")
        self.campo_sufixo.setClearButtonEnabled(True)
        
        self.label_formato = cw.Label("Padrão:")
        self.campo_formato = cw.LineEdit()
        self.campo_formato.setPlaceholderText("Variáveis disponíveis: {id} {aula} {titulo} {sufixo}")
        self.campo_formato.setText("{id}-video{aula}-{titulo}-{sufixo}")
        self.campo_formato.setToolTip("Variáveis disponíveis: {id} {aula} {titulo} {sufixo}")
        
        self.buttonrenomear = cw.PushButton("Renomear")
        self.buttonrenomear.clicked.connect(lambda: Renomear(pasta=os.path.dirname(self.campo_videos.text()),
                                                     entrada_videos=self.entrada_videos,
                                                     campo_formato=self.campo_formato.text(),
                                                     campo_id=self.campo_id.text(),
                                                     campo_sufixo=self.campo_sufixo.text()))
        
        layout = cw.VBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        layout.addWidget(self.label_videos)
        layout.addWidget(self.campo_videos)
        layout.addWidget(self.label_sheets)
        layout.addWidget(self.campo_sheets)
        layout.addWidget(self.label_id)
        layout.addWidget(self.campo_id)
        layout.addWidget(self.label_sufixo)
        layout.addWidget(self.campo_sufixo)
        layout.addWidget(self.label_formato)
        layout.addWidget(self.campo_formato)
        
        
        scroll_area = cw.ScrollArea(self)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Widget de conteúdo para a área de rolagem
        widget_conteudo = cw.Widget()
        scroll_area.setWidget(widget_conteudo)

        # Layout do widget de conteúdo
        layout_conteudo = cw.VBoxLayout(widget_conteudo)  

        # Seu layout2 (com os outros layouts)
        self.layout2 = cw.GridLayout()
        self.layoutvideos = cw.VBoxLayout()
        self.layoutnovosvideos = cw.VBoxLayout()
        self.layout2.addLayout(self.layoutvideos, 0, 0)
        self.layout2.addLayout(self.layoutnovosvideos, 0, 1)

        # Adiciona layout2 ao layout de conteúdo da scroll area
        layout_conteudo.addLayout(self.layout2)  
        layout.addWidget(self.buttonrenomear)

        self.setLayout(layout)
        
    
    def setFileVideos(self):
        VideosFilesRef = filedialog.askopenfilenames()
        try:
            self.campo_sheets.setText(VideosFilesRef[0])
            self.campo_formato.setText("{titulo}")
        except Exception as e:
            return
        
        for videos in VideosFilesRef:
            numero_aula_regex = r"(\d+\.\d+)"
            match = re.search(numero_aula_regex, os.path.basename(videos))
            if match:
                numero_aula = match.group(1)
                self.dados[f"Aula {numero_aula}"] = os.path.basename(videos)
        self.atualizar_entradas_videos()
            
    def atualizar_entradas_videos(self):
        for arquivo, entrada_nome in self.entrada_videos.items():
            nome_sem_extensao, _ = os.path.splitext(os.path.basename(arquivo))
            
            numero_aula_regex = r"(\d+\.\d+)"
            match = re.search(numero_aula_regex, nome_sem_extensao)
            if match:
                numero_aula = match.group(1)
            else:
                numero_aula = None
            
            nome_aula = self.dados.get(f"Aula {numero_aula}", "")
            entrada_nome.setText(nome_aula)
            if nome_aula:
                print(nome_aula)
        self.carregando = False
                
    def buscarVideos(self):
        file_names = filedialog.askopenfilenames(
        initialdir="/",
        title="Selecione os arquivos para renomear")
        if file_names:
            self.campo_videos.setText(file_names[0])
            for file_name in file_names:
                campo_video = cw.LineEdit()
                campo_video.setText(os.path.basename(file_name))
                campo_video.setReadOnly(True)
                
                campo_video_novo = cw.LineEdit()
                self.layoutvideos.addWidget(campo_video)
                self.layoutnovosvideos.addWidget(campo_video_novo)
                self.entrada_videos[os.path.basename(file_name)] = campo_video_novo
            
        
    
        