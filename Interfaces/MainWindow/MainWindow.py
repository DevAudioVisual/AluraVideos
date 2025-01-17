import os
from Util import Tokens
import Util.CustomWidgets as cw
from PyQt6.QtGui import QIcon, QAction,QPainter
from PyQt6.QtCore import Qt, QTranslator,QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtWidgets import QMainWindow,QApplication,QStackedWidget,QToolBar,QToolButton, QPushButton
from Config import LoadConfigs
from Interfaces.Atalhos import InterfaceAtalhos
from Interfaces.Home.Home import Interface
from Interfaces.Preferencias import InterfacePreferencias
from Interfaces.ExtensoesPPRO import InterfaceExtensoes
from Interfaces.MainWindow.MenuBar import MenuBar
from Interfaces.MainWindow.Tabs import Tabs


global main_window
main_window = None

def create_main_window(): 
    global main_window
    main_window = MainWindow()
    main_window.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        #self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.MSWindowsFixedSizeDialogHint)]
        self.barra_pequena = False
        import Main
        self.setWindowTitle(f'AluraVideos {Main.version}')
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
        
        self.extensoes = None
        self.config = InterfacePreferencias.Interface()
        self.atalhos = InterfaceAtalhos.Interface()
        self.menubar = MenuBar(self)  # Criar a instância de MenuBar
        self.tabs = Tabs(self.menubar)  # Passar a instância de MenuBar para Tabs
        
        if Tokens.AWS_S3 != None: self.Navbar()
 
        
        self.stacked_widget.addWidget(self.tabs)
        self.stacked_widget.addWidget(self.config)
        self.stacked_widget.addWidget(self.atalhos)
        
        self.extensoes = InterfaceExtensoes.Interface()
        if os.path.isdir(r"C:\Program Files (x86)\Common Files\Adobe\CEP\extensions"): self.stacked_widget.addWidget(self.extensoes)
        
        
        #SystemTrayIcon.SystemTrayIcon(self)
        #TeclasAtalho().registrarAtalhos()
    def closeEvent(self, event):
        try:
            data = LoadConfigs.Config.getConfigData(config="ConfigInterface") 
            data['barra_lateral_pequena'] = self.barra_pequena
            LoadConfigs.Config.saveConfigDict("ConfigInterface",data)
            self.tabs.save()
        except Exception as e:
            print(e)
        event.accept()
    def Navbar(self):
        # Criar a barra de ferramentas (navbar)
        self.toolbar = cw.ToolBar("", self)
        self.toolbar.setOrientation(Qt.Orientation.Vertical)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolbar.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)
        
        # Adicionar ações à barra de ferramentas
        acao_home = QAction(QIcon(r"Assets\Icons\icon.ico"), "Home", self)
        acao_edicao = QAction(QIcon(r"Assets\Images\penguin.png"), "Ferramentas", self)
        acao_producao = QAction(QIcon(r"Assets\Images\penguin.png"), "Produção", self)
        acao_outros = QAction(QIcon(r"Assets\Images\penguin.png"), "Outros", self)
        acao_ppro = QAction(QIcon(r"Assets\Icons\prproj.ico"), "Extensões PPRO", self)
        #acao_configuracoes = QAction(QIcon(r"Assets\Icons\config.ico"), "Configurações", self)
        
        #spacer = cw.Widget()
        #spacer.setSizePolicy(cw.SizePolicy.Policy.Expanding, cw.SizePolicy.Policy.Expanding)
        #self.toolbar.addWidget(spacer)
        
        self.toolbar.addAction(acao_home)
        self.toolbar.widgetForAction(acao_home).setProperty("active",True)
        acao_home.triggered.connect(self.mostrar_home)
        acao_home.triggered.connect(self.atualizar_estilo_botoes)
        
        self.toolbar.addAction(acao_edicao)
        acao_edicao.triggered.connect(self.mostrar_ferramentas)
        acao_edicao.triggered.connect(self.atualizar_estilo_botoes)
        
        if os.path.isdir(r"C:\Program Files (x86)\Common Files\Adobe\CEP\extensions"):
            self.toolbar.addAction(acao_ppro)
            acao_ppro.triggered.connect(self.mostrar_extensoes)
            acao_ppro.triggered.connect(self.atualizar_estilo_botoes)
        
        self.toolbar.addSeparator()
        self.botao_expandir = cw.PushButton("",animacao=False)
        #self.botao_expandir.setObjectName("botaoMenuBarraLateral")
        self.botao_expandir.setIcon(QIcon(r"Assets\svg\menu.svg"))
        self.botao_expandir.clicked.connect(self.change_animation_direction)
        self.toolbar.addWidget(self.botao_expandir)
        
        
        self.animationMin = QPropertyAnimation(self.toolbar, b"minimumWidth")
        self.animationMin.setDuration(500)  # 1 segundo
        self.animationMin.setStartValue(70)
        self.animationMin.setEndValue(200)
        self.animationMin.setEasingCurve(QEasingCurve.Type.InOutCubic)
        
        self.animationMax = QPropertyAnimation(self.toolbar, b"maximumWidth")
        self.animationMax.setDuration(500)  # 1 segundo
        self.animationMax.setStartValue(70)
        self.animationMax.setEndValue(200)
        self.animationMax.setEasingCurve(QEasingCurve.Type.InOutCubic)
        
        for action in self.toolbar.actions():
            button = self.toolbar.widgetForAction(action)
            if button:
                button.setMinimumWidth(180)
                button.setMaximumWidth(180)
                
        if bool(LoadConfigs.Config.getConfigData(config="ConfigInterface",data="barra_lateral_pequena")) == True:
            self.barra_pequena = True
            self.toolbar.setMinimumWidth(70)
            self.toolbar.setMaximumWidth(70)
            self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
            for action in self.toolbar.actions():
                button = self.toolbar.widgetForAction(action)
                if button:
                    button.setMinimumWidth(70)
                    button.setMaximumWidth(70)
                    button.style().unpolish(button)
                    button.style().polish(button)
        else:
            self.barra_pequena = False
            self.toolbar.setMinimumWidth(200)
            self.toolbar.setMaximumWidth(200)
            for action in self.toolbar.actions():
                button = self.toolbar.widgetForAction(action)
                if button:
                    button.setMinimumWidth(200)
                    button.setMaximumWidth(200)
                    button.style().unpolish(button)
                    button.style().polish(button)
           
    def change_animation_direction(self):
        if self.barra_pequena == False:
            self.animationMin.setDirection(QPropertyAnimation.Direction.Backward)
            self.animationMin.finished.connect(lambda: self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly))
            self.animationMin.start()
            self.barra_pequena = True
            
            def mudar():
                tamanho = self.toolbar.minimumWidth()-10  # Obtém o valor atual de minimumWidth
                for action in self.toolbar.actions():
                    button = self.toolbar.widgetForAction(action)
                    if button:
                        button.setMinimumWidth(tamanho)
                        button.setMaximumWidth(tamanho)
                        button.style().unpolish(button)
                        button.style().polish(button)

                if not self.isMaximized(): self.adjustSize()
            self.animationMin.valueChanged.connect(mudar)
        else:
            self.animationMax.setDirection(QPropertyAnimation.Direction.Forward)
            self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            self.animationMax.start()
            self.barra_pequena = False
            def mudar():
                tamanho = self.toolbar.maximumWidth()-10  # Obtém o valor atual de minimumWidth
                for action in self.toolbar.actions():
                    button = self.toolbar.widgetForAction(action)
                    if button:
                        button.setMinimumWidth(tamanho)
                        button.setMaximumWidth(tamanho)
                        button.style().unpolish(button)
                        button.style().polish(button)
                if not self.isMaximized(): self.adjustSize()

            self.animationMax.valueChanged.connect(mudar)

           
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
        
    def showEvent(self, event):
        # Centralizar a janela no monitor atual após ela ser exibida
        qtRectangle = self.frameGeometry()
        centerPoint = self.window().windowHandle().screen().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        super().showEvent(event)
        