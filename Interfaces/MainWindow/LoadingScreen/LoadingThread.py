from PyQt6.QtCore import QThread, pyqtSignal
from Config import LoadConfigs
from Util import Tokens
global Config

class LoadingThread(QThread):
    progress_updated = pyqtSignal(int)
    etapa = pyqtSignal(str)
    execute_in_main_thread = pyqtSignal(object) 
    execute_in_main_thread2 = pyqtSignal(object) 
    def __init__(self):
        super().__init__()
        self.processos = [
            self.carregar_configs,
            #self.carregar_web_socket,
            #self.carregar_atalhos,
            #self.versoes_extensões_ppro
            #self.carregar_tensorflow,
            self.validar_credenciais,
            self.verificar_atualizacoes,
        ]
        
    def run(self):
        total_steps = len(self.processos)
        for i, processo in enumerate(self.processos):
            progress = int((i + 1) / total_steps * 100)
            processo()
            self.progress_updated.emit(progress)
    def carregar_atalhos(self):
        self.etapa.emit("Carregando teclas de atalho")
        self.execute_in_main_thread2.emit(self.carregar_atalhos) 
        #QThread.msleep(500)
        
    def carregar_configs(self):
        self.etapa.emit("Carregando configurações")
        LoadConfigs.Config = LoadConfigs.Configs()
        LoadConfigs.Config.firtLoad()  # Corrigido: firstLoad
        #QThread.msleep(500)

    def carregar_tensorflow(self):
        config = LoadConfigs.Config
        data = config.getConfigData("ConfigInterface")["Janelas"]["VideoValidator"][0]
        if data:
            self.etapa.emit("Inicializando TensorFlow")
            #import tensorflow
        QThread.msleep(500)

    def verificar_atualizacoes(self):
        if Tokens.GITHUB != None: 
            self.etapa.emit("Buscando por atualizações")
            self.execute_in_main_thread.emit(self.verificar_atualizacoes) 
        #QThread.msleep(500)
    
    def validar_credenciais(self):
        self.etapa.emit("Validando credenciais de acesso")
        Tokens.LoadKeys()