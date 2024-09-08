from tkinter import ttk
from Util import CustomWidgets, Styles


class Loudnorm(ttk.Frame):
  def __init__(self,frame=None):
    super().__init__(frame)
    self.mostrando = False;
    
    self.titulo = CustomWidgets.CustomLabel(frame, text="Paramêtros do Lourdnorm",font=Styles.fonte_titulo)
    self.Slider_loudnorm_target_level = CustomWidgets.CustomSliderFloat(frame,from_=-30,to=-5,start=-6,sufixo="Integrated Loudness")
    self.Slider_loudnorm_TP = CustomWidgets.CustomSliderFloat(frame,from_=-9,to=0,start=-1.5,sufixo="True Peak")
    self.Slider_loudnorm_LRA = CustomWidgets.CustomSliderFloat(frame,from_=1,to=20,start=11,sufixo="Loudness Range")
    
  def iniciar(self):
    if self.mostrando == False: self.aparecer()
    else: self.esconder()  
  def aparecer(self):
    self.mostrando=True
    self.titulo.pack()
    self.Slider_loudnorm_LRA.pack(fill="x",expand=True,pady=5)
    self.Slider_loudnorm_TP.pack(fill="x",expand=True,pady=5)
    self.Slider_loudnorm_target_level.pack(fill="x",expand=True,pady=5)
  def esconder(self):
    self.mostrando = False;
    self.titulo.pack_forget()
    self.Slider_loudnorm_LRA.pack_forget()
    self.Slider_loudnorm_TP.pack_forget()
    self.Slider_loudnorm_target_level.pack_forget()
    