import sys
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QSpacerItem, QToolBar, QSizePolicy,QWidget, QPushButton,QStackedWidget,QToolButton,QApplication
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from QtInterfaces.Preferencias import InterfacePreferencias
from QtInterfaces.ExtensõesPPRO import InterfaceExtensoes
from QtInterfaces.MainWindow.MenuBar import MenuBar
from QtInterfaces.MainWindow.Tabs import Tabs
from Util import Util

global main_window
main_window = None

def create_main_window(): 
    global main_window
    main_window = MainWindow()
    main_window.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'AluraVideos {Util.version}')
        icon = QIcon(r"Assets\Icons\icon.ico")
        self.setWindowIcon(icon) 
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.extensoes = InterfaceExtensoes.Interface()
        self.config = InterfacePreferencias.Interface()
        
        
        self.menubar = MenuBar(self)  # Criar a instância de MenuBar
        self.tabs = Tabs(self.menubar)  # Passar a instância de MenuBar para Tabs
        
        self.Navbar()
 
        
        self.stacked_widget.addWidget(self.tabs)
        self.stacked_widget.addWidget(self.config)
        self.stacked_widget.addWidget(self.extensoes)

    def closeEvent(self, event):
        print("################# ENCERRANDO")
        #sys.exit()    
    def Navbar(self):
        # Criar a barra de ferramentas (navbar)
        self.toolbar = QToolBar("", self)
        self.toolbar.setOrientation(Qt.Orientation.Vertical)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolbar.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        #self.toolbar.setMaximumWidth(500)
        self.toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)
        
        # Adicionar ações à barra de ferramentas
        acao_home = QAction(QIcon(r"Assets\Images\penguin.png"), "Home", self)
        acao_ppro = QAction(QIcon(r"Assets\Icons\prproj.ico"), "Extensões PPRO", self)
        #acao_configuracoes = QAction(QIcon(r"Assets\Icons\config.ico"), "Configurações", self)
        
        self.toolbar.addAction(acao_home)
        self.toolbar.widgetForAction(acao_home).setProperty("active",True)
        acao_home.triggered.connect(self.mostrar_home)
        acao_home.triggered.connect(self.atualizar_estilo_botoes)
        self.toolbar.addAction(acao_ppro)
        acao_ppro.triggered.connect(self.mostrar_extensoes)
        acao_ppro.triggered.connect(self.atualizar_estilo_botoes)
        
        # self.toolbar.addAction(acao_configuracoes)
        # acao_configuracoes.triggered.connect(self.mostrar_configuracoes)
        # acao_configuracoes.triggered.connect(self.atualizar_estilo_botoes)
        
        self.botao_expandir = QPushButton("<")
        #self.toolbar.addWidget(self.botao_expandir)
        self.botao_expandir.clicked.connect(self.toggle_sidebar)
        
        
        botao_expandir_container = QWidget()
        botao_expandir_layout = QVBoxLayout(botao_expandir_container)
        botao_expandir_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)  # Alinhar o botão ao fundo
        botao_expandir_layout.setContentsMargins(0, 0, 0, 0)  # Remover margens extras
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        botao_expandir_layout.addItem(spacer)
        botao_expandir_layout.addWidget(self.botao_expandir)

        # Adicionar o container à toolbar com alinhamento para baixo
        self.toolbar.addWidget(botao_expandir_container)
        toolbar_layout = self.toolbar.layout()

        # Alinhar o container ao fundo usando o layout
        toolbar_layout.setAlignment(botao_expandir_container, Qt.AlignmentFlag.AlignBottom)

        self.original_sidebar_width = self.toolbar.maximumWidth()  # Corrigido para self.toolbar
        self.minimized_sidebar_width = 50
        
        
        
        for action in self.toolbar.actions():
            button = self.toolbar.widgetForAction(action)
            if button:
                button.setMinimumWidth(150)

    def toggle_sidebar(self):
        if self.toolbar.maximumWidth() == self.minimized_sidebar_width:  # Barra lateral minimizada
            self.toolbar.setMaximumWidth(self.original_sidebar_width)  # Expandir
            self.botao_expandir.setText("<")
            self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            
            for action in self.toolbar.actions():
                button = self.toolbar.widgetForAction(action)
                if button:
                    button.setMinimumWidth(150)
            
        else:  # Barra lateral expandida
            self.toolbar.setMaximumWidth(self.minimized_sidebar_width)  # Minimizar
            self.botao_expandir.setText(">")
            self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
            
            for action in self.toolbar.actions():
                button = self.toolbar.widgetForAction(action)
                if button:
                    button.setMinimumWidth(0)
           
    def atualizar_estilo_botoes(self):
        sender_action = self.sender() 

        if sender_action:
            sender_button = self.toolbar.widgetForAction(sender_action)
            for action in self.toolbar.actions():
                widget = self.toolbar.widgetForAction(action)
                if isinstance(widget, QToolButton):
                    widget.setProperty("active", False)
                    widget.style().unpolish(widget)
                    widget.style().polish(widget)

            sender_button.setProperty("active", True)
            sender_button.style().unpolish(sender_button)
            sender_button.style().polish(sender_button)
    
    def mostrar_home(self):
        self.stacked_widget.setCurrentWidget(self.tabs)

    def mostrar_configuracoes(self):
        self.stacked_widget.setCurrentWidget(self.config)
        
    def mostrar_extensoes(self):
        self.stacked_widget.setCurrentWidget(self.extensoes)