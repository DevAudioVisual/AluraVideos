from tkinter import messagebox
import Util.Util as Util;
import customtkinter as ctk
import tkinter as tk
import Util.CustomWidgets as CustomWidgets
import Modelos.EditorAudio.FiltrosAudio as FiltrosAudio
from tkinter import filedialog
import Util.Styles as Styles


def abrirConfigAudio(root,tabview):
  
  frame = CustomWidgets.CustomFrame(tabview.tab("Audio"))
  frame.pack()
  
  framebotoes = CustomWidgets.CustomFrame(frame)
  framebotoes.pack(side="top")
  
  frame_side_by_side = CustomWidgets.CustomFrame(frame)
  frame_side_by_side.pack(anchor="center",side="top")
  
  frameLouddorn = CustomWidgets.CustomFrame(frame_side_by_side)
  frameLouddorn.pack(side="left",fill="both",padx=10,pady=10)
  frameafftdn = CustomWidgets.CustomFrame(frame_side_by_side)
  frameafftdn.pack(side="left",fill="both",padx=10,pady=10)
  framespeechnorm = CustomWidgets.CustomFrame(frame_side_by_side)
  framespeechnorm.pack(side="left",fill="both",padx=10,pady=10)
  frameaaudio_delay = CustomWidgets.CustomFrame(frame_side_by_side)
  frameaaudio_delay.pack(side="left",fill="both",padx=10,pady=10)
  
  framearnndn = CustomWidgets.CustomFrame(frame_side_by_side)
  framearnndn.pack(side="left",fill="both",padx=10,pady=10)
  # framehighpass = CustomWidgets.CustomFrame(frame_side_by_side)
  # framehighpass.pack(side="left",fill="both",padx=10,pady=10)
  # framelowpass = CustomWidgets.CustomFrame(frame_side_by_side)
  # framelowpass.pack(side="left",fill="both",padx=10,pady=10)
  # frame_silence_remove = CustomWidgets.CustomFrame(frame_side_by_side)
  # frame_silence_remove.pack(side="left",fill="both",padx=10,pady=10)
  
  frameaaudio_mono = CustomWidgets.CustomFrame(frame_side_by_side)
  frameaaudio_mono.pack(side="left",fill="both",padx=10,pady=10)
  
  
  
  frameouvir = CustomWidgets.CustomFrame(frame)
  frameouvir.pack(side="bottom",anchor="center")

  global app_manager
  app_manager = AppManager(framearnndn, frameaaudio_mono)
  
  entrada = ctk.StringVar()
  arquivos = []
  def buscar():
    arquivos = []
    arquivo = filedialog.askopenfiles()
    entrada.set(arquivo[0].name)
    for a in arquivo:     
      arquivos.append(a.name)
    print(arquivos)
  CustomWidgets.CustomLabel(framebotoes,text="Arquivos:",font=Styles.fonte_titulo).pack(pady=10,padx=10,fill="x")  
  CustomWidgets.CustomButton(framebotoes,text="Buscar",dica=Util.quebrar_linhas("Selecione os arquivos que deseja editar o audio."),Image=CustomWidgets.CustomImage("folder.png",20,20),command=buscar).pack(pady=10,padx=10,side="right")
  CustomWidgets.CustomEntry(framebotoes,textvariable=entrada,width=500).pack(pady=10)
  
  filtro_loudnorm = tk.BooleanVar(value=False)
  CustomWidgets.CustomCheckBox(frameLouddorn,text="Loudnorm",command=lambda: app_manager.addFiltro("Loudnorm", filtro_loudnorm),dica=Util.quebrar_linhas("Loudnorm é um filtro de normalização de audio, assemelhando-se ao levelator. Com ele você nivelará todas as frequências."),variable=filtro_loudnorm).pack(pady=10)

  Slider_loudnorm_target_level = CustomWidgets.CustomSliderFloat(frameLouddorn,from_=-30,to=-5,start=-6,sufixo="DB's")
  Slider_loudnorm_target_level.pack(pady=10)
  Slider_loudnorm_target_levelVar = Slider_loudnorm_target_level.get_slider_value()
  
  Slider_loudnorm_TP = CustomWidgets.CustomSliderFloat(frameLouddorn,from_=-0,to=-100,start=-1.5,sufixo="TP")
  Slider_loudnorm_TP.pack(pady=10)
  Slider_loudnorm_TPVar = Slider_loudnorm_TP.get_slider_value()
  
  Slider_loudnorm_LRA = CustomWidgets.CustomSliderFloat(frameLouddorn,from_=1,to=20,start=11,sufixo="LRA")
  Slider_loudnorm_LRA.pack(pady=10)
  Slider_loudnorm_LRAVar = Slider_loudnorm_LRA.get_slider_value()
  
  filtro_afftdn = tk.BooleanVar(value=False)
  CustomWidgets.CustomCheckBox(frameafftdn,command=lambda: app_manager.addFiltro("Afftdn", filtro_afftdn),text="Afftdn",dica="Redutor de ruído",variable=filtro_afftdn).pack(pady=10)

  Slider_afftdn_NF = CustomWidgets.CustomSliderFloat(frameafftdn,from_=-99,to=0,start=-25,sufixo="Noise Floor",dica=Util.quebrar_linhas("Define o nível de ruído de fundo em decibéis (dB) que você deseja reduzir. Valores negativos indicam que o ruído está abaixo do nível do sinal desejado. Quanto mais negativo o valor, mais agressiva será a redução de ruído."))
  Slider_afftdn_NF.pack(pady=10)
  Slider_afftdn_NFVar = Slider_afftdn_NF.get_slider_value()

  Slider_afftdn_NR = CustomWidgets.CustomSliderFloat(frameafftdn,from_=0,to=100,start=22,sufixo="Noise Reduction",dica=Util.quebrar_linhas("Controla a quantidade de redução de ruído aplicada em decibéis (dB). Valores mais altos resultam em maior redução, mas podem afetar a qualidade do áudio."))
  Slider_afftdn_NR.pack(pady=10)
  Slider_afftdn_NRVar = Slider_afftdn_NR.get_slider_value()
  
  NtVar = tk.StringVar(value="w")
  CustomWidgets.CustomComboBox(frameafftdn,Values=["w","v"],variable=NtVar,dica="Noise Type: Especifica o tipo de ruído a ser reduzido.\nw: Ruído branco (espectro plano)\nv: Ruído variável (combinação de diferentes tipos)").pack(pady=10)
  
  Slider_afftdn_TN = CustomWidgets.CustomSliderFloat(frameafftdn,from_=0,to=100,start=1,sufixo="Threshold",dica=Util.quebrar_linhas("Define o limiar de ruído em relação ao nível do sinal. Valores mais altos significam que o filtro será mais agressivo na redução de ruído, mas também pode afetar o sinal original."))
  Slider_afftdn_TN.pack(pady=10)
  Slider_afftdn_TNVar = Slider_afftdn_TN.get_slider_value()
  
  Slider_afftdn_TR = CustomWidgets.CustomSliderFloat(frameafftdn,from_=0,to=100,start=0,sufixo="Threshold Ratio",dica=Util.quebrar_linhas("Define a proporção entre o limiar de ruído e o nível do sinal. Valores mais altos significam que o filtro será mais sensível a pequenas variações no nível de ruído."))
  Slider_afftdn_TR.pack(pady=10)
  Slider_afftdn_TRVar = Slider_afftdn_TR.get_slider_value()
  
  filtro_speechnorm = tk.BooleanVar(value=False)
  CustomWidgets.CustomCheckBox(framespeechnorm,command=lambda: app_manager.addFiltro("Speechnorm", filtro_speechnorm),text="Speechnorm",dica=Util.quebrar_linhas("Speechhorn é um filtro que se assemelha ao Loudnorm, porém ele tentará elevar apenas as frequências de dialogo."),variable=filtro_speechnorm).pack(pady=10,side="top")
  
  Slider_speechnorm_P = CustomWidgets.CustomSliderFloat(framespeechnorm,from_=10,to=-10,start=1,sufixo="P")
  Slider_speechnorm_P.pack(pady=10,side="top")
  Slider_speechnorm_PVar = Slider_speechnorm_P.get_slider_value()
  
  filtro_delay_audio = tk.BooleanVar(value=False)
  CustomWidgets.CustomCheckBox(frameaaudio_delay,command=lambda: app_manager.addFiltro("Audio Delay", filtro_delay_audio),text="Delay audio",variable=filtro_delay_audio).pack(pady=10,side="top")
  
  Slider_delayaudio = CustomWidgets.CustomSlider(frameaaudio_delay,from_=0,to=10000,start=0,sufixo="MS")
  Slider_delayaudio.pack(pady=10,side="top")
  Slider_delayaudioVar = Slider_delayaudio.get_slider_value()
  
  # filtro_arnndn = tk.BooleanVar(value=True)
  # CustomWidgets.CustomCheckBox(framearnndn,text="arnndn",dica=Util.quebrar_linhas("Redutor de ruído baseado em I.A (Em breve)"),variable=filtro_arnndn).pack(pady=10,side="top")
  
  # filtro_highpass = tk.BooleanVar(value=True)
  # CustomWidgets.CustomCheckBox(framehighpass,text="highpass",variable=filtro_highpass).pack(pady=10,side="top")
  
  # filtro_lowpass = tk.BooleanVar(value=True)
  # CustomWidgets.CustomCheckBox(framelowpass,text="lowpass",variable=filtro_lowpass).pack(pady=10,side="top")
  
  # filtro_silence_remove = tk.BooleanVar(value=True)
  # CustomWidgets.CustomCheckBox(frame_silence_remove,text="Silence remove",variable=filtro_silence_remove).pack(pady=10,side="top")
  
  filtro_audio_mono = tk.BooleanVar(value=True)
  app_manager.addFiltro("Audio Mono", filtro_audio_mono)
  CustomWidgets.CustomCheckBox(framearnndn,command=lambda: app_manager.addFiltro("Audio Mono", filtro_audio_mono),text="Audio Mono",dica=Util.quebrar_linhas("Deseja o audio mono?"),variable=filtro_audio_mono).pack(pady=10,side="top")
  
  def ouvir():
    if not entrada.get():
      messagebox.showwarning("Aviso","Arquivos não especificados")
      return
    Filtros = FiltrosAudio.FiltrosAudio(entrada=entrada.get(),
                                        filtro_loudnorm=filtro_loudnorm.get(),
                                        target_level=Slider_loudnorm_target_levelVar,
                                        TP=Slider_loudnorm_TPVar,
                                        LRA=Slider_loudnorm_LRAVar,
                                        filtro_afftdn=filtro_afftdn.get(),
                                        nr=Slider_afftdn_NRVar,
                                        tn=Slider_afftdn_TNVar,
                                        tr=Slider_afftdn_TRVar,
                                        nf=Slider_afftdn_NFVar,
                                        nt=NtVar.get(),
                                        filtro_speechnorm=filtro_speechnorm.get(),
                                        p=Slider_speechnorm_PVar,
                                        filtro_audio_mono=filtro_audio_mono.get(),
                                        audio_delay=filtro_delay_audio.get(),
                                        audio_delay_ms=Slider_delayaudioVar
                                        )
    Filtros.ouvir()
    #visuaudio(False,entrada.get(),filtro_loudnorm.get(),Slider_loudnorm_target_levelVar,Slider_loudnorm_TPVar,Slider_loudnorm_LRAVar,filtro_afftdn.get(),Slider_afftdn_NRVar,Slider_afftdn_TNVar,Slider_afftdn_TRVar,filtro_speechnorm.get(),Slider_speechnorm_PVar,filtro_audio_mono.get())
  def converter():
    if not entrada.get():
      messagebox.showwarning("Aviso","Arquivos não especificados")
      return
    Filtros = FiltrosAudio.FiltrosAudio(entrada=entrada.get(),
                                        filtro_loudnorm=filtro_loudnorm.get(),
                                        target_level=Slider_loudnorm_target_levelVar,
                                        TP=Slider_loudnorm_TPVar,
                                        LRA=Slider_loudnorm_LRAVar,
                                        filtro_afftdn=filtro_afftdn.get(),
                                        nr=Slider_afftdn_NRVar,
                                        tn=Slider_afftdn_TNVar,
                                        tr=Slider_afftdn_TRVar,
                                        nf=Slider_afftdn_NFVar,
                                        nt=NtVar.get(),
                                        filtro_speechnorm=filtro_speechnorm.get(),
                                        p=Slider_speechnorm_PVar,
                                        filtro_audio_mono=filtro_audio_mono.get(),
                                        audio_delay=filtro_delay_audio.get(),
                                        audio_delay_ms=Slider_delayaudioVar
                                        )
    Filtros.converter()
  
  #CustomWidgets.CustomComboBox(frameouvir,Values=[".wav",".mp3"]).pack(pady=10,anchor="center")
  CustomWidgets.CustomButton(frameouvir,text="Ouvir",dica=Util.quebrar_linhas("Ao especificar mais que um arquivo, você ouvirá o primeiro da fila."),command=ouvir).pack(pady=10,padx=10,side="left")
  CustomWidgets.CustomButton(frameouvir,text="Converter",command=converter).pack(pady=10,padx=10,side="left")
  
  
  
  
  
class AppManager:
    def __init__(self, master, frameaaudio_mono):
        self.master = master
        self.frameaaudio_mono = frameaaudio_mono
        self.app = None
        self.lista_filtros = []

    def addFiltro(self, filtro="", variavel=bool):
        if variavel.get():
            if filtro not in self.lista_filtros:
                self.lista_filtros.append(filtro)
        else:
            if filtro in self.lista_filtros:
                self.lista_filtros.remove(filtro)

        if self.app:
            self.app.destroy()

        self.app = FiltrosAudio.OrdemFiltros(self.frameaaudio_mono, self.lista_filtros)
        self.app.listbox.bind("<Button-1>", self.app.on_drag)
        self.app.pack()

    def listaFiltros(self):
      return self.lista_filtros
