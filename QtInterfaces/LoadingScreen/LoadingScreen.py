from PyQt6.QtWidgets import QWidget, QLabel, QProgressBar,QVBoxLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from Config import LoadConfigs
from Models.AutoUpdate import AutoUpdate
global Config

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.FramelessWindowHint)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        self.label = QLabel('Carregando Aluravideos...')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.etapa = QLabel('Etapa atual: ')
        self.etapa.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        
        layout.addWidget(self.label)
        layout.addWidget(self.etapa)
        layout.addWidget(self.progressBar)
        
    def update_etapa(self, etapa):
        self.etapa.setText(f"Etapa atual: {etapa}")
    def update_progress(self, value):
        self.progressBar.setValue(value)
        
class LoadingThread(QThread):
    progress_updated = pyqtSignal(int)
    etapa = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.processos = [
            self.carregar_configs,
            #self.verificar_atualizacoes
        ]
        
    def run(self):
        total_steps = len(self.processos)
        for i, processo in enumerate(self.processos):
            progress = int((i + 1) / total_steps * 100)
            self.progress_updated.emit(progress)
            processo()

    def carregar_configs(self):
        self.etapa.emit("Carregando configurações")
        LoadConfigs.Config = LoadConfigs.Configs()
        LoadConfigs.Config.firtLoad()  # Corrigido: firstLoad
        QThread.msleep(500)

    def verificar_atualizacoes(self):
        self.etapa.emit("Buscando por atualizações")
        AutoUpdate.app().check_updates()
        QThread.msleep(500)
    

        