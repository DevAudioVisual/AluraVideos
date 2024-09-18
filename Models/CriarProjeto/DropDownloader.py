import threading
import time
from tkinter import messagebox, ttk
import zipfile
import requests
import os
import tkinter as tk

from Util import CustomWidgets, Styles

class DownloadDropApp():
    def __init__(self, root, url, extract_folder_path):
        self.extract_folder_path = extract_folder_path
        self.zip_file = None
        self.url = self.convert_link(url)
        self.downloaded = False
        self.root = root
        
        self.Interface = DownloadDropInterface(root)
        
        self.velocidade = 0
        self.tempo_restante = 0
        self.downloaded_size = 0
        self.progress = 0
        self.total_size = 0
        
    def startDownload(self): 
        threading.Thread(target=self.Download,daemon=True).start()
        threading.Thread(target=self.updateInterface,daemon=True).start()
        
    def updateInterface(self):
        if self.downloaded == True:
            return
        self.Interface.velocidade_download.set(f"Velocidade: {self.format_size(self.velocidade)}/s")
        self.Interface.tempo_restante.set(f"Tempo Restante: {time.strftime('%H:%M:%S', time.gmtime(self.tempo_restante))}") 
        self.Interface.total_baixado.set(f"Tamanho do Arquivo: {self.format_size(self.downloaded_size)} / {self.format_size(self.total_size)}")
        self.Interface.barra_progresso['value'] = self.progress
        self.root.update_idletasks()
        self.root.after(300, self.updateInterface)
             
    def Download(self,chunk_size=8192):
        if not self.url.startswith('https://www.dropbox.com'):
            messagebox.showerror("Error","Link do dropbox inválido ou comprometido.")
            return
        filename = "arquivo_videos.zip"
        folderpath = os.path.join(self.extract_folder_path)
        os.makedirs(folderpath, exist_ok=True)
        filepath = os.path.join(folderpath,filename)

        retries = 0
        max_retries = 3
        retry_delay = 5
        
        start_time = time.time()
        
        while retries < max_retries:
            try:
                response = requests.get(self.url, stream=True, allow_redirects=True)
                self.total_size = int(response.headers.get('content-length', 0))
                self.downloaded_size = 0
                with open(filepath, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size): 
                        size = file.write(data)
                        self.downloaded_size += size
                        self.progress = (self.downloaded_size / self.total_size) * 100
                        self.elapsed_time = time.time() - start_time
                        self.velocidade = (self.downloaded_size / self.elapsed_time) 
                        self.tempo_restante = ((self.total_size - self.downloaded_size) / self.velocidade) if self.velocidade > 0 else 0
                        
                        #print(f"Velocidade: {self.format_size(self.velocidade)}")
                        
                self.zip_file = filepath
                if not self.check_zip_integrity(filepath):
                    print("Arquivo zip corrompido.")
                self.downloaded = True
                self.Interface.janela.destroy()
                break 
            except requests.exceptions.RequestException as e:
                retries += 1
                print(f"Erro no download (tentativa {retries}/{max_retries}): {e}")
                if retries < max_retries:
                    print(f"Tentando novamente em {retry_delay} segundos...")
                    time.sleep(retry_delay)
                else:
                    print("Número máximo de tentativas atingido. Download falhou.")
                    
    def convert_link(self,url):
        if "dl=0" in url:
            return url.replace("dl=0", "dl=1")
        return url
    
    def check_zip_integrity(self,filename):
        try:
            with zipfile.ZipFile(filename) as zf:
                zf.testzip()
            return True
        except zipfile.BadZipFile:
            return False
    def format_size(self, size):
        if size >= 1024**3:  # GB
            return f"{size / (1024**3):.2f} GB"
        elif size >= 1024**2:  # MB
            return f"{size / (1024**2):.2f} MB"
        elif size >= 1024:  # KB
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size:.2f} bytes"
        
        
class DownloadDropInterface():
    def __init__(self, root):
        self.janela = tk.Toplevel(root)
        self.janela.title("Baixando arquivos...")
        self.janela.configure(bg=Styles.cor_fundo,padx=50,pady=50)
        self.janela.protocol("WM_DELETE_WINDOW", lambda: None)
        self.janela.lift()
        self.janela.attributes('-topmost', True)
        self.janela.after_idle(self.janela.attributes, '-topmost', False)
        self.janela.resizable(False, False)
        
        frameBarra = CustomWidgets.CustomFrame(self.janela)
        frameBarra.pack()
        
        self.barra_progresso = ttk.Progressbar(frameBarra, orient='horizontal', length=300, mode='determinate',style="Horizontal.TProgressbar")
        self.barra_progresso.pack(anchor="center",side="top")
        self.progresso = tk.StringVar()
        self.total_baixado = tk.StringVar()
        self.velocidade_download = tk.StringVar()
        self.tempo_restante = tk.StringVar()
        CustomWidgets.CustomEntry(frameBarra,textvariable=self.progresso,width=380,border_width=0,fg_color=Styles.cor_fundo,text_color="white",state="readonly").pack(anchor="center",side="top",pady=2)
        CustomWidgets.CustomEntry(self.janela,textvariable=self.total_baixado,width=380,border_width=0,fg_color=Styles.cor_fundo,text_color="white",state="readonly").pack(fill="x",pady=2)
        CustomWidgets.CustomEntry(self.janela,textvariable=self.velocidade_download,width=380,border_width=0,fg_color=Styles.cor_fundo,text_color="white",state="readonly").pack(fill="x",pady=2)
        CustomWidgets.CustomEntry(self.janela,textvariable=self.tempo_restante,width=380,border_width=0,fg_color=Styles.cor_fundo,text_color="white",state="readonly").pack(fill="x",pady=2)
            
