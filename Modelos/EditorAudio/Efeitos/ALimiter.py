import tkinter as tk    
from tkinter import ttk
from Util import CustomWidgets, Styles, Util

comando = ""

class ALimiter(ttk.Frame):
  def __init__(self,frame=None):
    super().__init__(frame)
    self.mostrando = False;
    
    self.titulo = CustomWidgets.CustomLabel(frame, text="Paramêtros do ALimiter",font=Styles.fonte_titulo)
    
   
    self.Slider_level_in = CustomWidgets.CustomSliderFloat(frame,from_=0.02,to=6.0,start=3.0,sufixo="Level In",dica=Util.quebrar_linhas(""))
    
    self.Slider_level_out = CustomWidgets.CustomSliderFloat(frame,from_=0.02,to=6.0,start=3.0,sufixo="Level Out",dica=Util.quebrar_linhas(""))
    
    self.Slider_limit = CustomWidgets.CustomSliderFloat(frame,from_=0.07,to=1.0,start=0.5,sufixo="Limit",dica=Util.quebrar_linhas(""))
    
    self.Slider_attack = CustomWidgets.CustomSliderFloat(frame,from_=0.1,to=80.0,start=0.1,sufixo="Attack",dica=Util.quebrar_linhas(""))
    
    self.Slider_release = CustomWidgets.CustomSliderFloat(frame,from_=1.0,to=8000.0,start=1.0,sufixo="Release",dica=Util.quebrar_linhas(""))
    
    self.ascVar = tk.IntVar(value=0)
    self.asc = CustomWidgets.CustomCheckBox(frame,text="Asc",variable=self.ascVar)
    
    self.Slider_asc_level = CustomWidgets.CustomSliderFloat(frame,from_=0.0,to=1.0,start=0.0,sufixo="Asc Level",dica=Util.quebrar_linhas(""))
    
    self.levelVar = tk.IntVar(value=0)
    self.level = CustomWidgets.CustomCheckBox(frame,text="Level",variable=self.levelVar)
    
    self.LatencyVar = tk.IntVar(value=0)
    self.Latency = CustomWidgets.CustomCheckBox(frame,text="Latency",variable=self.LatencyVar)
    
  def apagar(self):
    self.destroy()
  def iniciar(self):
    if self.mostrando == False: self.aparecer()
    else: self.esconder()  
  def aparecer(self):
    self.mostrando=True
    self.titulo.pack()
    self.Slider_level_in.pack(fill="x",expand=True,pady=5)
    self.Slider_level_out.pack(fill="x",expand=True,pady=5)
    self.Slider_limit.pack(fill="x",expand=True,pady=5)
    self.Slider_attack.pack(fill="x",expand=True,pady=5)
    self.Slider_release.pack(fill="x",expand=True,pady=5)
    self.asc.pack(fill="x",expand=True,pady=5)
    self.Slider_asc_level.pack(fill="x",expand=True,pady=5)
    self.level.pack(fill="x",expand=True,pady=5)
    self.Latency.pack(fill="x",expand=True,pady=5)
  def esconder(self):
    self.mostrando = False;
    self.titulo.pack_forget()
    self.Slider_level_in.pack_forget()
    self.Slider_level_out.pack_forget()
    self.Slider_limit.pack_forget()
    self.Slider_attack.pack_forget()
    self.Slider_release.pack_forget()
    self.asc.pack_forget()
    self.Slider_asc_level.pack_forget()
    self.level.pack_forget()
    self.Latency.pack_forget()

      
  
