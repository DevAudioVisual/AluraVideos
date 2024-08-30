import subprocess
import sys
import tkinter as tk
import json
import Config.LoadConfigCache as LoadConfigCache
from Modelos.Atalhos import InterfaceConfigAtalhos
import Modelos.Interface.Interface as Interface
import customtkinter as ctk
import Modelos.LimparCache.InterfaceConfigLimparcache as InterfaceLimparcache
from Util import CustomWidgets, Util,Styles
from tkinter import messagebox, messagebox
from Modelos.CriarProjeto import InterfaceConfigCriarProjeto as InterfaceCriarprojeto
from Config import LoadConfigAtalhos, LoadConfigCriarProjeto, LoadConfigInterface
from Modelos.Interface import InterfaceConfigInterface

            
def save_and_close():
    new_config_LimparCache = InterfaceLimparcache.text_area_editor.get("1.0", tk.END).strip()
    #new_config_CriarProjeto = InterfaceCriarprojeto.text_area_editor.get("1.0", tk.END).strip()
    try:
        if new_config_LimparCache:
            new_config_data_LimparCache = json.loads(new_config_LimparCache)
            # new_config_data_CriarProjeto = json.loads(new_config_CriarProjeto)     
            LoadConfigCache.save_config(new_config_data_LimparCache) 
        LoadConfigCriarProjeto.salvar_configuracoes_json()
        LoadConfigInterface.salvar_configuracoes_json()
        LoadConfigAtalhos.salvar_configuracoes_json()
       # print(f"Conteúdo do text_area_editor: {new_config_CriarProjeto}")  # Verifica o conteúdo
        #print(f"Tipo do conteúdo: {type(new_config_CriarProjeto)}") 
        
        messagebox.showinfo("Informação", "Configurações salvas com sucesso!")
        #Interface.root.destroy()
        Util.reabrir()
    except json.JSONDecodeError as e:
        Util.LogError("InterfaceConfigEditor",f"Erro ao salvar configurações: {e}")

            
            
def open_config_editor():
    global editor_window
    editor_window = tk.Toplevel(Interface.root,padx=20,pady=20)  # Use ttk.Toplevel
    editor_window.title("Configurações")
    #diretorio_atual = Path(__file__).parent.absolute()
    global icone
    icone = Util.pegarImagem("config.ico")
    editor_window.iconbitmap(False, icone)
    editor_window.configure(bg=Styles.cor_fundo,padx=10,pady=10)
    editor_window.resizable(False,False)
    editor_window.geometry("900x800")
    # Criação do frame e posicionamento
    
    tabviewprincipal = ctk.CTkTabview(editor_window, bg_color=Styles.cor_fundo,
                             fg_color=Styles.cor_fundo,
                             corner_radius=50,
                             segmented_button_fg_color=Styles.cor_fundo,
                             segmented_button_selected_color=Styles.cor_ativo,
                             segmented_button_selected_hover_color=Styles.cor_ativo,                    
                             segmented_button_unselected_hover_color=Styles.cor_ativo)
   
    tabviewprincipal.pack()
    tabviewprincipal.add("Interfaces")
    tabviewprincipal.add("Atalhos")
    
    tabview = ctk.CTkTabview(tabviewprincipal.tab("Interfaces"), bg_color=Styles.cor_fundo,
                             fg_color=Styles.cor_fundo,
                             corner_radius=50,
                             segmented_button_fg_color=Styles.cor_fundo,
                             segmented_button_selected_color=Styles.cor_ativo,
                             segmented_button_selected_hover_color=Styles.cor_ativo,                    
                             segmented_button_unselected_hover_color=Styles.cor_ativo)
    
    
    tabview.pack()
    tabview.add("Config Criar projeto")
    #tabview.add("Config Editor")
    tabview.add("Config Limpar Cache")
    tabview.add("Config Interface")
    
    InterfaceCriarprojeto.ConfigCriarProjetoInterface(tabview)
    InterfaceLimparcache.ConfigLimparCacheInterface(tabview)
    InterfaceConfigInterface.ConfigInterfaceInterface(tabview)
    InterfaceConfigAtalhos.ConfigAtalhosInterface(tabviewprincipal)
   

    CustomWidgets.CustomButton(editor_window,text="Salvar",command=save_and_close).pack()
