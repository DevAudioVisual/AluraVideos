import os
import webbrowser
from PyQt6.QtGui import QAction,QIcon
from PyQt6.QtWidgets import QMenu

class MenuBar():
    def __init__(self, MainWindow):
      self.MainWindow = MainWindow
      self.menubar = self.MainWindow.menuBar()
      self.janelas_submenu = QMenu("Janelas fechadas:", self.MainWindow)
      self.Arquivo()
      self.Visualizar()
      self.Ajuda()
      
    def Arquivo(self):
      self.visualizar_menu = self.menubar.addMenu("Arquivo")
      self.logs_action = QAction(QIcon(r"Assets\Images\logs.png"), "Logs", self.MainWindow)
      self.repositorion_action = QAction(QIcon(r"Assets\Icons\github.ico"), "Repositório", self.MainWindow)
      self.atalhos_action = QAction(QIcon(r"Assets\Icons\keyboard.ico"), "Atalhos", self.MainWindow)
      self.preferences_action = QAction(QIcon(r"Assets\Icons\config.ico"), "Preferências", self.MainWindow)
      self.visualizar_menu.addAction(self.logs_action)
      self.visualizar_menu.addAction(self.repositorion_action)
      self.visualizar_menu.addAction(self.atalhos_action)
      self.visualizar_menu.addAction(self.preferences_action)
      
      def abrir_logs():
        log_file_path = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos", "Logs")
        webbrowser.open(log_file_path) 
      self.logs_action.triggered.connect(abrir_logs)
      def abrir_repositorio():
        webbrowser.open("https://github.com/DevAudioVisual/AluraVideos")
      self.repositorion_action.triggered.connect(abrir_repositorio)
      self.preferences_action.triggered.connect(self.MainWindow.mostrar_configuracoes)
      
    def Visualizar(self):
      self.visualizar_menu = self.menubar.addMenu("Visualizar")
      self.visualizar_menu.addMenu(self.janelas_submenu)
      
    def Ajuda(self):
      self.ajuda_menu = self.menubar.addMenu("Ajuda")
      self.exit_action = QAction("Sair", self.MainWindow)
      
      self.ajuda_menu.addSeparator()  
      self.ajuda_menu.addAction(self.exit_action)
      
      self.exit_action.triggered.connect(self.MainWindow.close) 
      
      