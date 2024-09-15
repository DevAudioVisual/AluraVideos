from tkinter import messagebox, ttk
import Util.Util as Util;
import customtkinter as ctk
import tkinter as tk
import Util.CustomWidgets as CustomWidgets
import Models.EditorAudio.FiltrosAudio as FiltrosAudio
from tkinter import filedialog
import Util.Styles as Styles
from Models.EditorAudio.Efeitos import ACompressor, ALimiter, Afftdn, AudioDelay, AudioMono, Loudnorm, Speechnorm



def abrirConfigAudio(tabview):
  
  frame = CustomWidgets.CustomScroolabeFrame(tabview.tab("Audio"))
  
  framebotoes = CustomWidgets.CustomFrame(frame)
  framebotoes.pack(side="top")
  
  frameEfeitos = CustomWidgets.CustomFrame(frame)
  frameEfeitos.pack(side="top")



  
  
  
  frameouvir = CustomWidgets.CustomFrame(frame)
  frameouvir.pack(side="bottom",anchor="center")

  #global app_manager
  #app_manager = AppManager(frameOrdem)
  
  global lista
  lista = EscolherFiltros(frameEfeitos)

  global entry
  diretorio = tk.StringVar()
  entry = CustomWidgets.CustomEntry(framebotoes,textvariable=diretorio,width=500)
  def dic():
    lista.setDirectory()
    diretorio.set(lista.entrada.get())

  CustomWidgets.CustomLabel(framebotoes,text="Arquivos:",font=Styles.fonte_titulo).pack(pady=10,padx=10,fill="x")  
  CustomWidgets.CustomButton(framebotoes,text="Buscar",dica=Util.quebrar_linhas("Selecione os arquivos que deseja editar o audio."),Image=CustomWidgets.CustomImage("folder.png",20,20),command=dic).pack(pady=10,padx=10,side="right")
  entry.pack(pady=10)
  lista.pack(pady=10)
  
  
  global mostrarGrafico
  mostrarGrafico = tk.BooleanVar(value=False)
  #CustomWidgets.CustomCheckBox(frameouvir,text="Mostrar gráfico de DB's",variable=mostrarGrafico).pack(pady=10,padx=10,side="left")
  CustomWidgets.CustomButton(frameouvir,text="Ouvir",dica=Util.quebrar_linhas("Ao especificar mais que um arquivo, você ouvirá o primeiro da fila."),command=lista.ouvir).pack(pady=10,padx=10,side="left")
  CustomWidgets.CustomButton(frameouvir,text="Converter",command=lista.converter).pack(pady=10,padx=10,side="left")
  
  return frame

  
def dicafiltro(item):  
  dica_para_filtro = {
    "Loudnorm": Util.quebrar_linhas("Loudnorm é um filtro de normalização de audio, assemelhando-se ao levelator. Com ele você nivelará todas as frequências."),
    "Afftdn": Util.quebrar_linhas("Redutor de ruído"),
    "Speechnorm": Util.quebrar_linhas("Speechhorn é um filtro que se assemelha ao Loudnorm, porém ele tentará elevar apenas as frequências de dialogo.")
  }  
  return dica_para_filtro.get(item, "Descrição não encontrada") 
