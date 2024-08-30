import tkinter as tk    
from tkinter import ttk
from Util import CustomWidgets, Styles, Util

comando = ""

class ACompressor(ttk.Frame):
  def __init__(self,frame=None):
    super().__init__(frame)
    self.mostrando = False;
    
    self.titulo = CustomWidgets.CustomLabel(frame, text="Paramêtros do ACompressor",font=Styles.fonte_titulo)
    
   
    self.Slider_threshold = CustomWidgets.CustomSliderFloat(frame,from_=0.1,to=1,start=0.5,sufixo="Threshold",dica=Util.quebrar_linhas(""))
    
    self.Slider_ratio = CustomWidgets.CustomSlider(frame,from_=1,to=20,start=10,sufixo="Ratio",dica=Util.quebrar_linhas(""))
    
    self.Slider_attach = CustomWidgets.CustomSliderFloat(frame,from_=0.01,to=2000,start=1000,sufixo="Attach",dica=Util.quebrar_linhas(""))
    
    self.Slider_release = CustomWidgets.CustomSliderFloat(frame,from_=0.01,to=9000,start=1000,sufixo="Release",dica=Util.quebrar_linhas(""))
    
  def apagar(self):
    self.destroy()
  def iniciar(self):
    if self.mostrando == False: self.aparecer()
    else: self.esconder()  
  def aparecer(self):
    self.mostrando=True
    self.titulo.pack()
    self.Slider_threshold.pack(fill="x",expand=True,pady=5)
    self.Slider_ratio.pack(fill="x",expand=True,pady=5)
    self.Slider_attach.pack(fill="x",expand=True,pady=5)
    self.Slider_release.pack(fill="x",expand=True,pady=5)
  def esconder(self):
    self.mostrando = False;
    self.titulo.pack_forget()
    self.Slider_threshold.pack_forget()
    self.Slider_ratio.pack_forget()
    self.Slider_attach.pack_forget()
    self.Slider_release.pack_forget()

      
  
