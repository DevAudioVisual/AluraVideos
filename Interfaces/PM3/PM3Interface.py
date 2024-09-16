from cgitb import text
import math
from multiprocessing import Value
import multiprocessing
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import Main
from Models.PM3 import Pm3Downloader
from Util import Styles, Util
import Util.CustomWidgets as ctk

def InterfacePM3(tabview):
    frame_principal = ctk.CustomScroolabeFrame(tabview.tab("PM3"))
    
    ctk.CustomLabel(frame_principal,text="Digite no campo de texto abaixo,\ntodos os links dos vídeos da PM3 (Google Drive).",font=Styles.fonte_titulo).pack(pady=10, expand=True)
    
    text_widget = ctk.CustomTextbox(frame_principal,wrap="word",width=700,height=500)
    text_widget.pack(fill="both", expand=True)
    
    ctk.CustomLabel(frame_principal,text_color="red",text="ATENÇÃO!\nÉ possível que haja erro de downloads, verifique após o término.",font=Styles.fonte_titulo).pack(pady=10, expand=True)
    
    frame_project_name = ctk.CustomFrame(frame_principal)
    frame_project_name.pack(side="top", expand=True)
    
    ProjectNameVar = tk.StringVar()
    
    ctk.CustomLabel(frame_project_name,text="Nome do projeto:").pack(side="left",padx=10,pady=10, expand=True,fill="x")
    ProjectName = ctk.CustomEntry(frame_project_name,textvariable=ProjectNameVar,width=300)
    ProjectName.pack(side="left",padx=10,pady=10, expand=True,fill="x")
    
    frame_dir = ctk.CustomFrame(frame_principal)
    frame_dir.pack(side="top", expand=True)
    
    DirVar = tk.StringVar(value="")
    def setTextDir():
        dir = filedialog.askdirectory()
        DirVar.set(dir)
    ctk.CustomLabel(frame_dir,text="Diretório de download:").pack(side="left",padx=10,pady=10, expand=True,fill="x")
    ctk.CustomEntry(frame_dir,state="readonly",textvariable=DirVar,width=300).pack(side="left",padx=10,pady=10, expand=True,fill="x")
    ctk.CustomButton(frame_dir,text="Buscar",command=setTextDir).pack(side="left",padx=10,pady=10, expand=True,fill="x")
    
    frame_buttons = ctk.CustomFrame(frame_principal)
    frame_buttons.pack(side="top", expand=True)
    
    def download():
        if DirVar == tk.StringVar(value=""):
            print("Diretório inválido")
            return
        if ProjectName.get() == "":
            print("Nome do projeto inválido")
            return
        def startdownload():
            Pm3Downloader.App(root=Main.InterfaceMain.root,
                filename=text_widget.getTextBox().get("1.0", "end-1c"),
                extract_folder_path=rf"{DirVar.get()}",
                extract_folder_name=Util.sanitize_filename(ProjectName.get()),
                max_workers=max_workers.get_slider_value()).startDownload()
        threading.Thread(target=startdownload,daemon=True).start()
    max_threads = multiprocessing.cpu_count()    
    divide_threads = max_threads / 2
    start_threads = int(math.ceil(divide_threads) if divide_threads % 1 != 0 else divide_threads)
    max_workers = ctk.CustomSlider(frame_buttons,from_=1,to=max_threads,start=start_threads,sufixo="Máximo paralelismo")
    max_workers.pack(side="left",padx=10,pady=10, expand=True,fill="x")
    ctk.CustomButton(frame_buttons,text="Download",command=download).pack(side="left",padx=10,pady=10, expand=True,fill="x")
    
    return frame_principal