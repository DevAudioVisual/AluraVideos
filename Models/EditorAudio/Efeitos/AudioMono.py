from tkinter import ttk

class AudioMono(ttk.Frame):
  def __init__(self,frame=None):
    super().__init__(frame)
    self.mostrando = False;
 
  def iniciar(self):
    if self.mostrando == False: self.aparecer()
    else: self.esconder()  
  def aparecer(self):
    self.mostrando=True
  def esconder(self):
    self.mostrando = False;