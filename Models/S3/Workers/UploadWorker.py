from tkinter import messagebox
from PyQt6.QtCore import QRunnable
from PyQt6.QtWidgets import QMessageBox

class UploadWorker(QRunnable):
    def __init__(self, s3_client, bucket_name, local_file_path, s3_key, config, progress_callback=None):
        super().__init__()
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.local_file_path = local_file_path
        self.s3_key = s3_key
        self.config = config
        self.progress_callback = progress_callback

    def run(self):
        # Função para fazer upload do arquivo
        try:
            def progress_callback(bytes_amount):
                # Chama o callback do progresso, se definido
                if self.progress_callback:
                    self.progress_callback.emit(bytes_amount)

            self.s3_client.upload_file(
                self.local_file_path, self.bucket_name, self.s3_key,
                Callback=progress_callback, Config=self.config
            )
            #QMessageBox.information(None, "Sucesso!", f"Upload concluido!\nLocal de acesso: {self.s3_key}")
            #self.progress_dialog.quit()
            print(f"Upload concluído para {self.s3_key}")
            messagebox.showinfo("Sucesso!",f"Upload concluído para {self.s3_key}")
            #QMessageBox.information(None,"Aviso",f"Upload concluído para {self.s3_key}")
        except Exception as e:
            print(f"Erro ao carregar o arquivo {self.local_file_path}: {e}")