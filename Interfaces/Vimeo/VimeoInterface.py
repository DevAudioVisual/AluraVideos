import os
import re
import time
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QScrollArea, QPushButton ,QFileDialog,QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from bs4 import BeautifulSoup
import pandas as pd
import requests
from Config import LoadConfigs
from Models.Vimeo.VimeoUploader import VimeoUploader
global Config

class Interface(QWidget):
    def __init__(self):
        super().__init__() 
        self.setContentsMargins(10, 20, 10, 10)
        
        
        self.label_videos = QLabel("Videos:")
        self.campo_videos = QLineEdit()
        self.campo_videos.setReadOnly(True)
        self.campo_videos.setPlaceholderText("Busque pelos vídeos para subir")
        self.campo_videos.setClearButtonEnabled(True)
        self.action_campo_videos = self.campo_videos.addAction(QIcon(r"Assets\svg\folder.svg"),QLineEdit.ActionPosition.TrailingPosition)
        self.action_campo_videos.triggered.connect(self.buscarVideos)
        
        self.label_showcase = QLabel("Nome da showcase:")
        self.campo_showcase = QLineEdit()
        self.campo_showcase.setPlaceholderText("Diga o nome para a showcase")
        self.campo_showcase.setClearButtonEnabled(True)
        
        self.botaoSubir = QPushButton("Iniciar Upload")
        self.botaoSubir.clicked.connect(self.iniciar)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        layout.addWidget(self.label_videos)
        layout.addWidget(self.campo_videos)
        layout.addWidget(self.label_showcase)
        layout.addWidget(self.campo_showcase)
        layout.addWidget(self.botaoSubir)
        
        self.setLayout(layout)
        
        self.videos = []
        self.uploader = VimeoUploader()
    
    def iniciar(self):
      showcase_uri = self.uploader.criar_showcase(self.campo_showcase.text())
      self.uploader.subir_videos_para_showcase(self.videos,showcase_uri)
        
    def buscarVideos(self):
      options = QFileDialog.Option.ReadOnly
      filters = "Arquivos de Vídeo (*.mp4 *.avi *.mov *.mkv);;Todos os Arquivos (*)"
      file_names, _ = QFileDialog.getOpenFileNames(self, "Selecionar Vídeos", "", filters, options=options)
      
      self.campo_videos.setText(file_names[0])
      self.campo_showcase.setText(os.path.basename(os.path.dirname(file_names[0])))
      
      for file in file_names:
        self.videos.append(file)