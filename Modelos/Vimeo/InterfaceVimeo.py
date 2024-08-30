import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import Interface
import Util.CustomWidgets as CustomWidgets
import Util.Styles as Styles

def InterfaceVimeo(tabview):
    frame = ttk.Frame(tabview.tab("Vimeo"), style="Custom.TFrame")
    frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    tabview.tab("Vimeo").rowconfigure(0, weight=1)
    tabview.tab("Vimeo").rowconfigure(1, weight=1)
    tabview.tab("Vimeo").rowconfigure(2, weight=1)
    tabview.tab("Vimeo").rowconfigure(3, weight=1)
    tabview.tab("Vimeo").columnconfigure(0, weight=1)
    tabview.tab("Vimeo").columnconfigure(1, weight=1)  

    CustomWidgets.CustomLabel(frame,text="Nome da showcase:",font=Styles.fonte_titulo,pack=True).pack()
    
    variavel = ctk.StringVar()
    CustomWidgets.CustomEntry(frame,textvariable=variavel,width=500,pack=True).pack()
    
    CustomWidgets.CustomLabel(frame,text="Diretório dos vídeos",font=Styles.fonte_titulo,pack=True).pack()
    
    CustomWidgets.CustomButton(frame,text="Buscar",pack=True).pack(pady=20)
    
    CustomWidgets.CustomButton(frame,text="Subir",pack=True).pack()
    
    
    
    