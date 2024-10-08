import json
import os
from pathlib import Path
import jwt
from Config import LoadConfigs
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.config import Config
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject, QThread, QTimer
from Models.S3.ProgressDialog import ProgressDialog
from Models.S3.S3Worker import S3Worker

class S3Model(QObject):
    def __init__(self):
        super().__init__() 
        caminho_arquivo = os.path.join(os.path.dirname(__file__), 'keys.json')
        with open(caminho_arquivo, 'r') as f:
            dados = json.load(f)
        self.KEY = str(dados['S3'])
        self.s3_client = None
        self.bucket_name = "equipevideos"
        self.downloaded = False
        self.config = TransferConfig(
            multipart_threshold=1024 * 1024 * 8,
            multipart_chunksize=1024 * 1024 * 8,
            use_threads=True,
            max_io_queue=1000,
        )

    def resetCredentials(self):
        self.s3_client = None
        LoadConfigs.Config.Reset("Credentials", reabrir=False)

    def setS3Client(self):
        try:
            access_key = self.Decode(LoadConfigs.Config.getConfigData("Credentials", "token"))['access_key']
            secret_key = self.Decode(LoadConfigs.Config.getConfigData("Credentials", "token"))['secret_key']
            self.s3_client = boto3.client(
                's3', aws_access_key_id=access_key, aws_secret_access_key=secret_key,
                config=Config(max_pool_connections=20)
            )
            return True
        except Exception as e:
            print(e)
            return False
    def start(self):
        self.progressdialog = ProgressDialog()
        self.progressdialog_thread = QThread()
        self.progressdialog.moveToThread(self.progressdialog_thread)
        self.progressdialog.show()
        self.progressdialog_thread.finished.connect(self.progressdialog_thread.quit)
        self.progressdialog_thread.finished.connect(self.progressdialog_thread.wait)
        
        self.worker = S3Worker(self.s3_client, self.bucket_name, self.config)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.finished.connect(self.worker_thread.quit)
        self.worker_thread.finished.connect(self.worker_thread.wait)

        # Conectar o sinal de progresso do worker à atualização da interface
        self.worker.progress_updated.connect(self.progressdialog.update_progress)
        
    def startDownload(self, folder_key, destination_path, isFolder):
        self.start()
        if isFolder:
            total_size = 0
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=folder_key)
            
            for obj in response.get('Contents', []):
                total_size += obj['Size']  # Soma o tamanho de cada arquivo
            self.progressdialog.setTotal_size(total_size)
            self.worker_thread.started.connect(lambda: self.worker.download_folder(folder_key, destination_path))
            self.worker_thread.start()
        else: 
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=folder_key)
            total_size = response['ContentLength']

            self.progressdialog.setTotal_size(total_size)
            self.worker_thread.started.connect(lambda: self.worker.download_file(folder_key, destination_path))
            self.worker_thread.start()
            
        
    def startUpload(self, local_folder_path, destination_folder):
        self.start()
        total_size = sum(os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(local_folder_path) for file in files)
        self.progressdialog.setTotal_size(total_size)

        print(local_folder_path, destination_folder)
        self.worker_thread.started.connect(lambda: self.worker.upload_folder(local_folder_path, destination_folder))
        self.worker_thread.start()
        
    def update(self):
        if self.progressdialog.get_seen_so_far() >= self.progressdialog.getTotal_size():
            print(f"Upload concluído!")
            self.downloaded = True
            return
        QTimer.singleShot(500, self.update)
        
    def list_s3_objects(self,prefix=''):
        result = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix, Delimiter='/')
        
        folders = []
        files = []

        # Listar pastas
        if 'CommonPrefixes' in result:
            for obj in result['CommonPrefixes']:
                folders.append(obj.get('Prefix'))

        # Listar arquivos
        if 'Contents' in result:
            for obj in result['Contents']:
                if obj['Key'] != prefix:  # Ignorar o próprio prefixo
                    files.append(obj['Key'])

        return folders, files

    def list_folders_s3(self, sort=False):
        folder_names = []
        paginator = self.s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=self.bucket_name, Delimiter='/'):
            if 'CommonPrefixes' in page:
                for prefix in page['CommonPrefixes']:
                    folder_names.append(prefix['Prefix'].rstrip('/'))

        return folder_names if not sort else sorted(folder_names)

    def registerCredentials(self, secret_key, access_key):
        if not self.ValidateCredentials(access_key=access_key, secret_key=secret_key):
            QMessageBox.information(None, "Aviso", "Credenciais inválidas")
            return False
        else:
            self.Encode(access_key=access_key, secret_key=secret_key)
            QMessageBox.information(None, "Sucesso!", "Credenciais válidas e registradas com sucesso!")
            LoadConfigs.Config.Load(config="Credentials")
            self.setS3Client()
            return True

    def ValidateCredentials(self, secret_key, access_key):
        try:
            self.s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
            self.s3_client.list_buckets()
            return True
        except Exception as e:
            print(e)
            return False

    def hasToken(self):
        return LoadConfigs.Config.getConfigData("Credentials", "token") != ""

    def Encode(self, access_key, secret_key):
        payload = {
            "secret_key": secret_key,
            "access_key": access_key
        }
        token = jwt.encode(payload, self.KEY, algorithm="HS256")
        token_dict = {"token": token}
        LoadConfigs.Config.saveConfigDict("Credentials", token_dict)

    def Decode(self, token):
        return jwt.decode(token, self.KEY, algorithms=["HS256"])
    
    


