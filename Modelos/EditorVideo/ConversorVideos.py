import re
import subprocess
import threading
from tkinter import ttk
import Main
import Modelos.EditorVideo.InterfaceConversorMP4 as InterfaceConversorMP4
from Modelos.Interface import Interface
import Util.Util as Util
import fnmatch
import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinter import messagebox

comando_ffmpeg = Util.pegarFFMPEG()

def select_input_directory():
    entrada = ctk.StringVar()
    arquivo = filedialog.askopenfiles()
    entrada.set(arquivo[0].name)
    InterfaceConversorMP4.input_dir_var2.set(entrada.get())
    for a in arquivo:     
       InterfaceConversorMP4.input_dir_var.append(a.name)

def select_output_directory():
    output_directory = filedialog.askdirectory()
    InterfaceConversorMP4.output_dir_var.set(output_directory)

class Converter():
    def __init__(self, input_dir, output_dir,decodificadorVar,video_fps,video_crf,preset_compressao,ResolucaooVar,formatoDe,formatoPara):
        super().__init__()
        self.decodificadorVar = decodificadorVar
        self.ResolucaooVar = ResolucaooVar
        
        
        
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.video_fps = video_fps
        self.video_crf = video_crf  
        self.preset_compressao = preset_compressao
        self.codec_video = f'-c:v {self.getDedcodificador()}'
        self.crf = self.getCrfOrQp()
        self.profile_video = '-profile:v high' 
        self.preset = f'-preset {self.preset_compressao}'
        self.fps_limit = f'-r "{int(self.video_fps)}"'
        self.resolucaoO = f'-s {self.getResulucao()}'
        self.debug = '-ss 00:00:00'
        self.formatoDe = formatoDe
        self.formatoPara = formatoPara
        
        self.barra_progresso = None
        self.janela = None
        
        
        
    def criarBarradeProgresso(self):
        self.janela = tk.Toplevel(Interface.root)
        self.janela.title("Convertendo, aguarde...")

        # Trazer a janela para frente
        self.janela.protocol("WM_DELETE_WINDOW", lambda: None)
        self.janela.lift()
        self.janela.attributes('-topmost', True)
        self.janela.after_idle(self.janela.attributes, '-topmost', False)
        self.janela.resizable(False, False)

        self.barra_progresso = ttk.Progressbar(self.janela, orient="horizontal", length=300, mode="determinate")
        self.barra_progresso.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        self.barra_progresso['value'] = 0
    def startCoversao(self):     
        def conv():
            threadBarra = threading.Thread(target=self.criarBarradeProgresso)
            threadBarra.setDaemon(True)
            threadBarra.start()
            for arquivo in self.input_dir:
                if fnmatch.fnmatch(arquivo, f'*{self.formatoDe}'): 
                        
                        # Define o nome do arquivo de saída para o vídeo e para o áudio
                        arquivo_saida = f'{arquivo}_CONVERTIDO{self.formatoPara}'
                        
                        # Verifica se os arquivos de saída já existem e adiciona sufixo se necessário
                        arquivo_saida = self.verificar_arquivo_existente(arquivo_saida)
                        
                        if not self.input_dir or not self.output_dir:
                            messagebox.showerror("Erro", "Entrada ou saída inválidos")
                            return
                        
                        # Monta o comando FFmpeg com os arquivos de saída ajustados
                        comando = f'{comando_ffmpeg} -hwaccel cuda -i "{arquivo}" {self.resolucaoO} {self.codec_video} {self.profile_video} {self.crf} {self.preset} {self.fps_limit} {self.debug} "{arquivo_saida}"'
                        #os.system(comando)     
                        process = subprocess.Popen(comando, stderr=subprocess.PIPE, universal_newlines=True)

                        duration_pattern = re.compile(r"Duration:\s*(\d{2}):(\d{2}):(\d{2})\.(\d{2})")
                        time_pattern = re.compile(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})")

                        duration = None
                        for line in process.stderr:
                            if duration is None:
                                duration_match = duration_pattern.search(line)
                                if duration_match:
                                    duration = (
                                        int(duration_match.group(1)) * 3600
                                        + int(duration_match.group(2)) * 60
                                        + int(duration_match.group(3))
                                        + float(duration_match.group(4)) / 100
                                    )
                            else:
                                time_match = time_pattern.search(line)
                                if time_match:
                                    elapsed_time = (
                                        int(time_match.group(1)) * 3600
                                        + int(time_match.group(2)) * 60
                                        + int(time_match.group(3))
                                        + float(time_match.group(4)) / 100
                                    )
                                    progress = (elapsed_time / duration) * 100
                                    self.barra_progresso['value'] = progress
                                    #print(f"Progresso: {progress:.2f}%")
                        
                        
                        
            self.janela.destroy()                          
            messagebox.showinfo("Sucesso!", "Conversão finalizada!")
        messagebox.showinfo("Iniciando", "Iniciando conversão!")    
        thread = threading.Thread(target=conv)
        thread.setDaemon(True)
        thread.start()
        
            
    def verificar_arquivo_existente(self,nome_arquivo):
        if not os.path.exists(nome_arquivo):
            return nome_arquivo
        
        nome_base, extensao = os.path.splitext(nome_arquivo)
        contador = 2
        while True:
            novo_nome = f"{nome_base}_V{contador}{extensao}"
            if not os.path.exists(novo_nome):
                return novo_nome
            contador += 1
            
    def getCrfOrQp(self):
        if self.getDedcodificador == "libx264":
            return f'-crf "{int(self.video_crf)}"'
        else:
            return f'-qp "{int(self.video_crf)}"'  
    def getDedcodificador(self):
        if self.decodificadorVar == "CPU":
            return "libx264"
        else: 
            return "h264_nvenc"
    def getResulucao(self):
        if self.ResolucaooVar == "4k":
            if InterfaceConversorMP4.UltraWideoVar.get() == 1:
                valor = 3840*2
                return f"{valor}x2160"
            else:
                return "3840x2160"
        elif self.ResolucaooVar == "2k":
            if InterfaceConversorMP4.UltraWideoVar.get() == 1:
                valor = 2048*2
                return f"{valor}x1080"
            else:
                return "2048x1080"
        elif self.ResolucaooVar == "1080P":
            if InterfaceConversorMP4.UltraWideoVar.get() == 1:
                valor = 1920*2
                return f"{valor}x1080"
            else:
                return "1920x1080"
        elif self.ResolucaooVar == "720P":
            if InterfaceConversorMP4.UltraWideoVar.get() == 1:
                valor = 1280*2
                return f"{valor}x720"
            else:
                return "1280x720"
        elif self.ResolucaooVar == "480P":
            if InterfaceConversorMP4.UltraWideoVar.get() == 1:
                valor = 854*2
                return f"{valor}x480"
            else:
                return "854x480"
        elif self.ResolucaooVar == "360P":
            if InterfaceConversorMP4.UltraWideoVar.get() == 1:
                valor = 640*2
                return f"{valor}x360"
            else:
                return "640x360"
        elif self.ResolucaooVar == "144P":
            if InterfaceConversorMP4.UltraWideoVar.get() == 1:
                valor = 256*2
                return f"{valor}x144"
            else:
                return "256x144"