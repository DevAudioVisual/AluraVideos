import time
import zipfile
import requests
import os
from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout, QProgressBar
from PyQt6.QtCore import pyqtSignal, QObject,QThread,QTimer, Qt

from Util import Util

class DownloadDropApp(QObject):
    progress_updated = pyqtSignal(int, str, str, str)

    def __init__(self, url, extract_folder_path,stackedwidget, projeto):
        super().__init__() 
        self.stackedwidget = stackedwidget
        self.projeto = projeto
        self.extract_folder_path = extract_folder_path
        self.zip_file = None
        self.url = self.convert_link(url)
        self.downloaded = False
        self.erroCorrompido = False
        self.erroTentativas = False

        self.velocidade = 0
        self.tempo_restante = 0
        self.downloaded_size = 0
        self.progress = 0
        self.total_size = 0

        self.progressdialog = ProgressWidget(projeto=projeto)
        self.stackedwidget.addWidget(self.progressdialog)
        self.stackedwidget.setCurrentWidget(self.progressdialog)
        self.progress_updated.connect(self.progressdialog.update_progress)

    def startDownload(self):
        self.download_thread = QThread()
        self.moveToThread(self.download_thread)
        self.download_thread.started.connect(self.Download)
        self.download_thread.start()

        def update():
            self.emit_progress_update()
            if self.downloaded == True:
                self.update_thread.quit()
                self.update_thread.wait()
                return
            QTimer.singleShot(1000,update)
        self.update_thread = QThread()
        self.update_thread.started.connect(update)
        self.update_thread.start()

    def Download(self, chunk_size=8 * 1024 * 1024):
        if not self.url.startswith('https://www.dropbox.com'):
            #messagebox.showerror("Error","Link do dropbox inválido ou comprometido.")
            return

        filename = "arquivo_videos.zip"
        folderpath = os.path.join(self.extract_folder_path)
        os.makedirs(folderpath, exist_ok=True)
        filepath = os.path.join(folderpath, filename)

        retries = 0
        max_retries = 3
        retry_delay = 5

        start_time = time.time()

        while retries < max_retries:
            try:
                response = requests.get(self.url, stream=True, allow_redirects=True)
                self.total_size = int(response.headers.get('content-length', 0))
                self.downloaded_size = 0
                with open(filepath, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size): 
                        size = file.write(data)
                        self.downloaded_size += size
                        self.progress = (self.downloaded_size / self.total_size) * 100
                        self.elapsed_time = time.time() - start_time
                        self.velocidade = (self.downloaded_size / self.elapsed_time) 
                        self.tempo_restante = ((self.total_size - self.downloaded_size) / self.velocidade) if self.velocidade > 0 else 0

                self.zip_file = filepath
                if not self.check_zip_integrity(filepath):
                    print("Arquivo zip corrompido.")
                    Util.LogError("DropDownloader","Arquivo zip corrompido.")
                    self.erroCorrompido = True
                    num_widgets = self.stackedwidget.count()
                    if num_widgets > 1:
                        for i in range(1, num_widgets):
                            self.stackedwidget.removeWidget(self.stackedwidget.widget(1))  # Remove sempre o índice 1
                    self.stackedwidget.setCurrentIndex(0)
                    break
                else:
                    self.downloaded = True
                    break

            except requests.exceptions.RequestException as e:
                retries += 1
                print(f"Erro no download (tentativa {retries}/{max_retries}): {e}")
                if retries < max_retries:
                    print(f"Tentando novamente em {retry_delay} segundos...")
                    time.sleep(retry_delay)
                else:
                    Util.LogError("DropDownloader","Número máximo de tentativas atingido. Download falhou.")
                    self.erroTentativas = True
                    print("Número máximo de tentativas atingido. Download falhou.")
                    num_widgets = self.stackedwidget.count()
                    if num_widgets > 1:
                        for i in range(1, num_widgets):
                            self.stackedwidget.removeWidget(self.stackedwidget.widget(1))  # Remove sempre o índice 1
                    self.stackedwidget.setCurrentIndex(0)
                    break

        self.download_thread.quit()
        self.download_thread.wait()

        # Encerra a thread de atualização da interface
        #self.update_timer.stop()
        self.update_thread.quit()
        self.update_thread.wait()

    def emit_progress_update(self):
        """
        Emite o sinal de atualização de progresso com os valores atuais.
        """
        self.progress_updated.emit(
            int(self.progress),
            self.format_size(self.velocidade),
            time.strftime('%H:%M:%S', time.gmtime(self.tempo_restante)),
            f"{self.format_size(self.downloaded_size)} / {self.format_size(self.total_size)}"
        )
                    
    def convert_link(self,url):
        if "dl=0" in url:
            return url.replace("dl=0", "dl=1")
        return url
    
    def check_zip_integrity(self,filename):
        try:
            with zipfile.ZipFile(filename) as zf:
                zf.testzip()
            return True
        except zipfile.BadZipFile:
            return False
    def format_size(self, size):
        if size >= 1024**3:  # GB
            return f"{size / (1024**3):.2f} GB"
        elif size >= 1024**2:  # MB
            return f"{size / (1024**2):.2f} MB"
        elif size >= 1024:  # KB
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size:.2f} bytes"
        
def quebrar_texto(texto, limite):
    resultado = ""
    contador = 0
    
    for i, caractere in enumerate(texto):
        resultado += caractere
        contador += 1
        
        # Quando o limite é atingido
        if contador == limite:
            resultado += "<br>"   # Quebra normal
            contador = 0  # Reinicia o contador para a próxima linha
    
    return resultado
class ProgressWidget(QWidget):
    def __init__(self, projeto):
        super().__init__()

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.setContentsMargins(10, 20, 10, 10)

        self.titulo = QLabel(f"Aguarde! Estou criando o projeto:<br><font face='Helvetica'>{projeto}</font>")
        self.titulo.setWordWrap(True)
        self.titulo.setObjectName("grande")
        self.subtitulo = QLabel("Etapa atual: Fazendo download")
        self.subtitulo.setObjectName("medio")

        self.velocidade_download = QLabel("Velocidade: Calculando...")
        self.tempo_restante = QLabel("Tempo Restante: Calculando...")
        self.total_baixado = QLabel("Tamanho do Arquivo: Calculando...")

        layout.addWidget(self.titulo,1,0)
        layout.addWidget(self.subtitulo,2,0)
        layout.addWidget(self.velocidade_download,3,0)
        layout.addWidget(self.tempo_restante,4,0)
        layout.addWidget(self.total_baixado,5,0)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)  # Inicializa a barra de progresso em 0
        layout.addWidget(self.progress_bar,6,0)

        self.setLayout(layout)

    def update_progress(self, progress, velocidade, tempo_restante, total_baixado):
        self.progress_bar.setValue(progress)
        self.velocidade_download.setText(f"Velocidade: {velocidade}/s")
        self.tempo_restante.setText(f"Tempo Restante: {tempo_restante}")
        self.total_baixado.setText(f"Tamanho do Arquivo: {total_baixado}")


