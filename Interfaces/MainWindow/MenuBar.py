import os
import webbrowser
from PyQt6.QtGui import QAction,QIcon
from PyQt6.QtWidgets import QMenu
import jwt
import requests

from Interfaces.Administrador import AdministradorDialog
from Util import Tokens

class MenuBar():
    def __init__(self, MainWindow):
      self.MainWindow = MainWindow
      self.menubar = self.MainWindow.menuBar()
      self.janelas_submenu = QMenu("Janelas fechadas:", self.MainWindow)
      if Tokens.AWS_S3 != None: 
        self.Arquivo()
        self.Visualizar()
        self.Ajuda()
      
    def Arquivo(self):
      self.visualizar_menu = self.menubar.addMenu("Arquivo")
      self.atalhos_action = QAction(QIcon(r"Assets\Icons\shortcut.ico"), "Atalhos (Em breve)", self.MainWindow)
      self.atalhos_action.setStatusTip("Em breve")
      
      self.logs_action = QAction(QIcon(r"Assets\Images\logs.png"), "Logs", self.MainWindow)
      self.logs_action.setStatusTip("Acesse o arquivo de logs do AluraVideos")
      
      self.repositorion_action = QAction(QIcon(r"Assets\Icons\github.ico"), "Repositório", self.MainWindow)
      
      self.notion_action = QAction(QIcon(r"Assets\Icons\notion.ico"), "Documentação", self.MainWindow)
      self.notion_action.setStatusTip("Acesse a documentação oficial do AluraVideos")
      
      self.preferences_action = QAction(QIcon(r"Assets\Icons\config.ico"), "Preferências (Em breve)", self.MainWindow)
      self.preferences_action.setStatusTip("Em breve")
      
      self.administrador_action = QAction(QIcon(r"Assets\svg\user.svg"), "Administrador", self.MainWindow)
      self.administrador_action.setStatusTip("Painel administrador")
      
      self.visualizar_menu.addAction(self.atalhos_action)
      self.visualizar_menu.addAction(self.logs_action)
      self.visualizar_menu.addAction(self.repositorion_action)
      self.visualizar_menu.addAction(self.notion_action)
      self.visualizar_menu.addSeparator()
      self.visualizar_menu.addAction(self.preferences_action)
      
      if self.isAdm(): 
        self.visualizar_menu.addSeparator()
        self.visualizar_menu.addAction(self.administrador_action)
      

      #self.atalhos_action.triggered.connect(self.MainWindow.mostrar_atalhos)
      
      self.logs_action.triggered.connect(lambda: webbrowser.open(os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos", "Logs")) ) 
      self.repositorion_action.triggered.connect(lambda: webbrowser.open("https://github.com/DevAudioVisual/AluraVideos"))
      self.notion_action.triggered.connect(lambda: webbrowser.open("https://www.notion.so/grupoalura/AluraVideos-8589d6eab57744b7a9ccf4080c0b6bca?pvs=25"))
      self.preferences_action.triggered.connect(self.MainWindow.mostrar_configuracoes)
      self.administrador_action.triggered.connect(lambda: AdministradorDialog.TabelaDialog().exec())
      
    def Visualizar(self):
      self.visualizar_menu = self.menubar.addMenu("Visualizar")
      self.visualizar_menu.addMenu(self.janelas_submenu)
      
    def Ajuda(self):
      self.ajuda_menu = self.menubar.addMenu("Ajuda")
      self.exit_action = QAction("Sair", self.MainWindow)
      
      self.ajuda_menu.addSeparator()  
      self.ajuda_menu.addAction(self.exit_action)
      
      self.exit_action.triggered.connect(self.MainWindow.close) 
    def isAdm(self):
      try:
          key = "O+k9G/kMiXqcm+FRKGvAWQ=="
          dir = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos")
          tokens = os.path.join(dir,"credentials.json") 
          with open(tokens, 'r') as f:
              encoded_jwt = f.read()  # Lê o token do arquivo
              self.decoded_jwt = jwt.decode(encoded_jwt, key, algorithms=['HS256'])
          response = requests.post("https://samuka.pythonanywhere.com/isadm",json=self.decoded_jwt,timeout=60)
          if response.status_code == 200:
            return True
          else:
            return False
      except Exception as e:
        return False
      
      