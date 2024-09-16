import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import Util.CustomWidgets as ctk
import Util.Styles as Styles

def InterfaceVimeo(tabview):
    frame_principal = ctk.CustomFrame(tabview.tab("Vimeo"))
    
    ctk.CustomLabel(frame_principal,font=Styles.fonte_titulo,text="Em desenvolvimento.").pack()
    
    return frame_principal
    
    
    