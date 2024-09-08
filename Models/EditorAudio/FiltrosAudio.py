import os
import re
import subprocess
import tempfile
import threading
import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import Main
import Interfaces.EditorAudioInterface as AudioInterFace
from tkinter import ttk
from Models.EditorAudio.Efeitos import Speechnorm
from Interfaces import InterfaceMain
from Util import Util
import Util.CustomWidgets as CustomWidgets
import Util.Styles as Styles


class FiltrosAudio():
  def __init__(self,
               filtro_loudnorm,target_level,TP,LRA,
               filtro_afftdn,om,nf,nr,nt,tn,tr,
               filtro_speechnorm,p,t,
               filtro_audio_mono,
               audio_delay,audio_delay_ms,
               filtro_acompressor,
               acompressor_threshold,
               acompressor_ratio,
               acompressor_attack,
               acompressor_release,
               filtro_alimiter,
               alimiter_level_in,
               alimiter_level_out,
               alimiter_limit,
               alimiter_attack,
               alimiter_release	,
               alimiter_asc,
               alimiter_asc_level,
               alimiter_level,
               alimiter_latency,
               **kwargs):
        super().__init__(**kwargs)
        
        if not filtro_loudnorm: filtro_loudnorm = False
        if not filtro_afftdn: filtro_afftdn = False
        if not filtro_audio_mono: filtro_audio_mono = False
        if not filtro_loudnorm: filtro_loudnorm=False
        if not audio_delay: audio_delay = False
        if not filtro_acompressor: filtro_acompressor = False
        if not filtro_alimiter or filtro_alimiter is None: filtro_alimiter = False
        
        
        #self.audio_delay_ms = Util.frames_to_ms(Interface.SliderFrames.get_slider_value(), Interface.SliderFPS.get_slider_value())
        self.barra_progresso = None
        self.janela = None
        
        self.entrada = AudioInterFace.lista.getEntrada().get()
        self.om = om
        # Filtro para converter áudio para mono nos dois canais
        self.filtro_mono = 'pan=mono|c0=c0' if filtro_audio_mono else ''

        # Comando completo para FFmpeg
        self.comando = [
            Util.pegarFFMPEG(),        # Executável FFmpeg
            '-i', self.entrada,             # Arquivo de entrada
        ]

        # Montando a cadeia de filtros de áudio
        # Montando a cadeia de filtros de áudio
        self.filtros_audio = {}  # Dicionário para armazenar os filtros com seus nomes como chaves
        self.ordem_filtros = []  # Lista para armazenar a ordem dos filtros
        self.nova_ordem = AudioInterFace.lista.getAppManager().listaFiltros()
        # Adicionando filtro de conversão para mono, se ativado
        if filtro_audio_mono:
            self.filtros_audio["AudioMono"] = self.filtro_mono
            self.ordem_filtros.append("AudioMono")

        # Adicionando filtro loudnorm, se ativado
        if filtro_loudnorm:
            self.filtros_audio["Loudnorm"] = f'loudnorm=I={target_level}:TP={TP}:LRA={LRA}'
            self.ordem_filtros.append("Loudnorm")

        # Adicionando filtro speechnorm, se ativado
        if filtro_speechnorm:
            self.filtros_audio["Speechnorm"] = f'speechnorm=p={p}:t={t}'
            self.ordem_filtros.append("Speechnorm")

        # Adicionando filtro afftdn, se ativado
        if filtro_afftdn:
            self.filtros_audio["Afftdn"] = f'afftdn=nf={nf}:nr={nr}:nt={nt}:tn={tn}:tr={tr}:om={self.om}'
            self.ordem_filtros.append("Afftdn")

        if audio_delay:
            self.filtros_audio["AudioDelay"] = f'adelay={audio_delay_ms}:all=1'
            self.ordem_filtros.append("AudioDelay")
            
        if filtro_acompressor:
            self.filtros_audio["ACompressor"] = f'acompressor=threshold={acompressor_threshold}:ratio={acompressor_ratio}:attack={acompressor_attack}:release={acompressor_release}'
            self.ordem_filtros.append("ACompressor")
            
        if filtro_alimiter:
            self.filtros_audio["ALimiter"] = f'alimiter=level_in={alimiter_level_in}:level_out={alimiter_level_out}:limit={alimiter_limit}:attack={alimiter_attack}:release={alimiter_release}:asc={alimiter_asc}:asc_level={alimiter_asc_level}:level={alimiter_level}:latency={alimiter_latency}'
            self.ordem_filtros.append("ALimiter")

        # Unindo todos os filtros em uma única string separada por vírgulas
        if self.ordem_filtros:  # Verifica se a lista de ordem não está vazia
            self.ordem_filtros = self.reordenar_lista(self.ordem_filtros,self.nova_ordem)
            self.filtro_final = ','.join([self.filtros_audio[nome_filtro] for nome_filtro in self.ordem_filtros])
    
        
  def reordenar_lista(self,lista_original, nova_ordem):
    #if set(lista_original) != set(nova_ordem):
        #raise ValueError("As listas devem conter os mesmos elementos.")

    return [elemento for elemento in nova_ordem if elemento in lista_original]
  
    
  def converter(self,arquivo):
    saida = arquivo + '.wav'
    self.comando = [
            Util.pegarFFMPEG(),        # Executável FFmpeg
            '-i', arquivo,             # Arquivo de entrada
        ]
    self.comando += [
    *(['-af', self.filtro_final] if self.filtro_final else []),
    '-y',
    saida         # Formato de saída WAV para stdout
    ]
    #print(self.comando)
    #messagebox.showinfo("aviso",self.comando)
    def cv():
        # threadBarra = threading.Thread(target=self.criarBarradeProgresso)
        # threadBarra.setDaemon(True)
        # threadBarra.start()
        #subprocess.run(self.comando, check=True)
                #os.system(comando)     
        process = subprocess.Popen(self.comando, stderr=subprocess.PIPE, universal_newlines=True)

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
                    #self.barra_progresso['value'] = progress
                    #print(f"Progresso: {progress:.2f}%")
        #self.janela.destroy()                          
    thread = threading.Thread(target=cv)
    thread.daemon = True
    thread.start()
    
  def ouvir(self):  
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as arquivo_temporario:
       saida_temporaria = arquivo_temporario.name
    self.comando += [
      *(['-af', self.filtro_final] if self.filtro_final else []),
      '-y',
      '-f', 'wav', saida_temporaria,         # Formato de saída WAV para stdout
      ]
          # Executando o comando FFmpeg
          # Executando o FFmpeg e capturando a saída
          # Executando o FFmpeg e capturando a saída
    try:
              subprocess.run(self.comando, check=True)
              #print(self.comando)
              print("Áudio processado com sucesso.")

              # Comando ffplay para reproduzir o áudio com medidor de volume
              comando_ffplay = [
            Util.pegarFFMPLAY(),
            '-i', saida_temporaria,
            '-showmode', '1',
            '-window_title', 'Ouvindo:'
        ]
              """
              def mostrarGráfico():
                 audio, samplerate = sf.read(saida_temporaria)
                 db = 20 * np.log10(np.abs(audio))
                 plt.figure(figsize=(10, 6))
                 plt.plot(db)
                 plt.xlabel('Amostra')
                 plt.ylabel('Decibéis (dB)')
                 plt.title('Gráfico de Decibéis do Áudio')
                 plt.grid(True)
                 plt.show()
              if AudioInterFace.mostrarGrafico:
                 thread = threading.Thread(target=mostrarGráfico)
                 thread.daemon = True
                 thread.start()     
                """
              subprocess.run(comando_ffplay, check=True)
              print("Reprodução concluída com sucesso!")
    except subprocess.CalledProcessError as error:
            Util.LogError("FiltrosAudio",f"Erro ao executar o FFmpeg ou ffplay: {error}")
    finally:
              # Remover o arquivo temporário após o uso
              os.remove(saida_temporaria)
  def criarBarradeProgresso(self):
        self.janela = tk.Toplevel(InterfaceMain.root)
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
              
