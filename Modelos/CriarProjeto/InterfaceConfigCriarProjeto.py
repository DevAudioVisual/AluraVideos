import json
import re
import tkinter as tk
from tkinter import filedialog
import Config.LoadConfigCriarProjeto as LoadConfig;
import customtkinter as ctk
from Config import InterfaceConfigEditor
from Util import Styles
from Util import CustomWidgets

def ConfigCriarProjetoInterface(tabview):
    config_data = LoadConfig.load_config()

    framePrincipal = ctk.CTkFrame(tabview.tab("Config Criar projeto"), bg_color=Styles.cor_fundo, fg_color=Styles.cor_fundo)
    framePrincipal.pack(side="top",fill="both",pady=10)
    
    CustomWidgets.CustomLabel(framePrincipal,text="Predefinição para criar projetos",font=Styles.fonte_titulo).pack()

    frameDiretorios = ctk.CTkFrame(tabview.tab("Config Criar projeto"), bg_color=Styles.cor_fundo, fg_color=Styles.cor_fundo)
    frameDiretorios.pack(side="top",fill="both",pady=10)

    frame = ctk.CTkFrame(tabview.tab("Config Criar projeto"), bg_color=Styles.cor_fundo, fg_color=Styles.cor_fundo)
    frame.pack(side="left",fill="both",padx=10)
    
    frame2 = ctk.CTkFrame(tabview.tab("Config Criar projeto"), bg_color=Styles.cor_fundo, fg_color=Styles.cor_fundo)
    frame2.pack(side="left",fill="both",padx=10)
    
    frame3 = ctk.CTkFrame(tabview.tab("Config Criar projeto"), bg_color=Styles.cor_fundo, fg_color=Styles.cor_fundo)
    frame3.pack(side="left",fill="both",padx=10)
    global diretorio_padrao
    diretorio_padrao = tk.StringVar(value=config_data.get("diretorio_padrao"))

    
    CustomWidgets.CustomLabel(frameDiretorios,text="Diretório padrão do projeto").pack(side="left")
            
    CustomWidgets.CustomEntry(frameDiretorios, textvariable=diretorio_padrao, width=300).pack(side="left",padx=10)
    def escolherDir():
        dirr = filedialog.askdirectory()     
        diretorio_padrao.set(dirr) 
        update_config_from_widgets()
        InterfaceConfigEditor.editor_window.focus()
    CustomWidgets.CustomButton(frameDiretorios, text="Buscar",Image=CustomWidgets.CustomImage("folder.png",20,20),command=escolherDir).pack(side="left")
    
    
    global checks_vars, sub_pastas_vars, fechar_ao_criar
    
    fechar_ao_criar = tk.BooleanVar(value=config_data.get("fechar_ao_criar", True))
    
    
    checks_vars = {key: tk.BooleanVar(value=value) for key, value in config_data.get("checks", [{}])[0].items()}
    sub_pastas_vars = {key: tk.BooleanVar(value=value) for key, value in config_data.get("subpastas", [{}])[0].items()}
    
    global text_area_editor
    text_area_editor = tk.Text(frame, wrap='word', width=50, height=15)
    
    def update_config_from_widgets():
        config_data = {
            "fechar_ao_criar": fechar_ao_criar.get(),
            "diretorio_padrao": diretorio_padrao.get(),
            "checks": [{key: var.get() for key, var in checks_vars.items()}],
            "subpastas": [{key: var.get() for key, var in sub_pastas_vars.items()}]
        }
        
        text_area_editor.delete("1.0", tk.END)
        text_area_editor.insert(tk.END, json.dumps(config_data, indent=4))
    
    CustomWidgets.CustomLabel(frame,text="Processos",font=Styles.fonte_titulo).pack(fill="both",pady=10)
    for key, var in checks_vars.items():
        CustomWidgets.CustomCheckBox(frame, key, var, update_config_from_widgets).pack(fill="both",pady=10)
        
    CustomWidgets.CustomLabel(frame2,text="Sub-pastas",font=Styles.fonte_titulo).pack(fill="both",pady=10)
    for key, var in sub_pastas_vars.items():
        CustomWidgets.CustomCheckBox(frame2, key, var, update_config_from_widgets).pack(fill="both",pady=10)
  
    CustomWidgets.CustomLabel(frame3,text="Fechar ao criar",font=Styles.fonte_titulo).pack(fill="both",pady=10)
    fechar_ao_criar_checkbox = CustomWidgets.CustomCheckBox(frame3, "Fechar ao Criar", fechar_ao_criar, update_config_from_widgets)
    fechar_ao_criar_checkbox.pack(fill="both")
