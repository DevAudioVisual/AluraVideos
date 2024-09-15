from concurrent.futures import ThreadPoolExecutor
import os
import subprocess
import tempfile
import threading
import time
import requests
import Main
import tkinter as tk
import Util.CustomWidgets as ctk
from Util import Styles

def interfaceGerenciadorExtensoes():
  root = Main.InterfaceMain.root
  janela = tk.Toplevel(root)
  janela.title("Baixar extensões")
  janela.geometry("350x220")
  janela.configure(bg=Styles.cor_fundo,padx=50,pady=50)
  janela.lift()
  janela.attributes('-topmost', True)
  janela.after_idle(janela.attributes, '-topmost', False)
  
  frame = ctk.CustomFrame(janela)
  frame.pack()
  
  textEffector = "Download Effector"
  EffectorB = ctk.CustomButton(frame,text=textEffector,command=lambda: Downloader("Effector",EffectorB,textEffector),width=150)
  EffectorB.pack(pady=5)
  textOrdinem = "Download Ordinem"
  OrdinemB = ctk.CustomButton(frame,text=textOrdinem,command=lambda: Downloader("Ordinem",OrdinemB,textOrdinem),width=150)
  OrdinemB.pack(pady=5)
  textNotability = "Download Notability"
  NotabilityB = ctk.CustomButton(frame,text=textNotability,command=lambda: Downloader("Notability",NotabilityB,textNotability),width=150)
  NotabilityB.pack(pady=5)
  
class Downloader():
    def __init__(self,repo_name,widget,text):
        self.widget = widget
        self.text = text
        self.repo_owner = "DevAudioVisual"
        self.repo_name = repo_name
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        self.headers = {"Accept": "application/vnd.github+json"}
        
        self.response = requests.get(self.api_url, headers=self.headers)
        self.response.raise_for_status()
        self.release_data = self.response.json()
        self.latest_tag_name = self.release_data["tag_name"]
        self.release_notes = self.release_data["body"]
        
        self.widget.getButton().configure(text="Baixando...")
        self.widget.getButton().configure(fg_color="grey")
        self.widget.getButton().configure(state=tk.DISABLED)
        threading.Thread(target=self.download,daemon=True).start()
    def download(self):
        exe_asset = next((asset for asset in self.release_data["assets"] if asset["name"].endswith(".exe")), None)
        if not exe_asset:
            self.widget.getButton().configure(text="Erro")
            self.widget.getButton().configure(fg_color="red")
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
                self.widget.getButton().configure(text=self.text)
                self.widget.getButton().configure(fg_color=Styles.cor_botao)
                self.widget.getButton().configure(state=tk.NORMAL)
                time.sleep(1)
                baixado = True
                
        while True:
            if baixado == True:
                print(f"Executando {exe_asset['name']}...")
                subprocess.run([temp_exe_path])
                break
            else:
                self.widget.getButton().configure(text="Erro")
                self.widget.getButton().configure(fg_color="red")
                print(f"Erro no download de {exe_asset['name']}. O tamanho do arquivo baixado não corresponde ao tamanho esperado.")
                
    def download_file(self,url, file_path, chunk_size=8192, max_retries=5, retry_delay=1):
        for attempt in range(max_retries):
            try:
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    #total_size = int(r.headers.get('content-length', 0))
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
                    self.widget.getButton().configure(text="Erro")
                    self.widget.getButton().configure(fg_color="red")
                    raise 