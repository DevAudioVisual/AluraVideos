import json
import os
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
        self.KEY = str(os.environ.get('S3_KEY'))
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

    def start(self, local_folder_path, destination_folder):
        total_size = sum(os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(local_folder_path) for file in files)
        self.progressdialog = ProgressDialog()
        self.progressdialog_thread = QThread()
        self.progressdialog.moveToThread(self.progressdialog_thread)
        self.progressdialog.setTotal_size(total_size)
        self.progressdialog.show()
        

        # Criar e configurar o worker para upload
        self.worker = S3Worker(self.s3_client, self.bucket_name, self.config)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        # Conectar o sinal de progresso do worker à atualização da interface
        self.worker.progress_updated.connect(self.progressdialog.update_progress)

        # Iniciar o upload quando a thread começar
        self.worker_thread.started.connect(lambda: self.worker.upload_folder(local_folder_path, destination_folder))

        # Start threads
        self.worker_thread.start()

    def update(self):
        if self.progressdialog.get_seen_so_far() >= self.progressdialog.getTotal_size():
            print(f"Upload concluído!")
            self.downloaded = True
            return
        QTimer.singleShot(500, self.update)

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
        LoadConfigs.Config.saveConfigDict("Credentials", json.dumps(token_dict))

    def Decode(self, token):
        return jwt.decode(token, self.KEY, algorithms=["HS256"])

