import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from Modelos.ValidarVideos import ValidarVideos
import Util.Styles as Styles
import Util.CustomWidgets as CustomWidgets

def interfaceValidador(tabview):

    frame = CustomWidgets.CustomFrame(tabview.tab("Validador"))
    #frame.pack()
    
    CustomWidgets.CustomLabel(frame,text="Vídeo referência:",font=Styles.fonte_titulo).pack(fill="x")
    
    frame_ref = CustomWidgets.CustomFrame(frame)
    frame_ref.pack(fill="x")
    
    ReferenciaVar = tk.StringVar()
    
    def buscarRef():
      dire = filedialog.askopenfile()
      ReferenciaVar.set(dire.name)
    
    CustomWidgets.CustomEntry(frame_ref,textvariable=ReferenciaVar,width=400).pack(side="left",padx=10,pady=10,fill="x")
    CustomWidgets.CustomButton(frame_ref,text="Buscar",command=buscarRef,Image=CustomWidgets.CustomImage("folder.png",20,20)).pack(side="left",fill="x")
    
    CustomWidgets.CustomLabel(frame,text="Pasta de vídeos:",font=Styles.fonte_titulo).pack(fill="x")
    
    frame_folder = CustomWidgets.CustomFrame(frame)
    frame_folder.pack(fill="x")
    
    FolderVar = tk.StringVar()
    def buscarFolder():
      dire = filedialog.askdirectory()
      FolderVar.set(dire)
      
    CustomWidgets.CustomEntry(frame_folder,textvariable=FolderVar,width=400).pack(side="left",padx=10,pady=10,fill="x")
    CustomWidgets.CustomButton(frame_folder,text="Buscar",command=buscarFolder,Image=CustomWidgets.CustomImage("folder.png",20,20)).pack(side="left",fill="x")
    
    CustomWidgets.CustomLabel(frame,text="Monitorar:",font=Styles.fonte_titulo).pack(pady=10,fill="x")
    
    Flags = [
      "Enquadramento",
      "Framerate",
      "Cor",
      "Iluminação",
      "Audio Clipping",
      "Média do audio",
      "Maximo do audio", 
    ]
    row = 0
    column = 0
    frameCheckBoxes = CustomWidgets.CustomFrame(frame)
    frameCheckBoxes.pack(fill="x")
    for f in Flags:
      if row == 3:
        row = 0
        column +=1
      row +=1
      CustomWidgets.CustomCheckBox(frameCheckBoxes,text=f).grid(sticky="w",padx=10,pady=10,row=row,column=column)
    
    CustomWidgets.CustomLabel(frame,text="Lado do instrutor:",font=Styles.fonte_titulo).pack(pady=10,fill="x")
    LadoVar = tk.StringVar()
    CustomWidgets.CustomSegmentedButton(frame,values=["Esquerda","Meio","Direita"],segemented_button_var=LadoVar).pack(pady=10,fill="x")
    
    def Validar():
      def v():
        app = ValidarVideos.app(ref_video=rf"{ReferenciaVar.get()}",analise_videos_dir=rf"{FolderVar.get()}")
        app.Validar()
      thread = threading.Thread(target=v)
      thread.daemon = True
      thread.start()  
      messagebox.showinfo("Aviso","Iniciando a validação, aguarde.")
        
    CustomWidgets.CustomButton(frame, text="Iniciar",dica="",width=200, command=Validar,pack=True).pack(pady=20)
    
    return frame

