import os
import zipfile
import requests
import threading
import time
import tkinter as tk
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from Interfaces import CriarProjetoInterface
from Interfaces import InterfaceMain
from tkinter import ttk,messagebox
from Util import CustomWidgets, Styles, Util
from http.client import HTTPConnection 


HTTPConnection.protocol_version = "HTTP/2"

evento_termino = threading.Event()      
global foi_baixado 
foi_baixado = False

def transformar_link_dropbox(link):
    if "dl=0" in link:
        return link.replace("dl=0", "dl=1")
    return link


class DownloadProgress:
    def __init__(self, root, total_size):
        self.total_size = total_size
        self.bytes_downloaded = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
        
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
        

    def format_size(self, size):
        """Formata o tamanho em KB, MB ou GB."""
        if size >= 1024**3:  # GB
            return f"{size / (1024**3):.2f} GB"
        elif size >= 1024**2:  # MB
            return f"{size / (1024**2):.2f} MB"
        elif size >= 1024:  # KB
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size:.2f} bytes"

    def destroy(self):
        self.barra_progresso.destroy()
        self.janela.destroy()
    def update(self, chunk_size):
        with self.lock:
            self.bytes_downloaded += chunk_size
            percent = min((self.bytes_downloaded / self.total_size) * 100, 100)
            elapsed_time = time.time() - self.start_time
            download_rate = self.bytes_downloaded / elapsed_time if elapsed_time > 0 else 0
            download_rate_mb_s = download_rate / (1024 * 1024)
            bytes_remaining = self.total_size - self.bytes_downloaded
            speed = self.bytes_downloaded / (time.time() - self.start_time)  # Bytes por segundo
            time_remaining = bytes_remaining / speed if speed > 0 else 0  # Evita divisão por zero

            # Formata o tempo restante em hh:mm:ss
            hours, remainder = divmod(time_remaining, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            total_size_formatted = self.format_size(self.total_size)
            downloaded_size_formatted = self.format_size(self.bytes_downloaded)
            self.progresso.set(f"Progresso: {percent:.2f}%")
            self.total_baixado.set(f"Total baixado: {downloaded_size_formatted}/{total_size_formatted}")
            self.velocidade_download.set(f"Velocidade de download: {download_rate_mb_s:.2f} MB/s")
            self.tempo_restante.set(f"Tempo restante: {time_str}")
            #self.variavel.set(f"Progresso: {percent:.2f}% - {downloaded_size_formatted}/{total_size_formatted} - Taxa de download: {download_rate_mb_s:.2f} MB/s - Tempo restante: {time_str}")
            self.barra_progresso['value'] = percent
            print(f"Progresso: {percent:.2f}% - {downloaded_size_formatted}/{total_size_formatted} - Taxa de download: {download_rate_mb_s:.2f} MB/s - Tempo restante: {time_str}", end='\r')

def download_chunk(url,dir_path, filename, start, end, session, progress, lock, stop_event):
    """Baixa uma parte (chunk) do arquivo, atualiza o progresso e usa um lock para sincronização."""
    headers = {'Range': f'bytes={start}-{end}'}
    caminho_completo = os.path.join(dir_path, filename)
    with session.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()

        if stop_event.is_set():
            return  # Return immediately if stop_event is set

        with lock:  # Adquire o lock antes de escrever
            with open(caminho_completo, 'ab') as f:  # Modo append binary
                for chunk in r.iter_content(chunk_size=8192):
                    if stop_event.is_set():
                        return
                    if chunk:
                        f.write(chunk)
                        progress.update(len(chunk))

    # Signal completion of download
    stop_event.set()

def check_zip_integrity(filename):
    """Verifica a integridade do arquivo ZIP."""
    try:
        with zipfile.ZipFile(filename) as zf:
            zf.testzip()
        return True
    except zipfile.BadZipFile:
        return False

def baixar_pasta_dropbox(root,url, dir_path, num_threads=8, chunk_size=8 * 1024 * 1024):
    """Baixa um arquivo em partes usando threads e exibe o progresso."""

    if not url.startswith('https://www.dropbox.com'):
        messagebox.showerror("Error","Link do dropbox inválido ou comprometido.")
        return

    existing_size = 0
    if os.path.exists(dir_path):
        existing_size = os.path.getsize(dir_path)
        print("Iniciando novo download")
        #print(f"Retomando download a partir de {existing_size} bytes")
    else:
        print("Iniciando novo download")
        with open(dir_path, 'wb') as f:
            pass

    retry_strategy = Retry(
        total=10,  # Aumento das tentativas de repetição
        backoff_factor=0.5,  # Backoff ajustado
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    
    url_download = transformar_link_dropbox(url)
    with requests.Session() as session:
        adapter = HTTPAdapter(max_retries=retry_strategy,pool_connections=20,pool_maxsize=20)  # Define o adapter dentro do with
        session.mount('https://', adapter)
        session.mount('http://', adapter)

        with session.get(url_download, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))

        chunk_size = (total_size + num_threads - 1) // num_threads  

        progress = DownloadProgress(InterfaceMain.root,total_size)
        lock = threading.Lock() 
        stop_event = threading.Event()

        threads = []
        #nome_arquivo = url_download.split("/")[-1].split("?")[0] + ".zip"
        nome_arquivo = CriarProjetoInterface.nome_projeto_var.get() + ".zip"
        for i in range(num_threads):
            chunk_start = i * chunk_size
            chunk_end = min(chunk_start + chunk_size - 1, total_size - 1)
            t = threading.Thread(target=download_chunk, args=(url_download,dir_path, nome_arquivo,chunk_start, chunk_end, session, progress, lock, stop_event))
            threads.append(t)
            t.daemon = True
            t.start()

        for t in threads:
            t.join()

        print("\nDownload concluído!")
        progress.destroy()
        original = os.path.join(dir_path, nome_arquivo)
        caminho_normalizado = original.replace('/', '\\').replace('\\', '\\\\')
        global caminho_completo_tratado
        ori = rf"{original}"
        caminho_completo_tratado = os.path.normpath(ori)
        def baixou():
            global foi_baixado    
            foi_baixado = True
                

        if not check_zip_integrity(original):
            Util.LogError("DropboxDownloader","Arquivo ZIP corrompido.\nSe persistir, use o site do dropbox e reporte o erro.")
            os.remove(original)
            # Opções:
            # 1. Tentar baixar novamente:
            # baixar_pasta_dropbox(root, url, dir_path, num_threads, chunk_size)
            # 2. Informar o usuário e permitir que ele decida:
            # if messagebox.askretrycancel("Erro", "Arquivo ZIP corrompido. Tentar novamente?"):
            #     baixar_pasta_dropbox(root, url, dir_path, num_threads, chunk_size)
            # else:
            #     # Lidar com o erro (ex: exibir mensagem, registrar log, etc.)
        def f():
            global foi_baixado  
            foi_baixado = False
            print("Foi_baixado = False")
        InterfaceMain.root.after(5000, baixou)
        InterfaceMain.root.after(10000, f)
