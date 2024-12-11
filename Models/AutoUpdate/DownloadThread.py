import os
import tempfile
from PyQt6.QtCore import QThread, pyqtSignal
import requests

from Util import Util

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