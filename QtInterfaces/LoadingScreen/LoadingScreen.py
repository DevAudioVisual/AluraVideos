from PyQt6.QtWidgets import QWidget, QLabel, QProgressBar,QVBoxLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from Config import LoadConfigs
from Models.Updates import VerificarAtualizações

global Config

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.FramelessWindowHint)
        
        #self.setStyleSheet("background-color: transparent;")
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        self.label = QLabel('Carregando Aluravideos...')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        
        layout.addWidget(self.label)
        layout.addWidget(self.progressBar)

    def update_progress(self, value):
        self.progressBar.setValue(value)
        
        
class LoadingThread(QThread):
    progress_updated = pyqtSignal(int)
        
    def run(self):
        total_steps = 2  # Adapte para o número real de etapas

        LoadConfigs.Config = LoadConfigs.Configs()
        LoadConfigs.Config.firtLoad()
        progress = int(1 / total_steps * 100)  # 50% concluído
        self.progress_updated.emit(progress)
        
        QThread.msleep(500)

        # Verificação de atualizações
        progress = int(2 / total_steps * 100)  # 100% concluído
        self.progress_updated.emit(progress)
        VerificarAtualizações.app()