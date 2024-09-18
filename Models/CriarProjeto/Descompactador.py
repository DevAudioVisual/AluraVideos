import os
import re
import subprocess
import threading
import time
import tkinter as tk
from tkinter import ttk
import zipfile
import patoolib
from unidecode import unidecode
import Main
from Util import Util, Styles
import Util.CustomWidgets as ctk

class Descompact():
    def __init__(self):
        self.arquivo_entrada = None
        self.diretorio_saida = None
        self.descompacted = False
        self.novo_caminho_completo = None
        
        self.Interface = None
        
        self.patoolprogress = 0
        self.audioprogress = 0
        
        self.total_zip = 0
    def start(self,arquivo_entrada,diretorio_saida):
        self.arquivo_entrada = arquivo_entrada
        self.diretorio_saida = diretorio_saida
        self.limpar_texto()
        zip_file = zipfile.ZipFile(self.novo_caminho_completo)
        self.total_zip = len(zip_file.infolist())
        self.Interface = ProgressInterface()
        self.Interface.create_progress_window()
        def ConvertAndExtract():
            self.converter_zip_rar()
            self.extractAudios()
        def updateInterface():
            if self.descompacted == True:
                self.Interface.janela.destroy()
                return
            total_videos = sum(1 for filename in os.listdir(self.diretorio_saida) if filename.endswith(('.mp4', '.avi', '.mkv', '.mov')))
            if total_videos >= (self.total_zip -1):
                self.patoolprogress = 100
            else:
                self.patoolprogress = int((total_videos / self.total_zip) * 100) if self.total_zip > 0 else 0
            self.Interface.update_progress(audio_progress=self.audioprogress,descompact_progress=self.patoolprogress)
            Main.InterfaceMain.root.after(300, updateInterface)
        threading.Thread(target=updateInterface,daemon=True).start()    
        threading.Thread(target=ConvertAndExtract,daemon=True).start()
        
    def converter_zip_rar(self):
        try:     
            patoolib.extract_archive(self.novo_caminho_completo, outdir=self.diretorio_saida)
            os.remove(self.novo_caminho_completo)
        except patoolib.util.PatoolError as e:
            if isinstance(e, UnicodeDecodeError):
                Util.LogError("Descompactador", f"Erro de codificação no arquivo '{self.arquivo_entrada}'. Tente renomear o arquivo manualmente ou usar outro programa para descompactar.")
            else:
                Util.LogError("Descompactador", f"Erro ao converter o arquivo '{self.arquivo_entrada}': {e}")
        except Exception as ex:
            Util.LogError("Descompactador", f"Erro inesperado: {ex}")
    def extractAudios(self):
            total_videos = sum(1 for filename in os.listdir(self.diretorio_saida) if filename.endswith(('.mp4', '.avi', '.mkv', '.mov')))
            audios_extraidos = 0    
            diretorio_audio = os.path.dirname(self.diretorio_saida)
            diretorio_audio2 = os.path.join(diretorio_audio, "02_Audio")      
    
            for filename in os.listdir(self.diretorio_saida):
                # Adicione mais extensões se necessário
                if filename.endswith(('.mp4', '.avi', '.mkv', '.mov')):
                    video_path = os.path.join(self.diretorio_saida, filename)
                    video_path2 = os.path.normpath(video_path)
                    # Use .wav para qualidade original
                    audio_filename = os.path.splitext(filename)[0] + '.wav'
                    audio_path = os.path.join(diretorio_audio2, audio_filename)
                    audio_path2 = os.path.normpath(audio_path)

                    command = f'{Util.pegarFFMPEG()} -loglevel quiet -i "{video_path2}" "{audio_path2}"'

                    try:
                        subprocess.run(command, shell=True, check=True)
                        audios_extraidos +=1           
                        self.audioprogress = int((audios_extraidos / total_videos) * 100)
                        if self.audioprogress >= 99:
                            self.audioprogress = 100
                            self.descompacted = True
                    except subprocess.CalledProcessError as e:
                        Util.LogError("Descompactador", f'Erro ao extrair áudio de "{filename}": {e}')
            
    def limpar_texto(self):     
        try: 
            self.arquivo_entrada = os.path.normpath(self.arquivo_entrada)
            nome_arquivo = os.path.basename(self.arquivo_entrada)
            
            texto_normalizado = unidecode(nome_arquivo)
            nome_arquivo = re.sub(r'[^a-zA-Z0-9\s-]', '', texto_normalizado)
            nome_arquivo = nome_arquivo.replace('ç', 'c')
            
            novo_nome_arquivo = re.sub(r'[à-úÀ-Úâ-ûÂ-Ûã-õÃ-ÕçÇ\-_\+ ]', ' ', nome_arquivo).strip()
            novo_nome_arquivo = novo_nome_arquivo + ".zip"
            self.novo_caminho_completo = os.path.join(self.diretorio_saida, novo_nome_arquivo)
            os.rename(self.arquivo_entrada, self.novo_caminho_completo)
        except Exception as e:
            Util.LogError("LimparTextoDescompactador", f"Ocorreu um erro ao normalizar o arquivo: {e}", True)
            
            
class ProgressInterface():
    def __init__(self):
        self.janela = tk.Toplevel()
        self.janela.configure(bg=Styles.cor_fundo,padx=50,pady=50)
        self.janela.lift()
        self.janela.attributes('-topmost', True)
        self.janela.after_idle(self.janela.attributes, '-topmost', False)
        
        self.janela.title("Descompactador e Extrator")
        
        self.main_frame = ctk.CustomFrame(self.janela)
        self.main_frame.pack(fill="both", expand=True, anchor="center")

        
        self.descompactador = ctk.CustomLabel(self.main_frame,font=Styles.fonte_input, text="Descompactando:")
        self.descompactador_var = tk.DoubleVar()
        self.descompactador_progressbar = ttk.Progressbar(self.main_frame, variable=self.descompactador_var, maximum=100,length=300)
        
        self.extrator = ctk.CustomLabel(self.main_frame,font=Styles.fonte_input, text="Extraindo audios:")
        self.extrator_var = tk.DoubleVar()
        self.extrator_progressbar = ttk.Progressbar(self.main_frame, variable=self.extrator_var, maximum=100,length=300)

        
    def create_progress_window(self):
        def create():    
            self.descompactador.pack()
            self.descompactador_progressbar.pack()
            self.extrator.pack()
            self.extrator_progressbar.pack()
        threading.Thread(target=create,daemon=True).start()
        
    def update_progress(self, descompact_progress, audio_progress):    
          if audio_progress <= 0: audio_progress = 0 
          if descompact_progress <= 0: descompact_progress = 0 
          self.extrator_var.set(audio_progress)
          self.descompactador_var.set(descompact_progress)
          self.main_frame.after(300, lambda: self.main_frame.update_idletasks()) 
            