class EscolherFiltros(ttk.Frame):
    def __init__(self, master=None,):
      super().__init__(master)
      self.master = master
      self.entrada = None
      self.listaTotal = None
      self.arquivos = None
      
      self.FrameLista = CustomWidgets.CustomFrame(master)
      self.FrameLista.pack(side="left",anchor="n",fill="y",padx=20,pady=10,expand=True)
      
      self.FrameOrdem = CustomWidgets.CustomFrame(master)
      self.FrameOrdem.pack(side="left",anchor="n",fill="y",padx=20,pady=10,expand=True)
      
      self.FrameParametros = CustomWidgets.CustomFrame(master)
      self.FrameParametros.pack(side="left",anchor="n",fill="y",padx=20,pady=10,expand=True)
      
      self.app_manager = AppManager(self.FrameOrdem)
      
      self.config(style="Custom.TFrame")
      
      self.filtros = []
      for filtro,metodo in getFiltros():
        self.filtros.append(str(filtro))
      self.filtros.sort()
      self.filtro_escolhido = tk.StringVar()

      #self.Lista =  AutocompleteEntryListbox(self.FrameLista,text="Entry + Listbox with autocompletion for the Tk instance's methods:")
      self.Label = CustomWidgets.CustomLabel(self.FrameLista,text="Lista de efeitos",font=Styles.fonte_titulo)
      self.Label.pack()
      self.Label2 = CustomWidgets.CustomLabel(self.FrameLista,text="(Clique para ativar)\n\n\n\n\n",font=Styles.fonte_input)
      self.Label2.pack()
      
      self.entry = CustomWidgets.CustomList(self.FrameLista,completevalues=self.filtros,pack=True)
      self.entry.pack()      
      
      self.tooltip = Tooltip(self.entry.listbox)
      def on_item_leave(event):
        self.tooltip.hidetip()
      def on_item_hover(event):
        widget = event.widget
        index = widget.nearest(event.y)
        item = widget.get(index)
        dica = dicafiltro(item)
        self.tooltip.showtip(dica)
        #print(f"Mouse is over: {dicafiltro(item)}")
      def on_item_selected(event):
        try:
          selected_index = event.widget.curselection()[0]
          selected_item = event.widget.get(selected_index)
          self.filtro_escolhido.set(selected_item)
          #print(selected_item)
          self.adicionar()
        except IndexError:
          pass
        # Nenhum item selecionado, lidar com o erro
      self.entry.getList().listbox.bind("<<ListboxSelect>>", on_item_selected)      
      self.entry.getList().listbox.bind("<Motion>", on_item_hover)          
      self.entry.listbox.bind("<Leave>", on_item_leave)             
           
  
      self.FiltrosAudio = None
      
      self.Loudnorm = None
      self.Speechnorm = None
      self.Afftdn = None
      self.AudioMono = None
      self.AudioDelay = None
      self.ACompressor = None
      self.ALimiter = None
      
      self.filtros_escolhidos_lista =  []
    def adicionar(self):
      if not self.filtro_escolhido.get():
        print("nenhum filtro")
        return
      if self.filtro_escolhido.get() in self.filtros_escolhidos_lista: 
        return
      
      self.filtros_escolhidos_lista.append(self.filtro_escolhido.get()) 
        
        
        
      if self.filtro_escolhido.get() == "Loudnorm": 
        if not self.Loudnorm: self.Loudnorm = Loudnorm.Loudnorm(self.FrameParametros)
      if self.filtro_escolhido.get() == "Speechnorm":
        if not self.Speechnorm: self.Speechnorm = Speechnorm.Speechnorm(self.FrameParametros)
      if self.filtro_escolhido.get() == "Afftdn":
        if not self.Afftdn: self.Afftdn = Afftdn.Afftdn(self.FrameParametros)
      if self.filtro_escolhido.get() == "AudioMono":
        if not self.AudioMono: self.AudioMono = AudioMono.AudioMono(self.FrameParametros)
      if self.filtro_escolhido.get() == "AudioDelay":
        if not self.AudioDelay: self.AudioDelay = AudioDelay.AudioDelay(self.FrameParametros)
      if self.filtro_escolhido.get() == "ACompressor":
        if not self.ACompressor: self.ACompressor = ACompressor.ACompressor(self.FrameParametros)
      if self.filtro_escolhido.get() == "ALimiter":
        if not self.ALimiter: self.ALimiter = ALimiter.ALimiter(self.FrameParametros)
      
      
      

      self.app_manager.addFiltro(str(self.filtro_escolhido.get()),tk.BooleanVar(value=self.filtro_escolhido.get() in self.filtros_escolhidos_lista))      
      print(self.app_manager.listaFiltros()) 
    def ouvir(self):
      if not self.entrada:
        messagebox.showwarning("Aviso","Nenhum arquivo escolhido")
        return
      if not self.filtros_escolhidos_lista:
        messagebox.showwarning("Aviso","Nenhum filtro escolhido")
        return
      self.build()
      self.FiltrosAudio.ouvir()
    def converter(self):
      if not self.entrada:
        messagebox.showwarning("Aviso","Nenhum arquivo escolhido")
        return
      if not self.filtros_escolhidos_lista:
        messagebox.showwarning("Aviso","Nenhum filtro escolhido")
        return
      #for a in self.arquivos:
      self.build()
      for a in self.arquivos:
        #print("Convertendo: ", a)
        self.FiltrosAudio.converter(a)    
      
    def build(self):
        self.FiltrosAudio = FiltrosAudio.FiltrosAudio(
        filtro_loudnorm = tk.BooleanVar(value=True).get() if self.Loudnorm is not None else tk.BooleanVar(value=False).get(),
        filtro_afftdn = tk.BooleanVar(value=True).get() if self.Afftdn is not None else tk.BooleanVar(value=False).get(),
        filtro_speechnorm = tk.BooleanVar(value=True).get() if self.Speechnorm is not None else tk.BooleanVar(value=False).get(),
        filtro_audio_mono = tk.BooleanVar(value=True).get() if self.AudioMono is not None else tk.BooleanVar(value=False).get(),
        audio_delay = tk.BooleanVar(value=True).get() if self.AudioDelay is not None else tk.BooleanVar(value=False).get(),
        filtro_acompressor = tk.BooleanVar(value=True).get() if self.ACompressor is not None else tk.BooleanVar(value=False).get(),
        filtro_alimiter = tk.BooleanVar(value=True).get() if self.ALimiter is not None else tk.BooleanVar(value=False).get(),
        
        target_level=self.Loudnorm.Slider_loudnorm_target_level.get_slider_value() if self.Loudnorm else None,
        TP=self.Loudnorm.Slider_loudnorm_TP.get_slider_value() if self.Loudnorm else None,
        LRA=self.Loudnorm.Slider_loudnorm_LRA.get_slider_value() if self.Loudnorm else None,
        
        nf = self.Afftdn.Slider_afftdn_NF.get_slider_value() if self.Afftdn else None,
        nr = self.Afftdn.Slider_afftdn_NR.get_slider_value() if self.Afftdn else None,
        nt = str(self.Afftdn.comboboxVar.get()) if self.Afftdn else None,
        tn = self.Afftdn.tnVar.get() if self.Afftdn else None,
        tr = self.Afftdn.trVar.get() if self.Afftdn else None,
        om = self.Afftdn.omVar.get() if self.Afftdn else None,
        
        p = self.Speechnorm.Slider_speechnorm_P.get_slider_value() if self.Speechnorm else None,
        t = self.Speechnorm.Slider_speechnorm_T.get_slider_value() if self.Speechnorm else None,
        
        audio_delay_ms=self.AudioDelay.Slider_delayaudio.get_slider_value() if self.AudioDelay else None,
        
        acompressor_threshold=self.ACompressor.Slider_threshold.get_slider_value() if self.ACompressor else None,
        acompressor_ratio=self.ACompressor.Slider_ratio.get_slider_value() if self.ACompressor else None,
        acompressor_attack=self.ACompressor.Slider_attach.get_slider_value() if self.ACompressor else None,
        acompressor_release=self.ACompressor.Slider_release.get_slider_value() if self.ACompressor else None,
        
        alimiter_level_in = self.ALimiter.Slider_level_in.get_slider_value(),
        alimiter_level_out = self.ALimiter.Slider_level_out.get_slider_value(),
        alimiter_limit = self.ALimiter.Slider_limit.get_slider_value(),
        alimiter_attack = self.ALimiter.Slider_attack.get_slider_value(),
        alimiter_release = self.ALimiter.Slider_release.get_slider_value(),
        alimiter_asc = self.ALimiter.ascVar.get(),
        alimiter_asc_level = self.ALimiter.Slider_asc_level.get_slider_value(),
        alimiter_level = self.ALimiter.levelVar.get(),
        alimiter_latency = self.ALimiter.LatencyVar.get(),
        )
    def getAppManager(self):
      return self.app_manager    
    def getEntrada(self):
      return self.entrada
    def setDirectory(self):
      self.entrada = ctk.StringVar(value=None)
      self.arquivos = []
      self.arquivo = filedialog.askopenfiles()
      #self.a = filedialog.askopenfile()
      #self.entrada.set(self.a.name)
      self.entrada.set(self.arquivo[0].name)
      for a in self.arquivo:     
        self.arquivos.append(a.name)        
        
