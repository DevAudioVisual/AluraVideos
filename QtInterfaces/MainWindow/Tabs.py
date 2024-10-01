from PyQt6.QtWidgets import QVBoxLayout, QTabWidget,QMenu
from QtInterfaces.ImagensPixaBay import ImagensPixabay
from QtInterfaces.LimparCache import InterfaceLimparCache
from QtInterfaces.ProjectCreator import InterfaceProjectCreator
from QtInterfaces.S3 import InterfaceS3
from PyQt6.QtGui import QAction

class Tabs(QTabWidget):
    def __init__(self, menubar):  # Passar a instância de MenuBar
        super().__init__()
        self.menubar = menubar  # Armazenar a instância de MenuBar

        self.InterfaceProjectCreator = InterfaceProjectCreator.Interface()
        self.InterfaceLimparCache = InterfaceLimparCache.Interface()
        self.InterfaceAssetsPixaBay = ImagensPixabay.Interface()
        self.InterfaceS3 = InterfaceS3.Interface()

        self.closed_tabs = {}

        self.setMovable(True)
        self.setTabsClosable(False)
        self.tabCloseRequested.connect(self.close_tab)

        self.addTab(self.InterfaceProjectCreator, "Criar Projeto")
        self.addTab(self.InterfaceS3, "S3")
        self.addTab(None, "PM3")
        self.addTab(self.InterfaceAssetsPixaBay, "Imagens PixaBay")
        self.addTab(self.InterfaceLimparCache, "Limpar Cache")

        layout = QVBoxLayout()
        layout.addWidget(self)
        
    def contextMenuEvent(self, event):
        # Obter a referência ao QTabBar
        tab_bar = self.tabBar()

        # Verificar se o clique foi em uma aba
        tab_index = tab_bar.tabAt(event.pos())

        # Verificar se o widget que recebeu o evento é o QTabWidget ou um de seus filhos
        if tab_index >= 0 and (self.childAt(event.pos()) is not None or self == self.childAt(event.pos())):
            # Clique em uma aba e dentro da área do QTabWidget
            # Criar o menu de contexto
            menu = QMenu(self)
            close_action = QAction("Fechar", self)
            menu.addAction(close_action)

            # Conectar a ação de fechar à função close_tab
            close_action.triggered.connect(lambda: self.close_tab(tab_index))

            # Exibir o menu de contexto na posição do clique do mouse
            menu.exec(event.globalPos())
            
    def close_tab(self, index):
        tab_name = self.tabText(index)
        self.closed_tabs[tab_name] = self.widget(index)
        self.removeTab(index)

        existing_action = self.menubar.janelas_submenu.findChild(QAction, tab_name)
        if existing_action is None:
            reopen_action = QAction(tab_name, self)
            reopen_action.triggered.connect(lambda _, name=tab_name: self.reopen_tab(name))
            self.menubar.janelas_submenu.addAction(reopen_action)

    def reopen_tab(self, tab_name):
        print("Reopen")
        if tab_name in self.closed_tabs:
            print("esta")
            self.addTab(self.closed_tabs[tab_name], tab_name)
            del self.closed_tabs[tab_name]
            # Remover a ação de reabrir do menu
            actions = self.menubar.janelas_submenu.actions()
            for action in actions:
                if action.text() == tab_name:
                    self.menubar.janelas_submenu.removeAction(action)
                    break