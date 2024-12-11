import Util.CustomWidgets as cw
from PyQt6.QtCore import Qt

class ProgressWidget(cw.Widget):
    def __init__(self, projeto):
        super().__init__()

        layout = cw.GridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.setContentsMargins(10, 20, 10, 10)

        self.titulo = cw.Label(f"Aguarde! Estou criando o projeto:<br><font face='Helvetica'>{projeto}</font>")
        self.titulo.setWordWrap(True)
        self.titulo.setObjectName("grande")
        self.subtitulo = cw.Label("Etapa atual: Fazendo download")
        self.subtitulo.setObjectName("medio")

        self.velocidade_download = cw.Label("Velocidade: Calculando...")
        self.tempo_restante = cw.Label("Tempo Restante: Calculando...")
        self.total_baixado = cw.Label("Tamanho do Arquivo: Calculando...")

        layout.addWidget(self.titulo,1,0)
        layout.addWidget(self.subtitulo,2,0)
        layout.addWidget(self.velocidade_download,3,0)
        layout.addWidget(self.tempo_restante,4,0)
        layout.addWidget(self.total_baixado,5,0)

        self.progress_bar = cw.ProgressBar()
        self.progress_bar.setValue(0)  # Inicializa a barra de progresso em 0
        layout.addWidget(self.progress_bar,6,0)

        self.setLayout(layout)

    def update_progress(self, progress, velocidade, tempo_restante, total_baixado):
        self.progress_bar.setValue(progress)
        self.velocidade_download.setText(f"Velocidade: {velocidade}/s")
        self.tempo_restante.setText(f"Tempo Restante: {tempo_restante}")
        self.total_baixado.setText(f"Tamanho do Arquivo: {total_baixado}")