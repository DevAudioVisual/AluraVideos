import os
import Util.CustomWidgets as cw
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, QTranslator
from PyQt6.QtWidgets import QMainWindow,QApplication,QStackedWidget,QToolBar,QToolButton
from Config import LoadConfigs
from QtInterfaces.Interfaces.Atalhos import InterfaceAtalhos
from QtInterfaces.Interfaces.Home.Home import Interface
from QtInterfaces.Interfaces.Preferencias import InterfacePreferencias
from QtInterfaces.Interfaces.ExtensõesPPRO import InterfaceExtensoes
from QtInterfaces.Interfaces.MainWindow.MenuBar import MenuBar
from QtInterfaces.Interfaces.MainWindow.Tabs import Tabs
from Util import Tokens, Util

global main_window
main_window = None

def create_main_window(): 
    global main_window
    main_window = MainWindow()
    main_window.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        #self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle(f'AluraVideos {Util.version}')
        icon = QIcon(r"Assets\Icons\icon.ico")
        self.setWindowIcon(icon)
        
        translator = QTranslator(self)
        # Define o idioma para português
        translator.load("qtbase_pt_BR.qm", ":/translations")  # Caminho para o arquivo de tradução
        QApplication.instance().installTranslator(translator)
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.home = Interface()
        self.stacked_widget.addWidget(self.home)
        
        dir = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos")
        tokens = os.path.join(dir,"tokens.yml")
        key = os.path.join(dir,"key.key")
        if not os.path.exists(tokens) or not os.path.exists(key):
            return
        
        
        
        self.extensoes = None
        self.config = InterfacePreferencias.Interface()
        self.atalhos = InterfaceAtalhos.Interface()
        self.menubar = MenuBar(self)  # Criar a instância de MenuBar
        self.tabs = Tabs(self.menubar)  # Passar a instância de MenuBar para Tabs
        
        self.Navbar()
        self.barra_pequena = False
 
        
        self.stacked_widget.addWidget(self.tabs)
        self.stacked_widget.addWidget(self.config)
        self.stacked_widget.addWidget(self.atalhos)
        
        self.extensoes = InterfaceExtensoes.Interface()
        self.stacked_widget.addWidget(self.extensoes)
        
        
        #SystemTrayIcon.SystemTrayIcon(self)
        #TeclasAtalho().registrarAtalhos()

    def closeEvent(self, event):
        # if self.isHidden(): QApplication.quit()
        # reply = QMessageBox.question(self, "Fechar",
        #     "Minimizar para a bandeja do sistema?",
        #     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        #     QMessageBox.StandardButton.Yes)

        # if reply == QMessageBox.StandardButton.Yes:
        #     self.hide()
        #     toast = Notification(app_id="AluraVideos",
        #                  title="AluraVideos",
        #                  msg="AluraVideos está rodando em segundo plano",
        #                  icon=r"Assets\Icons\icon.ico",
        #                  duration="long")
        #     # Define um som para a notificação
        #     toast.set_audio(audio.LoopingAlarm, loop=False)
            
        #     toast.show()
        #     event.ignore()  # Impede o fechamento da aplicação
        # else:
        #     event.accept()  # Fecha a aplicação
        try:
            data = LoadConfigs.Config.getConfigData(config="ConfigInterface") 
            data['barra_lateral_pequena'] = self.barra_pequena
            LoadConfigs.Config.saveConfigDict("ConfigInterface",data)
            self.tabs.save()
        except Exception as e:
            print(e)
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
        acao_home = QAction(QIcon(r"Assets\Icons\icon.ico"), "Home", self)
        acao_edicao = QAction(QIcon(r"Assets\Images\penguin.png"), "Ferramentas", self)
        acao_producao = QAction(QIcon(r"Assets\Images\penguin.png"), "Produção", self)
        acao_outros = QAction(QIcon(r"Assets\Images\penguin.png"), "Outros", self)
        acao_ppro = QAction(QIcon(r"Assets\Icons\prproj.ico"), "Extensões PPRO", self)
        #acao_configuracoes = QAction(QIcon(r"Assets\Icons\config.ico"), "Configurações", self)
        
        self.toolbar.addAction(acao_home)
        self.toolbar.widgetForAction(acao_home).setProperty("active",True)
        acao_home.triggered.connect(self.mostrar_home)
        acao_home.triggered.connect(self.atualizar_estilo_botoes)
        
        self.toolbar.addAction(acao_edicao)
        acao_edicao.triggered.connect(self.mostrar_ferramentas)
        acao_edicao.triggered.connect(self.atualizar_estilo_botoes)
        
        self.toolbar.addAction(acao_ppro)
        acao_ppro.triggered.connect(self.mostrar_extensoes)
        acao_ppro.triggered.connect(self.atualizar_estilo_botoes)
        

        
        self.botao_expandir = cw.PushButton("<")
        self.botao_expandir.clicked.connect(self.toggle_sidebar)

        #spacer = QWidget()
        #spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        #self.toolbar.addWidget(spacer)
        self.toolbar.addWidget(self.botao_expandir)

        # Alinhar o container ao fundo usando o layout

        self.original_sidebar_width = self.toolbar.maximumWidth()  # Corrigido para self.toolbar
        self.minimized_sidebar_width = 50
        
        
        
        for action in self.toolbar.actions():
            button = self.toolbar.widgetForAction(action)
            if button:
                button.setMinimumWidth(150)
        
        if bool(LoadConfigs.Config.getConfigData(config="ConfigInterface",data="barra_lateral_pequena")) == True:
            self.toggle_sidebar()

    def toggle_sidebar(self):
        if self.toolbar.maximumWidth() == self.minimized_sidebar_width:  # Barra lateral minimizada
            self.toolbar.setMaximumWidth(self.original_sidebar_width)  # Expandir
            self.botao_expandir.setText("<")
            self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            self.barra_pequena = False
            
            for action in self.toolbar.actions():
                button = self.toolbar.widgetForAction(action)
                if button:
                    button.setMinimumWidth(150)
            
        else: 
            self.toolbar.setMaximumWidth(self.minimized_sidebar_width)  # Minimizar
            self.botao_expandir.setText(">")
            self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
            self.barra_pequena = True
            
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
        self.stacked_widget.setCurrentWidget(self.home)
    
    def mostrar_ferramentas(self):
        self.stacked_widget.setCurrentWidget(self.tabs)

    def mostrar_configuracoes(self):
        self.stacked_widget.setCurrentWidget(self.config)
        
    def mostrar_atalhos(self):
        self.stacked_widget.setCurrentWidget(self.atalhos)
        
    def mostrar_extensoes(self):
        self.stacked_widget.setCurrentWidget(self.extensoes)