class AppManager:
    def __init__(self, master):
        self.master = master
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

        self.app = FiltrosAudio.OrdemFiltros(self.master, self.lista_filtros)
        self.app.listbox.bind("<Button-1>", self.app.on_drag)
        self.app.pack(side="left")
    def listaFiltros(self):
      return self.lista_filtros







class Tooltip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def showtip(self, text):
        if self.tip_window or not text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.overrideredirect(True)  # Sem bordas
        #tw.withdraw()  # Esconde inicialmente
        tw.config(borderwidth=1)
        tw.config(background=Styles.cor_botao)   
        label = ctk.CTkLabel(tw,
                                    text="  "+text,
                                    font=Styles.fonte_input,
                                    bg_color=Styles.cor_botao,
                                    fg_color=Styles.cor_botao,
                                    text_color="white",
                                    text_color_disabled="white"
                                    #image=CustomImage("help.ico",25,25),
                                    #compound="left",
                                    )
        label.pack(padx=5, pady=5)

    def hidetip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

class Drag_and_Drop_Listbox(tk.Listbox):
    """ A Tkinter listbox with drag & drop reordering of lines """
    def __init__(self, master, **kw):
        kw['selectmode'] = tk.EXTENDED
        tk.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<Control-1>', self.toggleSelection)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.bind('<Leave>',  self.onLeave)
        self.bind('<Enter>',  self.onEnter)
        self.selectionClicked = False
        self.left = False
        self.unlockShifting()
        self.ctrlClicked = False
    def orderChangedEventHandler(self):
        pass

    def onLeave(self, event):
        # prevents changing selection when dragging
        # already selected items beyond the edge of the listbox
        if self.selectionClicked:
            self.left = True
            return 'break'
    def onEnter(self, event):
        self.left = False

    def setCurrent(self, event):
        self.ctrlClicked = False
        i = self.nearest(event.y)
        self.selectionClicked = self.selection_includes(i)
        if (self.selectionClicked):
            return 'break'

    def toggleSelection(self, event):
        self.ctrlClicked = True

    def moveElement(self, source, target):
        if not self.ctrlClicked:
            element = self.get(source)
            self.delete(source)
            self.insert(target, element)

    def unlockShifting(self):
        self.shifting = False
    def lockShifting(self):
        # prevent moving processes from disturbing each other
        # and prevent scrolling too fast
        # when dragged to the top/bottom of visible area
        self.shifting = True

    def shiftSelection(self, event):
        if self.ctrlClicked:
            return
        selection = self.curselection()
        if not self.selectionClicked or len(selection) == 0:
            return

        selectionRange = range(min(selection), max(selection))
        currentIndex = self.nearest(event.y)

        if self.shifting:
            return 'break'

        lineHeight = 15
        bottomY = self.winfo_height()
        if event.y >= bottomY - lineHeight:
            self.lockShifting()
            self.see(self.nearest(bottomY - lineHeight) + 1)
            self.master.after(500, self.unlockShifting)
        if event.y <= lineHeight:
            self.lockShifting()
            self.see(self.nearest(lineHeight) - 1)
            self.master.after(500, self.unlockShifting)

        if currentIndex < min(selection):
            self.lockShifting()
            notInSelectionIndex = 0
            for i in selectionRange[::-1]:
                if not self.selection_includes(i):
                    self.moveElement(i, max(selection)-notInSelectionIndex)
                    notInSelectionIndex += 1
            currentIndex = min(selection)-1
            self.moveElement(currentIndex, currentIndex + len(selection))
            self.orderChangedEventHandler()
        elif currentIndex > max(selection):
            self.lockShifting()
            notInSelectionIndex = 0
            for i in selectionRange:
                if not self.selection_includes(i):
                    self.moveElement(i, min(selection)+notInSelectionIndex)
                    notInSelectionIndex += 1
            currentIndex = max(selection)+1
            self.moveElement(currentIndex, currentIndex - len(selection))
            self.orderChangedEventHandler()
        self.unlockShifting()
        return 'break'



def getFiltros(): 
  try:
    Filtros = {
          "Speechnorm": lista.Speechnorm if lista is not None else "",
          "Afftdn": lista.Afftdn if lista is not None else "",
          "Loudnorm": lista.Loudnorm if lista is not None else "",
          "AudioMono": lista.AudioMono if lista is not None else "",
          "AudioDelay": lista.AudioDelay if lista is not None else "",
          "ACompressor": lista.ACompressor if lista is not None else "",
          "ALimiter": lista.ALimiter if lista is not None else "",
          }
  except Exception as e:
        # Se ocorrer um erro, define valores padrão
        Filtros = {
            "Speechnorm": "",
            "Afftdn": "",
            "Loudnorm": "",
            "AudioMono": "",
            "AudioDelay": "",
            "ACompressor": "",
            "ALimiter": ""
        }
  return Filtros.items()
