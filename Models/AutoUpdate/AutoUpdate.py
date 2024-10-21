import re
import requests
import os
import tempfile
import subprocess
import time
from packaging import version
from Util import Tokens, Util
from PyQt6.QtCore import QThread, pyqtSignal,QCoreApplication,Qt
from PyQt6.QtWidgets import QMessageBox, QProgressDialog


class DownloadThread(QThread):
    download_finished = pyqtSignal(bool)
    download_progress = pyqtSignal(int)  # Novo sinal para o progresso
    dirtemp = pyqtSignal(str)

    def __init__(self, app_instance):
        super().__init__()
        self.app_instance = app_instance

    def run(self):
        try:
            # Movendo a lógica de download_latest_release para cá
            exe_asset = next(
                (asset for asset in self.app_instance.release_data["assets"] if asset["name"].endswith(".exe")), None
            )
            if not exe_asset:
                print(f"Nenhum arquivo .exe encontrado na release {self.app_instance.latest_tag_name}")
                self.download_finished.emit(False)  # Emite sinal de erro
                return

            exe_url = exe_asset["browser_download_url"]
            exe_size = exe_asset["size"]
            chunk_size = 8192

            with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as temp_exe:
                temp_exe_path = temp_exe.name
                print(f"Baixando {exe_asset['name']}...")

                response = requests.get(exe_url, stream=True)
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0

                with open(temp_exe_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            progress = int(100 * downloaded_size / total_size)
                            self.download_progress.emit(progress)  # Emite o progresso

                downloaded_size = os.path.getsize(temp_exe_path)
                temp_exe_path = os.path.normpath(temp_exe_path)
                if downloaded_size == exe_size:
                    print(f"Download de {exe_asset['name']} concluído com sucesso!")
                    #time.sleep(5)
                    #subprocess.run([temp_exe_path, "/runas"], shell=True)
                    self.download_finished.emit(True)  # Emite sinal de sucesso
                    self.dirtemp.emit(temp_exe_path)
                else:
                    print(f"Erro: Tamanho do arquivo baixado não corresponde ao esperado.")
                    self.download_finished.emit(False)  # Emite sinal de erro
        except Exception as e:
            Util.LogError(func="DownloadThread", mensagem=f"Erro no download: {e}")
            self.download_finished.emit(False)  # Emite sinal de erro

class app():
    def __init__(self):
        self.repo_owner = "DevAudioVisual"
        self.repo_name = "AluraVideos"
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        self.headers = {"Authorization": f"Bearer {Tokens.GITHUB}","Accept": "application/vnd.github+json"}
        self.current_version = version.parse(Util.version.lstrip("V"))  # Certifique-se de que Util.version esteja definido

        self.response = None
        self.release_data = None
        self.latest_tag_name = None
        self.release_notes = None
        self.release_version = None
        self.progress_dialog = None

    def initRequest(self):
        try:
            print("Verificando atualizações...")
            self.response = requests.get(self.api_url, headers=self.headers)
            self.response.raise_for_status()
            self.release_data = self.response.json()
            self.latest_tag_name = self.release_data["tag_name"]
            self.release_notes = self.release_data["body"]
            self.release_version = version.parse(self.latest_tag_name.lstrip("V"))
            print(f"Versão atual: {self.current_version} Ultima versão disponíveL: {self.release_version}")
        except requests.exceptions.RequestException as e:
            Util.LogError(func="Atualizações", mensagem=f"Erro ao buscar por atualizações: {e}")

    def download_file(self, url, file_path, chunk_size=8192, max_retries=5, retry_delay=1):
        for attempt in range(max_retries):
            try:
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                break
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))
                    print(f"Erro no download: {e}. Tentando novamente em {retry_delay * (2 ** attempt)} segundos...")
                else:
                    raise

    def check_updates(self):
        self.initRequest()
        if self.release_version > self.current_version:
            print("Atualização disponível")
            padrao = r'^(#{1,6})\s'
            texto_sem_formatacao = re.sub(padrao, '', f"Atualização para a versão {self.release_version} disponível.\n\nNotas de atualização:\n{self.release_notes.replace('- ', '\n-')}", flags=re.MULTILINE)
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Question)
            msg_box.setWindowTitle("Atualização")
            msg_box.setText(texto_sem_formatacao)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.setDefaultButton(QMessageBox.StandardButton.Yes)
            ret = msg_box.exec()
            msg_box.activateWindow()
            msg_box.raise_()
            if ret == QMessageBox.StandardButton.Yes:
                self.download_thread = DownloadThread(self)
                self.download_thread.download_finished.connect(self.download_finished)
                self.download_thread.download_progress.connect(self.update_download_progress)  # Conecta o sinal
                self.download_thread.dirtemp.connect(self.dirtemp)
                
                self.progress_dialog = QProgressDialog("Baixando atualização...", "Cancelar", 0, 100)
                self.progress_dialog.setWindowTitle("Progresso do Download")
                self.progress_dialog.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
             
                self.progress_dialog.show()
                self.progress_dialog.activateWindow()
                self.progress_dialog.raise_()

                self.download_thread.start()
            return True
        else:
            print("Você está atualizado!")
            return False
    def dirtemp(self, str):
        self.dirtemp = str
        
    def download_finished(self, success):
        if success:
            QMessageBox.information(None, "Info", "Download concluído!\nO aplicativo será fechado para que a atualização seja instalada.")
            QCoreApplication.instance().quit()
            subprocess.run(self.dirtemp,shell=True)  # Execute o arquivo após o download (opcional)
            #QThread.msleep(5000)
        else:
            QMessageBox.critical(None, "Erro", "O download falhou.")
    
    def update_download_progress(self, progress):
        if self.progress_dialog:
            self.progress_dialog.setValue(progress)