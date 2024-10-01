from PyQt6.QtGui import QAction
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
      self.logs_action = QAction("Logs", self.MainWindow)
      self.visualizar_menu.addAction(self.logs_action)
      
    def Visualizar(self):
      self.visualizar_menu = self.menubar.addMenu("Visualizar")
      self.visualizar_menu.addMenu(self.janelas_submenu)
      
      self.criar_projeto_action = QAction("Criar Projeto", self.MainWindow)
      self.limpar_cache_action = QAction("Limpar Cache", self.MainWindow)
      self.s3_action = QAction("S3", self.MainWindow)
      self.pm3_action = QAction("PM3", self.MainWindow)
      self.imagens_pixabay_action = QAction("Imagens PixaBay", self.MainWindow)
      
      # self.janelas_submenu.addAction(self.criar_projeto_action)
      # self.janelas_submenu.addAction(self.limpar_cache_action)
      # self.janelas_submenu.addAction(self.s3_action)
      # self.janelas_submenu.addAction(self.pm3_action)
      # self.janelas_submenu.addAction(self.imagens_pixabay_action)
      
    def Ajuda(self):
      self.ajuda_menu = self.menubar.addMenu("Ajuda")
      self.exit_action = QAction("Sair", self.MainWindow)
      
      self.ajuda_menu.addSeparator()  
      self.ajuda_menu.addAction(self.exit_action)
      
      self.exit_action.triggered.connect(self.MainWindow.close) 
      
      