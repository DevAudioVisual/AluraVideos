from PyQt6.QtCore import QRunnable

class DownloadWorker(QRunnable):
    def __init__(self, s3_client, bucket_name, file_key, file_path, config, progress_callback=None):
        super().__init__()
        self.s3_client = s3_client
        self.file_key = file_key
        self.bucket_name = bucket_name
        self.file_path = file_path
        self.config = config
        self.progress_callback = progress_callback

    def run(self):
        # Função para fazer upload do arquivo
        print(f"Bucket Name: {self.bucket_name}")
        print(f"File Key: {self.file_key}")
        print(f"File Path: {self.file_path}")
        
        print(f"Baixando {self.file_key} para {self.file_path}")
        
        try:
            def progress_callback(bytes_amount):
                # Chama o callback do progresso, se definido
                if self.progress_callback:
                    self.progress_callback.emit(bytes_amount)
            self.s3_client.download_file(self.bucket_name, self.file_key, self.file_path, Callback=progress_callback, Config = self.config)
            print(f"Download concluído para {self.file_key}")
        except Exception as e:
            print(f"Erro ao baixar o arquivo {self.file_key}: {e}")     