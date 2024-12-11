import os
import subprocess
import zipfile
import patoolib
from Util import Util
from PyQt6.QtCore import QTimer, QThread, QObject, pyqtSignal
from Models.CriarProjeto.Descompactador.Worker import Worker
from Models.CriarProjeto.Descompactador.ProgressDialog import ProgressDialog

class Descompact(QObject):
    progress_signal = pyqtSignal(int, int)  # Para comunicar o progresso

    def __init__(self, projeto):
        super().__init__()
        self.projeto = projeto
        self.arquivo_entrada = None
        self.diretorio_saida = None
        self.descompacted = False
        self.novo_caminho_completo = None
        self.patoolprogress = 0
        self.audioprogress = 0
        self.total_zip = 0
        self.progress = ProgressDialog(projeto=self.projeto)  # Janela de progresso
        self.progress_signal.connect(self.progress.update_progress)

        # Timer para atualizar a interface
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.updateInterface)

    def start(self, arquivo_entrada, diretorio_saida, stackedwidget):
        self.stackedwidget = stackedwidget
        self.stackedwidget.addWidget(self.progress)
        self.stackedwidget.setCurrentWidget(self.progress)
        self.arquivo_entrada = arquivo_entrada
        self.diretorio_saida = diretorio_saida
        self.limpar_texto()
        zip_file = zipfile.ZipFile(self.novo_caminho_completo)
        self.total_zip = len(zip_file.infolist())

        # Criar a thread para o processamento pesado
        self.worker_thread = QThread()
        self.worker = Worker(self)  # Passa o objeto Descompact para o Worker
        self.worker.moveToThread(self.worker_thread)

        # Conectar os sinais e slots
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.finish)
        self.worker.progress_signal.connect(self.progress.update_progress)

        # Iniciar a thread de trabalho pesado
        self.worker_thread.start()

        # Exibir o progresso
        self.progress.show()

        # Iniciar o timer da interface para atualização regular do progresso
        self.update_timer.start(500)

    def finish(self):

        num_widgets = self.stackedwidget.count()
        if num_widgets > 1:
            for i in range(1, num_widgets):
                self.stackedwidget.removeWidget(self.stackedwidget.widget(1))  # Remove sempre o índice 1
        self.stackedwidget.setCurrentIndex(0)
        
        # Finalizar a thread e parar o timer
        self.worker_thread.quit()
        self.worker_thread.wait()
        self.update_timer.stop()
        self.progress.close()

    def updateInterface(self):
        if self.descompacted:
            self.audioprogress = 100
            self.emitprogress()
            self.finish()
            return

        total_videos = sum(1 for filename in os.listdir(self.diretorio_saida) if filename.endswith(('.mp4', '.avi', '.mkv', '.mov')))
        if total_videos >= (self.total_zip - 1):
            self.patoolprogress = 100
        else:
            self.patoolprogress = int((total_videos / self.total_zip) * 100) if self.total_zip > 0 else 0

        self.emitprogress()

    def emitprogress(self):
        self.progress_signal.emit(self.audioprogress, self.patoolprogress)

    def converter_e_extrair(self):
        self.converter_zip_rar()
        self.extractAudios()

    def converter_zip_rar(self):
        try:     
            patoolib.extract_archive(self.novo_caminho_completo, outdir=self.diretorio_saida)
            os.remove(self.novo_caminho_completo)
        except patoolib.util.PatoolError as e:
            if isinstance(e, UnicodeDecodeError):
                Util.LogError("Descompactador", f"Erro de codificação no arquivo '{self.arquivo_entrada}'. Tente renomear o arquivo manualmente ou usar outro programa para descompactar.")
            else:
                Util.LogError("Descompactador", f"Erro ao converter o arquivo '{self.arquivo_entrada}': {e}")
        except Exception as ex:
            Util.LogError("Descompactador", f"Erro inesperado: {ex}")

    def extractAudios(self):
        total_videos = sum(1 for filename in os.listdir(self.diretorio_saida) if filename.endswith(('.mp4', '.avi', '.mkv', '.mov')))
        audios_extraidos = 0    
        diretorio_audio = os.path.dirname(self.diretorio_saida)
        diretorio_audio2 = os.path.join(diretorio_audio, "02_Audio")      

        for filename in os.listdir(self.diretorio_saida):
            if filename.endswith(('.mp4', '.avi', '.mkv', '.mov')):
                video_path = os.path.join(self.diretorio_saida, filename)
                video_path2 = os.path.normpath(video_path)
                audio_filename = os.path.splitext(filename)[0] + '.wav'
                audio_path = os.path.join(diretorio_audio2, audio_filename)
                audio_path2 = os.path.normpath(audio_path)

                command = f'{Util.pegarFFMPEG()} -loglevel quiet -i "{video_path2}" "{audio_path2}"'

                try:
                    subprocess.run(command, shell=True, check=True)
                    audios_extraidos += 1           
                    self.audioprogress = int((audios_extraidos / total_videos) * 100)
                    if self.audioprogress >= 99:
                        self.descompacted = True
                except subprocess.CalledProcessError as e:
                    Util.LogError("Descompactador", f'Erro ao extrair áudio de "{filename}": {e}')

    def limpar_texto(self):     
        try: 
            self.arquivo_entrada = os.path.normpath(self.arquivo_entrada)
            self.diretorio_saida = os.path.normpath(self.diretorio_saida)
            self.novo_caminho_completo = os.path.join(self.diretorio_saida, "arquivovideos.zip")
            os.rename(self.arquivo_entrada, self.novo_caminho_completo)
        except Exception as e:
            Util.LogError("LimparTextoDescompactador", f"Ocorreu um erro ao normalizar o arquivo: {e}", True)






