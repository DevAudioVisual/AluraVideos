from PyQt6.QtCore import Qt
import Util.CustomWidgets as cw

class ProgressDialog(cw.Widget):
    def __init__(self, projeto):
        super().__init__()
        layout = cw.GridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.setContentsMargins(10, 20, 10, 10)

        self.titulo = cw.Label(f"Aguarde! Estou criando o projeto:<br><font face='Helvetica'>{projeto}</font>")
        self.titulo.setObjectName("grande")
        self.subtitulo = cw.Label("Etapa atual: carregando")
        self.subtitulo.setObjectName("medio")

        self.progress_bar = cw.ProgressBar()
        self.progress_bar.setValue(0)

        layout.addWidget(self.titulo,0,0)
        layout.addWidget(self.subtitulo,1,0)
        layout.addWidget(self.progress_bar,2,0)

        self.setLayout(layout)

    def update_progress(self, audio_progress, descompacted_progress):
        progresso_total = (audio_progress + descompacted_progress) // 2
        self.progress_bar.setValue(progresso_total)
        if audio_progress == 0:
            etapa = "Descompactando vídeos"
        else:
            etapa = "Extraindo áudios"
        self.subtitulo.setText(f"Etapa atual: {etapa}")