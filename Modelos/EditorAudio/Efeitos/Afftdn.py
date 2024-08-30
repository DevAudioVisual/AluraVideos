import tkinter as tk    
from tkinter import ttk
from Util import CustomWidgets, Styles, Util


class Afftdn(ttk.Frame):
  def __init__(self,frame=None):
    super().__init__(frame)
    self.mostrando = False;
    
    self.titulo = CustomWidgets.CustomLabel(frame, text="Paramêtros do Afftdn",font=Styles.fonte_titulo)
    self.Slider_afftdn_NF = CustomWidgets.CustomSliderFloat(frame,from_=-80,to=-20,start=-25,sufixo="Noise Floor",dica=Util.quebrar_linhas("Define o nível de ruído de fundo em decibéis (dB) que você deseja reduzir. Valores negativos indicam que o ruído está abaixo do nível do sinal desejado. Quanto mais negativo o valor, mais agressiva será a redução de ruído."))
    self.Slider_afftdn_NR = CustomWidgets.CustomSliderFloat(frame,from_=0.01,to=97,start=22,sufixo="Noise Reduction",dica=Util.quebrar_linhas("Controla a quantidade de redução de ruído aplicada em decibéis (dB). Valores mais altos resultam em maior redução, mas podem afetar a qualidade do áudio."))    
    self.comboboxVar = tk.StringVar(value="w")
    self.combobox = CustomWidgets.CustomComboBox(frame,textLabel="Noise Type",pack=True,Values=["w","v"],variable=self.comboboxVar,dica="Noise Type: Especifica o tipo de ruído a ser reduzido.\nw: Ruído branco (espectro plano)\nv: Ruído variável (combinação de diferentes tipos)") 
    self.omVar = tk.StringVar(value="o")
    self.om = CustomWidgets.CustomComboBox(frame,pack=True,textLabel="Saida de áudio",Values=["o","n"],variable=self.omVar,dica="") 
    self.tnVar = tk.StringVar()
    self.tnCheck = CustomWidgets.CustomCheckBox(frame,text="threshold noise",variable=self.tnVar)
    self.trVar = tk.StringVar()
    self.trCheck = CustomWidgets.CustomCheckBox(frame,text="threshold reduction",variable=self.trVar)
    #self.Slider_afftdn_TN = CustomWidgets.CustomSliderFloat(frame,from_=0,to=100,start=1,sufixo="Threshold",dica=Util.quebrar_linhas("Define o limiar de ruído em relação ao nível do sinal. Valores mais altos significam que o filtro será mais agressivo na redução de ruído, mas também pode afetar o sinal original."))    
    #self.Slider_afftdn_TR = CustomWidgets.CustomSliderFloat(frame,from_=0,to=100,start=0,sufixo="Threshold Ratio",dica=Util.quebrar_linhas("Define a proporção entre o limiar de ruído e o nível do sinal. Valores mais altos significam que o filtro será mais sensível a pequenas variações no nível de ruído."))
  def apagar(self):
    self.destroy()
  def iniciar(self):
    if self.mostrando == False: self.aparecer()
    else: self.esconder()  
  def aparecer(self):
    self.mostrando=True
    self.titulo.pack()
    self.Slider_afftdn_NF.pack(fill="x",expand=True,pady=5)
    self.Slider_afftdn_NR.pack(fill="x",expand=True,pady=5)
    self.combobox.pack(fill="x",expand=True,pady=5)
    self.tnCheck.pack(fill="x",expand=True,pady=5)
    self.trCheck.pack(fill="x",expand=True,pady=5)
    self.om.pack()
  def esconder(self):
    self.mostrando = False;
    self.titulo.pack_forget()
    self.Slider_afftdn_NF.pack_forget()
    self.Slider_afftdn_NR.pack_forget()
    self.combobox.pack_forget()
    self.tnCheck.pack_forget()
    self.trCheck.pack_forget()
    self.om.pack_forget()

      
  
