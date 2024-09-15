import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from Models.S3 import S3Model
from Util import Styles
import Util.CustomWidgets as ctk

def InterfaceS3(tabview):
    frame_principal = ctk.CustomFrame(tabview.tab("S3"))
    model = S3Model.S3Model()

    def Verify():
      if model.hasToken(): 
        if model.s3_client != None:
          hasCredentials(frame_principal,model)   
        else: 
          startConnection(frame_principal,model)   
      else: 
        noCredentials(frame_principal,model) 
    threading.Thread(target=Verify,daemon=True).start()
    
    return frame_principal
def startConnection(frame_principal,model):
    def limpar():
      for widget in frame_principal.winfo_children():
            widget.destroy()
            frame_principal.update()
    limpar()
    ctk.CustomLabel(frame_principal,font=Styles.fonte_titulo,text="Credenciais encontradas!\n\nIniciar conexão").pack(pady=10)
    def connect():
      limpar()
      hasCredentials(frame_principal,model)
    ctk.CustomButton(frame_principal,text="Conectar",command=lambda: threading.Thread(target=connect,daemon=True).start()).pack(pady=5)
    
def hasCredentials(frame_principal,model):
    if model.setS3Client() == False:
      ctk.CustomLabel(frame_principal,font=Styles.fonte_titulo,text_color="red",text="Erro de contexão ou credenciais inválidas.").pack(pady=10)
      frame = ctk.CustomFrame(frame_principal)
      frame.pack()
      def Reset():
        model.resetCredentials()
        messagebox.showinfo("Info","Credenciais resetadas!")
        for widget in frame_principal.winfo_children():
            widget.destroy()
            frame_principal.update()
        noCredentials(frame_principal,model)
      ctk.CustomButton(frame,text="Registrar novas credenciais",command=Reset).pack(padx=5,pady=10,side="left")
      ctk.CustomButton(frame,text="Tentar novamente",command=lambda: startConnection(frame_principal,model)).pack(padx=5,pady=10,side="left")
      return
    ctk.CustomLabel(frame_principal,font=Styles.fonte_titulo,text="Upload Amazon S3").pack(pady=10)
    
    frame_pastas_s3 = ctk.CustomFrame(frame_principal)
    frame_pastas_s3.pack()
    ctk.CustomLabel(frame_pastas_s3,text="Selecione o diretório dentro do S3").pack(pady=10,padx=5,side="left")
    foldersS3Var = tk.StringVar(value="cursos")
    ctk.CustomComboBox(frame_pastas_s3,Values=model.list_folders_s3(sort=True),variable=foldersS3Var,width=200).pack(pady=10,padx=5,side="left")
    
    frame_pastas = ctk.CustomFrame(frame_principal)
    frame_pastas.pack()
    entryLocalVar = tk.StringVar()
    entryLocal = ctk.CustomEntry(frame_pastas,textvariable=entryLocalVar,width=250)
    entryLocal.pack(pady=10,padx=5,side="left")
    def setLocal():
      dir = filedialog.askdirectory()
      entryLocalVar.set(dir)
    ctk.CustomButton(frame_pastas,text="Buscar",command=setLocal).pack(pady=10,padx=5,side="left")
    
    def upload():
      def t():
        model.upload_folder_to_s3(local_folder_path=entryLocalVar.get(), destination_folder=foldersS3Var.get())
      threading.Thread(target=t,daemon=True).start()
        
    ctk.CustomButton(frame_principal,text="Realizar upload",
                     command=upload).pack(pady=10,padx=5)
      
  
def noCredentials(frame_principal,model):
    ctk.CustomLabel(frame_principal,font=Styles.fonte_titulo,text="Você não possui credenciais associadas ao AluraVideos\n Por favor as associe agora.").pack(pady=10)
    
    frame_secret_key = ctk.CustomFrame(frame_principal)
    frame_secret_key.pack(side="top",padx=5,pady=5)
    ctk.CustomLabel(frame_secret_key,text="Secret Key:").pack(side="left",padx=5,pady=5)
    entry_secret_key = ctk.CustomEntry(frame_secret_key,width=500)
    entry_secret_key.pack(side="left",padx=5,pady=5)
    
    frame_access_key = ctk.CustomFrame(frame_principal)
    frame_access_key.pack(side="top",padx=5,pady=5)
    ctk.CustomLabel(frame_access_key,text="Acess Key:").pack(side="left",padx=5,pady=5)
    entry_access_key = ctk.CustomEntry(frame_access_key,width=500)
    entry_access_key.pack(side="left",padx=5,pady=5)
    
    frame_buttons = ctk.CustomFrame(frame_principal)
    frame_buttons.pack(side="top",padx=5,pady=5)
    def register():
      secret_key = entry_secret_key.get()
      access_key = entry_access_key.get()
      if model.registerCredentials(secret_key=secret_key,access_key=access_key):
          for widget in frame_principal.winfo_children():
            widget.destroy()
          frame_principal.update()
          hasCredentials(frame_principal,model)
    ctk.CustomButton(frame_buttons,text="Registrar",command=register).pack(pady=5)