class OrdemFiltros(ttk.Frame):
    def __init__(self, master=None, filtros=list):
        super().__init__(master)

        self.config(style="Custom.TFrame")
        self.ordem_janelas = filtros
        self.Label = CustomWidgets.CustomLabel(self,text="Ordem dos efeitos",font=Styles.fonte_titulo)
        self.Label.pack()
        self.Label2 = CustomWidgets.CustomLabel(self,text="(Clique e arraste para alterar)\n\n(Esquerdo para abrir parâmetros)\n\n(Direito para remover)",font=Styles.fonte_input)
        self.Label2.pack()
        self.listbox = tk.Listbox(self,
                                  width=30,
                                  bg=Styles.cor_fundo,
                                  fg=Styles.cor_texto,
                                  font=Styles.fonte_texto,
                                  highlightthickness=1,
                                  borderwidth=1,
                                  cursor="hand2",
                                  relief="flat",
                                  selectbackground=Styles.cor_ativo,
                                  selectmode="single")
        for item in self.ordem_janelas:
            self.listbox.insert(tk.END, item)
        self.listbox.pack(pady=20)
        self.listbox.bind("<ButtonRelease-1>", self.on_drop)
        self.listbox.bind("<<ListboxSelect>>", self.ativar_efeito)
        self.listbox.bind("<Button-3>", self.right_click)

        self.dragging = False
        
        self.listbox.pack()

    def ordem(self):
        return self.ordem_janelas

    def atualizar_lista(self, nova_lista):
        """Atualiza a Listbox de forma eficiente, alterando apenas os itens necessários."""
        for i, (item_antigo, item_novo) in enumerate(zip(self.ordem_janelas, nova_lista)):
            if item_antigo != item_novo:
                self.listbox.delete(i)
                self.listbox.insert(i, item_novo)
        self.ordem_janelas = nova_lista
    def right_click(self,event):
        self.efeitos(True)
        
    def on_drag(self, event):
        self.dragging = True
        self.drag_start_index = self.listbox.nearest(event.y)
        #self.efeitos(False)
        
    def ativar_efeito(self,event):
        self.efeitos(False)    
    def efeitos(self,remover):
        index = self.listbox.curselection()
        if index:
            item = self.listbox.get(index[0])
            print(f"Item clicado: {item}")
            for nome, metodo in AudioInterFace.getFiltros():
                if nome == item:
                    if metodo:
                        if remover:
                            AudioInterFace.lista.filtros_escolhidos_lista.remove(item)
                            metodo.esconder()
                            metodo.destroy()
                            metodo = None
                            self.listbox.delete(index)
                            self.ordem_janelas.remove(item)
                        else:
                            DesativaGeralMenosUm(item)
                            metodo.iniciar()
            """                    
            if item == "Speechnorm":
                if remover: 
                    AudioInterFace.lista.filtros_escolhidos_lista.remove(item)
                    AudioInterFace.lista.Speechnorm.esconder()
                    AudioInterFace.lista.Speechnorm.destroy()
                    AudioInterFace.lista.Speechnorm = None
                    self.listbox.delete(index)
                    self.ordem_janelas.remove(item)
                    print(f"Removendo: {item}")
                else:
                    if AudioInterFace.lista and AudioInterFace.lista.Speechnorm:
                        DesativaGeralMenosUm(item)
                        AudioInterFace.lista.Speechnorm.iniciar()
            elif item == "Loudnorm":
                if remover: 
                    AudioInterFace.lista.filtros_escolhidos_lista.remove(item)
                    AudioInterFace.lista.Loudnorm.esconder()
                    AudioInterFace.lista.Loudnorm.destroy()
                    AudioInterFace.lista.Loudnorm = None
                    self.listbox.delete(index)
                    self.ordem_janelas.remove(item)
                    print(f"Removendo: {item}")
                else:
                    if AudioInterFace.lista and AudioInterFace.lista.Loudnorm:
                        DesativaGeralMenosUm(item)
                        AudioInterFace.lista.Loudnorm.iniciar()
            elif item == "Afftdn":
                if remover: 
                    AudioInterFace.lista.filtros_escolhidos_lista.remove(item)
                    AudioInterFace.lista.Afftdn.esconder()
                    AudioInterFace.lista.Afftdn.destroy()
                    AudioInterFace.lista.Afftdn = None
                    self.listbox.delete(index)
                    self.ordem_janelas.remove(item)
                    print(f"Removendo: {item}")
                else:
                    if AudioInterFace.lista and AudioInterFace.lista.Afftdn:
                        DesativaGeralMenosUm(item)
                        AudioInterFace.lista.Afftdn.iniciar()
                        """
    def on_drop(self, event):
        if not self.dragging:
            return
        self.dragging = False

        drop_index = self.listbox.nearest(event.y)
        if drop_index == self.drag_start_index:
            return

        item = self.listbox.get(self.drag_start_index)
        self.listbox.delete(self.drag_start_index)
        self.listbox.insert(drop_index, item)

        # Atualizar DataFrame
        self.ordem_janelas.remove(item)
        self.ordem_janelas.insert(drop_index, item)

def DesativaGeralMenosUm(NaoDesativa = ""):
    for nome, metodo in AudioInterFace.getFiltros():
        if nome != NaoDesativa:
            if metodo:
                metodo.esconder()