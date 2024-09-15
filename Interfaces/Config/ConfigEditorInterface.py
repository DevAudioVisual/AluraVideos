import tkinter as tk
import Main
import json
from Interfaces.Atalhos import AtalhosConfigInterface
import Interfaces.Interface.InterfaceMain as InterfaceMain
import customtkinter as ctk
import Interfaces.LimparCache.LimparCacheConfigInterface as InterfaceLimparcache
from Util import CustomWidgets, Util,Styles
from tkinter import messagebox, messagebox
from Interfaces.CriarProjeto import CriarProjetoConfigInterface as InterfaceCriarprojeto
from Interfaces.Interface import InterfacePrincipalConfigInterface

            
def save_and_close():
    try:
        config = Main.Config
        config.saveConfig(config="ConfigAtalhos",text_area_editor=AtalhosConfigInterface.text_area_editor)
        config.saveConfig(config="ConfigInterface",text_area_editor=InterfacePrincipalConfigInterface.text_area_editor)
        config.saveConfig(config="ConfigCriarProjeto",text_area_editor=InterfaceCriarprojeto.text_area_editor)
        config.saveConfig(config="ConfigCache",text_area_editor=InterfaceLimparcache.text_area_editor)
        
        messagebox.showinfo("Informação", "Configurações salvas com sucesso!")
        Util.reabrir()
    except json.JSONDecodeError as e:
        Util.LogError("InterfaceConfigEditor",f"Erro ao salvar configurações: {e}")

            
            
def open_config_editor():
    global editor_window
    editor_window = tk.Toplevel(InterfaceMain.root,padx=20,pady=20)  # Use ttk.Toplevel
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
    InterfacePrincipalConfigInterface.ConfigInterfaceInterface(tabview)
    AtalhosConfigInterface.ConfigAtalhosInterface(tabviewprincipal)
   

    CustomWidgets.CustomButton(editor_window,text="Salvar",command=save_and_close).pack()
