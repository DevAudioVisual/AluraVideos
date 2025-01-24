import mimetypes
import os
import requests
import time
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from PyQt6.QtCore import QThread, pyqtSignal

from Models.VideoUploader import UploaderTokenManager

class UploadWorker(QThread):
    progress_signal = pyqtSignal(str, float, str)
    finished_signal = pyqtSignal(str, str)
    error_signal = pyqtSignal(str)

    def __init__(self, showcase_id, file_path, max_retries=3):
        super().__init__()
        self.showcase_id = showcase_id
        self.file_path = file_path
        self.max_retries = max_retries

    def run(self):
        
        print("Iniciando upload do video:", self.file_path)

        self.progress_counter = 0
        
        url = "https://video-uploader.alura.com.br/api/video/upload"

        headers = {
            "X-API-TOKEN": UploaderTokenManager.token()
        }

        file_name = os.path.basename(self.file_path)
        mime_type, _ = mimetypes.guess_type(self.file_path)

        start_time = None
        last_bytes_read = 0
        last_time = None

        def progress_callback(monitor):
            nonlocal start_time, last_bytes_read, last_time

            if start_time is None:
                start_time = time.time()
                last_time = start_time

            elapsed_time = time.time() - last_time
            bytes_transferred = monitor.bytes_read - last_bytes_read
            speed = bytes_transferred / elapsed_time if elapsed_time > 0 else 0

            remaining_bytes = monitor.len - monitor.bytes_read
            remaining_time = remaining_bytes / speed if speed > 0 else 0

            percent = (monitor.bytes_read / monitor.len) * 100

            # Formata a velocidade em GB/MB/KB
            speed_kb = speed / 1024
            speed_mb = speed_kb / 1024
            speed_gb = speed_mb / 1024
            if speed_gb >= 1:
                speed_str = f"{speed_gb:.2f} GB/s"
            elif speed_mb >= 1:
                speed_str = f"{speed_mb:.2f} MB/s"
            else:
                speed_str = f"{speed_kb:.2f} KB/s"
                
            horas, minutos, segundos = converte_segundos(int(f"{round(remaining_time)}"))
            remaining_time = f"{horas}h {minutos}m {segundos}s"

            self.progress_counter += 1
            if self.progress_counter >= 200:  # Emite o sinal a cada 10 chamadas
                self.progress_signal.emit(self.file_path, percent, remaining_time)
                self.progress_counter = 0  # Reinicia o contador
                print(f"Progresso: {percent:.2f}% - Velocidade: {speed_str} - Tempo restante: {remaining_time}",end="\r")

            last_bytes_read = monitor.bytes_read
            last_time = time.time()

        try:
            with open(self.file_path, 'rb') as file:
                encoder = MultipartEncoder(
                    fields={
                        'showcase': str(self.showcase_id),
                        'file': (file_name, file, mime_type)
                    }
                )
                monitor = MultipartEncoderMonitor(encoder, progress_callback)
                headers['Content-Type'] = monitor.content_type
                response = requests.post(url, headers=headers, data=monitor)
                response.raise_for_status()

                video_id = response.json()['uuid']
                self.finished_signal.emit(self.file_path, video_id)       

        except requests.exceptions.RequestException as e:
            self.error_signal.emit(self.file_path)
        except (IndexError, KeyError, AttributeError) as e:
            self.error_signal.emit(self.file_path)

            
def converte_segundos(segundos):
  horas = segundos // 3600
  segundos %= 3600
  minutos = segundos // 60
  segundos %= 60
  return horas, minutos, segundos