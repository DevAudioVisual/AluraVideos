import json
import multiprocessing
import os
from PyQt6.QtCore import pyqtSignal, QObject, QThreadPool
from Models.S3.DownloadWorker import DownloadWorker
from Models.S3.UploadWorker import UploadWorker

class S3Worker(QObject):
    progress_updated = pyqtSignal(int)
    def __init__(self, s3_client, bucket_name, config):
        super().__init__()
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.config = config
        self.thread_pool = QThreadPool()
        max_threads = min(multiprocessing.cpu_count(), 10) 
        self.thread_pool.setMaxThreadCount(max_threads)
        
    def download_folder(self, folder_key, destination_path):
        # Listar todos os objetos na pasta do S3
        objects = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=folder_key)

        # Cria a pasta principal no caminho de destino
        main_folder_name = os.path.basename(folder_key.rstrip('/'))  # Nome da pasta principal
        main_folder_path = os.path.join(destination_path, main_folder_name)

        # Crie a pasta principal se não existir
        os.makedirs(main_folder_path, exist_ok=True)
        print(f"Pasta principal criada: {main_folder_path}")

        for obj in objects.get('Contents', []):
            file_key = obj['Key']
            
            # Caminho relativo para a estrutura local
            relative_path = os.path.relpath(file_key, folder_key)
            file_path = os.path.join(main_folder_path, relative_path)  # Use o caminho da pasta principal

            # Se for um diretório (termina com /), crie a pasta
            if file_key.endswith('/'):
                os.makedirs(file_path, exist_ok=True)  # Cria a pasta se não existir
                print(f"Pasta criada: {file_path}")
            else:
                # Se for um arquivo, faça o download
                print(f"Baixando {file_key} para {file_path}")
                # Crie os diretórios pai se não existirem
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                worker = DownloadWorker(
                    s3_client=self.s3_client,
                    bucket_name=self.bucket_name,
                    file_key=file_key,
                    file_path=file_path,
                    config=self.config,
                    progress_callback=self.progress_updated
                )
                self.thread_pool.start(worker)
                print("######## Threadpool worker")



    def download_file(self, file_key, destination_path):
        # Extrai o nome do arquivo a partir do file_key
        file_name = os.path.basename(file_key)  # Obtém apenas o nome do arquivo
        file_path = os.path.join(destination_path, file_name)  # Constrói o caminho completo para o arquivo

        # Se for um arquivo, faça o download
        print(f"Baixando {file_key} para {file_path}")
        
        # Crie os diretórios pai se não existirem
        os.makedirs(destination_path, exist_ok=True)  # Garante que o diretório de destino exista

        # Iniciar o worker para o download
        worker = DownloadWorker(
            s3_client=self.s3_client,
            bucket_name=self.bucket_name,
            file_key=file_key,
            file_path=file_path,
            config=self.config,
            progress_callback=self.progress_updated
        )
        self.thread_pool.start(worker)
        print("######## Threadpool worker")

        
    def upload_folder(self, local_folder_path, destination_folder):
        folder_name = os.path.basename(local_folder_path)
        destination_folder = destination_folder.rstrip('/')
        s3_destination_folder = f"{destination_folder}/{folder_name}/".replace('\\', '/')

        print("Iniciando o upload")
            
        for root, dirs, files in os.walk(local_folder_path):
          for file in files:
              local_file_path = os.path.join(root, file).replace('\\', '/')
              relative_path = os.path.relpath(local_file_path, local_folder_path)
              s3_key = os.path.join(s3_destination_folder, relative_path).replace('\\', '/')

              worker = UploadWorker(
                  s3_client=self.s3_client,
                  bucket_name=self.bucket_name,
                  local_file_path=local_file_path,
                  s3_key=s3_key,
                  config=self.config,
                  progress_callback=self.progress_updated
              )

              self.thread_pool.start(worker)  # Iniciar o worker aqui

    def upload_file(self, local_file_path, s3_key):
        try:
            # Callback de progresso
            def progress_callback(bytes_amount):
                self.progress_updated.emit(bytes_amount)

            # Fazer o upload do arquivo para o S3
            self.s3_client.upload_file(
                local_file_path, self.bucket_name, s3_key, 
                Callback=progress_callback, Config=self.config
            )

        except Exception as e:
            print(f"Erro ao carregar o arquivo {local_file_path}: {e}")