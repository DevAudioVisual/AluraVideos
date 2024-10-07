import re
import sys
import threading
from tkinter import messagebox
import requests
import os
import tempfile
import subprocess
from concurrent.futures import ThreadPoolExecutor
import time
from packaging import version
from Util import Util
from PyQt6.QtCore import QTimer

class app():
    def __init__(self):
        self.repo_owner = "DevAudioVisual"
        self.repo_name = "AluraVideos"
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        self.headers = {"Accept": "application/vnd.github+json"}
        self.current_version = version.parse(Util.version.lstrip("V"))
        
        self.response = None
        self.release_data = None
        self.latest_tag_name = None
        self.release_notes = None
        self.release_version = None
        
        self.initRequest()
        #threading.Thread(target=self.initRequest(),daemon=True).start()
        
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
            self.check_updates()
        except requests.exceptions.RequestException as e:
            Util.LogError(func="Atualizações",mensagem=f"Erro ao buscar por atualizações: {e}")
        
    def download_file(self,url, file_path, chunk_size=8192, max_retries=5, retry_delay=1):
        for attempt in range(max_retries):
            try:
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(file_path, 'wb') as f:
                        with ThreadPoolExecutor(max_workers=4) as executor:
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
        if self.release_version > self.current_version:
            print("Atualização disponível")
            padrao = r'^(#{1,6})\s' 
            texto_sem_formatacao = re.sub(padrao, '', f"Atualização para a versão {self.release_version} disponível.\n\nNotas de atualização:\n{self.release_notes.replace('- ', '\n-')}", flags=re.MULTILINE)
            if messagebox.askyesno("Atualização disponivel", texto_sem_formatacao) == True:
                threading.Thread(target=self.download_latest_release(),daemon=True).start()   
            else:
                return
        else:
            print("Você está atualizado!")

            
    def download_latest_release(self):
        exe_asset = next((asset for asset in self.release_data["assets"] if asset["name"].endswith(".exe")), None)
        if not exe_asset:
            print(f"Nenhum arquivo .exe encontrado na release {self.latest_tag_name}")
            return

        exe_url = exe_asset["browser_download_url"]
        exe_size = exe_asset["size"]
        baixado = False 
                
        with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as temp_exe:
            temp_exe_path = temp_exe.name
            print(f"Baixando {exe_asset['name']}...")
            self.download_file(exe_url, temp_exe_path)
            
            downloaded_size = os.path.getsize(temp_exe_path)
            temp_exe_path = os.path.normpath(temp_exe_path)
            if downloaded_size == exe_size:
                print(f"Download de {exe_asset['name']} concluído com sucesso!")
                time.sleep(1)
                baixado = True
                
        def loopVerificarBaixado():
            if baixado != True:
                QTimer.singleShot(1000, lambda: loopVerificarBaixado())
                #Main.InterfaceMain.root.after(1000, lambda: loopVerificarBaixado())
                return
            print(f"Executando {exe_asset['name']}...")
            subprocess.run([temp_exe_path])
            sys.exit()
        loopVerificarBaixado()        