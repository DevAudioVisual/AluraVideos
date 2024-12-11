from PyQt6.QtCore import QObject, pyqtSignal

class Worker(QObject):
    # Sinais para comunicação
    progress_signal = pyqtSignal(int, int)
    finished = pyqtSignal()

    def __init__(self, descompact_obj):
        super().__init__()
        self.descompact_obj = descompact_obj

    def run(self):
        # Executa o processo pesado de descompactação e extração
        self.descompact_obj.converter_e_extrair()
        self.finished.emit()  # Emite sinal de finalização