from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from Config import LoadConfigs
from WebSocket import WebSocket
import Util.CustomWidgets as cw
global Config

versao_effector = None
versao_ordinem = None
versao_notabillity = None

notes_effector = None
notes_ordinem = None
notes_notability = None

class LoadingScreen(cw.Widget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.FramelessWindowHint)
        
        layout = cw.VBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        self.label = cw.Label('Carregando Aluravideos')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.timer.start(500)  # Atualiza a cada 500 milissegundos
        self.counter = 0
        
        self.etapa = cw.Label('Etapa atual: ')
        self.etapa.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progressBar = cw.ProgressBar()
        self.progressBar.setValue(0)
        
        layout.addWidget(self.label)
        layout.addWidget(self.etapa)
        layout.addWidget(self.progressBar)
        
    def update_text(self):
        self.counter += 1
        if self.counter > 3:
            self.counter = 0
        ponto = "." * self.counter
        self.label.setText(f"Carregando Aluravideos{ponto}")
    
    def update_etapa(self, etapa):
        self.etapa.setText(f"Etapa atual: {etapa}")
    def update_progress(self, value):
        self.progressBar.setValue(value)
        
class LoadingThread(QThread):
    progress_updated = pyqtSignal(int)
    etapa = pyqtSignal(str)
    execute_in_main_thread = pyqtSignal(object) 
    execute_in_main_thread2 = pyqtSignal(object) 
    def __init__(self):
        super().__init__()
        self.processos = [
            #self.carregar_web_socket,
            self.carregar_configs,
            self.verificar_atualizacoes,
            #self.carregar_atalhos,
            #self.versoes_extensões_ppro
            self.carregar_tensorflow,
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
            
    def carregar_web_socket(self):
        self.etapa.emit("Iniciando Web Sockets")
        WebSocket.startServer()
        #QThread.msleep(500)
        
    def carregar_configs(self):
        self.etapa.emit("Carregando configurações")
        LoadConfigs.Config = LoadConfigs.Configs()
        LoadConfigs.Config.firtLoad()  # Corrigido: firstLoad
        #QThread.msleep(500)

    def carregar_tensorflow(self):
        self.etapa.emit("Inicializando TensorFlow")
        import tensorflow
        #QThread.msleep(500)

    def verificar_atualizacoes(self):
        self.etapa.emit("Buscando por atualizações")
        self.execute_in_main_thread.emit(self.verificar_atualizacoes) 
        #QThread.msleep(500)
        

        