from concurrent.futures import ThreadPoolExecutor
import json
from logging import root
import os
import threading
import time
from tkinter import messagebox
import jwt
import Main
from Util import Styles
import Util.CustomWidgets as ctk
import boto3
import tkinter as tk
from tkinter import ttk
from boto3.s3.transfer import TransferConfig

_seen_so_far = 0

class S3Model():
  def __init__(self):
    self.KEY = os.environ.get('S3_KEY')
    self.s3_client = None
    self.bucket_name = "equipevideos"
    self.downloaded = False
    
  def resetCredentials(self):
    Main.Config.Reset("Credentials",reabrir=False)
    
  def setS3Client(self):  
    try:
      access_key = self.Decode(Main.Config.getConfigData("Credentials","token"))['access_key']
      secret_key = self.Decode(Main.Config.getConfigData("Credentials","token"))['secret_key']
      self.s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
      return True
    except Exception as e:
      print(e)
      return False
      
  def upload_folder_to_s3(self, local_folder_path, destination_folder):
    folder_name = os.path.basename(local_folder_path)

    # Certifique-se de que destination_folder não termina com barra
    destination_folder = destination_folder.rstrip('/')

    # Constrói o caminho completo da pasta de destino no S3, incluindo a barra final
    s3_destination_folder = f"{destination_folder}/{folder_name}/"
    s3_destination_folder = s3_destination_folder.replace('\\', '/')

    Interface = ProgressInterface()
    total_size = 0
    Interface.create_progress_window()
    for root, dirs, files in os.walk(local_folder_path):
        for file in files:
            total_size += os.path.getsize(os.path.join(root, file))
    def update(): 
        global _seen_so_far
        Interface.update_progress(_seen_so_far, total_size)
        if _seen_so_far >= total_size:
            print(f"baixado com sucesso!")
            self.downloaded == True
            return            
        Main.InterfaceMain.root.after(700, update)
    update()
    config = TransferConfig(
                      multipart_threshold=1024 * 1024 * 32,
                      multipart_chunksize=1024 * 1024 * 32,
                      use_threads=False,
                      #max_concurrency=10
                  ) 
    with ThreadPoolExecutor(max_workers=10) as executor:
      for root, dirs, files in os.walk(local_folder_path):
          for dir_name in dirs:
              subfolder_path = os.path.relpath(os.path.join(root, dir_name), local_folder_path)
              s3_subfolder_key = os.path.join(s3_destination_folder, subfolder_path)
              s3_subfolder_key = s3_subfolder_key.replace('\\', '/')

          for file in files:
              local_file_path = os.path.join(root, file)
              local_file_path = local_file_path.replace('\\', '/')

              # Calcula o caminho relativo do arquivo, incluindo a subpasta
              relative_path = os.path.relpath(local_file_path, local_folder_path)
              relative_path.replace('\\', '/')

              # Constrói o caminho completo do objeto no S3, incluindo subpastas
              s3_key = os.path.join(s3_destination_folder, relative_path)

              s3_key = s3_key.replace('\\', '/')

              # Configura o manipulador de progresso
              progress_callback = ProgressPercentage(local_file_path)
              try:           
                  executor.submit(self.s3_client.upload_file, local_file_path, self.bucket_name, s3_key, Callback=progress_callback, Config=config)
              except Exception as e:
                  print(f"\nErro ao carregar o arquivo {local_file_path}: {e}")
                
  def list_folders_s3(self,sort = False):
    folder_names = []
    paginator = self.s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=self.bucket_name, Delimiter='/'):
        if 'CommonPrefixes' in page:
            for prefix in page['CommonPrefixes']:
                folder_names.append(prefix['Prefix'].rstrip('/'))

    return folder_names if not sort else sorted(folder_names)
  
  def registerCredentials(self,secret_key,access_key):
        if not self.ValidateCredentials(access_key=access_key,secret_key=secret_key):
          messagebox.showwarning("Aviso", "Credenciais inválidas")
          return False
        else:
          messagebox.showinfo("Sucesso!","Credenciais válidadas e registradas com sucesso!")
          self.Encode(access_key=access_key,secret_key=secret_key)
          return True
          
  def ValidateCredentials(self,secret_key, access_key):
    try:
        self.s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.s3_client.list_buckets()
        return True 
    except Exception as e:
        print(e)
        return False 
    
  def hasToken(self):
    return Main.Config.getConfigData("Credentials","token") != "" 
    
  def Encode(self,access_key,secret_key):
    payload= {
      "secret_key": secret_key,
      "access_key": access_key
    }
    token = jwt.encode(payload, self.KEY, algorithm="HS256")
    token_dict = {
      "token": token
    }
    Main.Config.saveConfigDict("Credentials",json.dumps(token_dict))
    
  def Decode(self,token):
    return jwt.decode(token, self.KEY, algorithms=["HS256"])

