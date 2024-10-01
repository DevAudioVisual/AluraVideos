import json
import multiprocessing
import os
import time
import jwt
from Config import LoadConfigs
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.config import Config
from PyQt6.QtWidgets import QLabel, QDialog, QVBoxLayout, QProgressBar, QMessageBox
from PyQt6.QtCore import pyqtSignal, QObject, QThread, QTimer, QThreadPool,QRunnable

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