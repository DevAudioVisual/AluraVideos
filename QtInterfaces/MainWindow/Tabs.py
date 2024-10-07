from PyQt6.QtWidgets import QVBoxLayout, QTabWidget,QMenu
from Config import LoadConfigs
from QtInterfaces.ImagensPixaBay import ImagensPixabay
from QtInterfaces.LimparCache import InterfaceLimparCache
from QtInterfaces.ProjectCreator import InterfaceProjectCreator
from QtInterfaces.Renamer import InterfaceRenamer
from QtInterfaces.S3 import InterfaceS3
from PyQt6.QtGui import QAction

class Tabs(QTabWidget):
    def __init__(self, menubar):  # Passar a instância de MenuBar
        super().__init__()
        self.config = LoadConfigs.Config
        self.data = LoadConfigs.Config.getConfigData("ConfigInterface")

        self.menubar = menubar

        self.closed_tabs = {}

        self.setMovable(True)
        self.setTabsClosable(False)
        self.tabCloseRequested.connect(self.close_tab)
        
        self.janelas = {}
        
        #self.setToolTip("Dica: Você pode clicar com o botão direito e fechar guias não desejadas.\nAlém de poder posicionalas ao seu agrado! :D")
        
        
        abas = {
            "Criar Projeto": {InterfaceProjectCreator.Interface(): self.data["Criar Projeto"]},
            "S3": {InterfaceS3.Interface(): self.data["S3"]},
            "PM3": [],
            "Imagens Pixabay": {ImagensPixabay.Interface(): self.data["Imagens Pixabay"]},
            "Limpar Cache": {InterfaceLimparCache.Interface(): self.data["Limpar Cache"]},
            "Renamer": {InterfaceRenamer.Interface(): self.data["Renamer"]}
        }
        abas_para_fechar = {}
        for nome_aba, valor in abas.items():  # Alterado de dict para valor
            if isinstance(valor, dict):  # Verifica se o valor é um dicionário
                for modulo, ativado in valor.items():
                    if ativado:
                        self.addTab(modulo, nome_aba)
                        self.janelas[nome_aba] = True
                    else:
                        self.janelas[nome_aba] = False
                        abas_para_fechar[nome_aba] = modulo
            else:
                # Aqui você pode adicionar um tratamento para o caso de 'PM3'
                print(f"Valor associado a '{nome_aba}' não é um dicionário: {valor}")
                
        #abas_para_fechar[nome_aba] = modulo
        for nome_aba, modulo in abas_para_fechar.items():
            self.close_tab(self.addTab(modulo,nome_aba))
            
        
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
        self.janelas[tab_name] = False
        self.save()

        existing_action = self.menubar.janelas_submenu.findChild(QAction, tab_name)
        if existing_action is None:
            reopen_action = QAction(tab_name, self)
            reopen_action.triggered.connect(lambda _, name=tab_name: self.reopen_tab(name))
            self.menubar.janelas_submenu.addAction(reopen_action)

    def reopen_tab(self, tab_name):
        if tab_name in self.closed_tabs:
            self.addTab(self.closed_tabs[tab_name], tab_name)
            self.janelas[tab_name] = True
            self.save()
            del self.closed_tabs[tab_name]
            # Remover a ação de reabrir do menu
            actions = self.menubar.janelas_submenu.actions()
            for action in actions:
                if action.text() == tab_name:
                    self.menubar.janelas_submenu.removeAction(action)
                    break
    def save(self):
        dict = {
            "OrdemJanelas": [self.janelas]
        }
        self.config.saveConfigDict("ConfigInterface",self.janelas)
        self.config.Load("ConfigInterface")