class ProgressInterface():
    def __init__(self):
       # Criação dos elementos da janela principal
        self.janela = tk.Toplevel()
        self.janela.configure(bg=Styles.cor_fundo,padx=50,pady=50)
        self.janela.lift()
        self.janela.attributes('-topmost', True)
        self.janela.after_idle(self.janela.attributes, '-topmost', False)
        
        self.main_frame = ctk.CustomFrame(self.janela)
        self.main_frame.pack(fill="both", expand=True, anchor="center")

        self.start_time = None
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.main_frame, variable=self.progress_var, maximum=100)
        self.progress_label = ctk.CustomLabel(self.main_frame,font=Styles.fonte_input, text="Progresso: Calculando...")
        self.time_remaining_label = ctk.CustomLabel(self.main_frame,font=Styles.fonte_input, text="Tempo restante: Calculando...")
        self.speed_label = ctk.CustomLabel(self.main_frame,font=Styles.fonte_input, text="Velocidade: Calculando...")
        
    def create_progress_window(self):
        def create():    
            self.progress_bar.pack()
            self.progress_label.pack()
            self.time_remaining_label.pack()        
            self.speed_label.pack()
        threading.Thread(target=create,daemon=True).start()
        
    def update_progress(self, uploaded_size, total_size):
          progress_percent = (uploaded_size / total_size) * 100
          self.progress_var.set(progress_percent)
          self.progress_label.get().configure(text=f"{progress_percent:.2f}%")

          if self.start_time is None:
              self.start_time = time.time()
          else:
              if progress_percent >= 99:
                  self.time_remaining_label.get().configure(text=f"Concluído")
                  self.progress_var.set(100)
                  self.speed_label.pack_forget()
                  self.progress_label.pack_forget()
                  self.main_frame.update()
                  return
              elapsed_time = time.time() - self.start_time
              remaining_time = (elapsed_time / progress_percent) * (100 - progress_percent) if progress_percent > 0 else 0
              self.time_remaining_label.get().configure(text=f"Tempo restante: {time.strftime('%H:%M:%S', time.gmtime(remaining_time))}")

              speed = uploaded_size / elapsed_time
              self.speed_label.get().configure(text=f"Velocidade: {format_size(speed)}/s")

          self.main_frame.after(100, lambda: self.main_frame.update_idletasks()) 


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename)) 
        self._lock = threading.Lock()
           
          
    def __call__(self, bytes_amount): 
        with self._lock:
            global _seen_so_far
            _seen_so_far += bytes_amount
            #print(_seen_so_far)
            
    
def format_size(size):
    if size >= 1024**3:  # GB
        return f"{size / (1024**3):.2f} GB"
    elif size >= 1024**2:  # MB
        return f"{size / (1024**2):.2f} MB"
    elif size >= 1024:  # KB
        return f"{size / 1024:.2f} KB"
    else:
        return f"{size:.2f} bytes"