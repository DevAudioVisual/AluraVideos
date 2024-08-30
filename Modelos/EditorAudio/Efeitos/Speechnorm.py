  
from tkinter import ttk

from Util import CustomWidgets, Styles


class Speechnorm(ttk.Frame):
  def __init__(self,frame=None):
    super().__init__(frame)
    self.mostrando = False;
    
    self.titulo = CustomWidgets.CustomLabel(frame, text="Paramêtros do Speechnorm",font=Styles.fonte_titulo)
    self.Slider_speechnorm_P = CustomWidgets.CustomSliderFloat(frame,from_=0,to=1,start=1,sufixo="Normalização")
    self.Slider_speechnorm_T = CustomWidgets.CustomSliderFloat(frame,from_=0,to=1,start=1,sufixo="Limiar")
    
  def iniciar(self):
    if self.mostrando == False: self.aparecer()
    else: self.esconder()  
  def aparecer(self):
    self.mostrando=True
    self.titulo.pack(fill="x",expand=True)
    self.Slider_speechnorm_P.pack(fill="x",expand=True,pady=5)
    self.Slider_speechnorm_T.pack(fill="x",expand=True,pady=5)
  def esconder(self):
    self.mostrando = False;
    self.titulo.pack_forget()
    self.Slider_speechnorm_P.pack_forget()
    self.Slider_speechnorm_T.pack_forget()

      
  
