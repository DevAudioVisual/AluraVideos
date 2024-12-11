import time
from PyQt6.QtWidgets import QLabel, QDialog, QVBoxLayout, QProgressBar, QMessageBox
from Util import Util

class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Progresso")

        layout = QVBoxLayout()

        self.velocidade_download = QLabel("Velocidade: Calculando...")
        self.tempo_restante = QLabel("Tempo Restante: Calculando...")
        self.total_baixado = QLabel("Tamanho do Arquivo: Calculando...")

        layout.addWidget(self.velocidade_download)
        layout.addWidget(self.tempo_restante)
        layout.addWidget(self.total_baixado)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)  # Inicializa a barra de progresso em 0
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        self.start_time = None
        self._seen_so_far = 0
        self.total_size = 0

    def setTotal_size(self, total_size):
        self.total_size = total_size

    def update_progress(self, bytes_amount):
        if self.start_time is None:
            self.start_time = time.time()

        self._seen_so_far += bytes_amount
        progress = (self._seen_so_far / self.total_size) * 100 if self.total_size > 0 else 100

        elapsed_time = time.time() - self.start_time
        remaining_time = (elapsed_time / progress) * (100 - progress) if progress > 0 else 0

        speed = self._seen_so_far / elapsed_time if elapsed_time > 0 else 0

        # Atualizar interface
        self.progress_bar.setValue(int(progress))
        self.velocidade_download.setText(f"Velocidade: {Util.format_size(speed)}/s")
        self.tempo_restante.setText(f"Tempo Restante: {time.strftime('%H:%M:%S', time.gmtime(remaining_time))}")
        self.total_baixado.setText(f"Tamanho do Arquivo: {Util.format_size(self._seen_so_far)} / {Util.format_size(self.total_size)}")
        
        if progress >= 100:
            QMessageBox.information(None,"Sucesso!","Processo concluido com exito.")
            self.close()