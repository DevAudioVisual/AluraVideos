from tkinter import ttk
from Util import CustomWidgets, Styles


class AudioDelay(ttk.Frame):
  def __init__(self,frame=None):
    super().__init__(frame)
    self.mostrando = False;
    
    self.titulo = CustomWidgets.CustomLabel(frame, text="Paramêtros do Audio Delay",font=Styles.fonte_titulo)
    self.Slider_delayaudio = CustomWidgets.CustomSlider(frame,from_=0,to=10000,start=0,sufixo="MS")
    
  def iniciar(self):
    if self.mostrando == False: self.aparecer()
    else: self.esconder()  
  def aparecer(self):
    self.mostrando=True
    self.titulo.pack()
    self.Slider_delayaudio.pack(fill="x",expand=True,pady=5)
  def esconder(self):
    self.mostrando = False;
    self.titulo.pack_forget()
    self.Slider_delayaudio.pack_forget()