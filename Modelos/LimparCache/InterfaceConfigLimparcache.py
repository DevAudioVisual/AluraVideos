import tkinter as tk
import re
import Config.LoadConfigCache as LoadConfigCache
import customtkinter as ctk
from Config import InterfaceConfigEditor
from tkinter import filedialog
from Util import CustomWidgets, Styles

def ConfigLimparCacheInterface(tabview):
    config_data = LoadConfigCache.load_config()
    
    frame = CustomWidgets.CustomFrame(tabview.tab("Config Limpar Cache"))
    frame.pack(pady=10,padx=10,fill="both")
    frameDiretorios = CustomWidgets.CustomFrame(tabview.tab("Config Limpar Cache"))
    frameDiretorios.pack(pady=10,padx=10,fill="both")
    framePastasTop = CustomWidgets.CustomFrame(tabview.tab("Config Limpar Cache"))
    framePastasTop.pack(pady=10,padx=10,fill="both")
    
    dirs = {
        "Cache_Adobe": "Adobe Cache"
    }
    
    CustomWidgets.CustomLabel(frame,text="Predefinição para Limpar Cache",font=Styles.fonte_titulo).pack()
    
    entry_vars = {}
    def escolher_diretorio(var):
        novo_diretorio = filedialog.askdirectory()
        InterfaceConfigEditor.editor_window.focus()
        if novo_diretorio:
            novo_diretorio = novo_diretorio.replace("/", "\\\\")  # Duplica as barras invertidas
            #print(novo_diretorio)  # Verifica o valor retornado
            var.set(novo_diretorio)
            update_config_from_widgets()
    
    
    for key, label in dirs.items():
            var = tk.StringVar(value=config_data.get(key, "").replace("\\", "\\\\"))
            entry_vars[key] = var
            
            CustomWidgets.CustomLabel(frameDiretorios,text="Diretório " + label).pack(side="left")
            
            CustomWidgets.CustomEntry(frameDiretorios, textvariable=var, width=300).pack(side="left",padx=10)
            
            CustomWidgets.CustomButton(frameDiretorios, text="Buscar",Image=CustomWidgets.CustomImage("folder.png",20,20),command=lambda k=key: escolher_diretorio(entry_vars[k])).pack(side="left")

    checkbox_vars = {}
    for key, criar in LoadConfigCache.Pastas.items():
        check_var = tk.BooleanVar(value=criar)
        checkbox_vars[key] = check_var
        CustomWidgets.CustomCheckBox(framePastasTop,text=key,variable=check_var,command=lambda key=key: update_config_from_widgets()).pack(pady=10,fill="x")



    global text_area_editor
    text_area_editor = tk.Text(framePastasTop, wrap='word', width=50, height=15)
    
    def update_config_from_widgets():
        with open(LoadConfigCache.file_path, 'r', encoding='utf-8') as f:
            config_str = f.read()

        # Atualiza os valores dos checkboxes
        for key, value in checkbox_vars.items():
            pattern = f'"{key}": (true|false)'
            replacement = f'"{key}": {str(value.get()).lower()}'
            config_str = re.sub(pattern, replacement, config_str)

        # Atualiza os valores das entradas de texto

        for key, var in entry_vars.items():
            pattern = rf'"{key}": ".*?"'
            new_value = var.get().replace("\\", "\\\\")
            replacement = rf'"{key}": "{new_value}"'
            config_str = re.sub(pattern, replacement, config_str)

        # Atualiza o texto na área de texto
        text_area_editor.delete("1.0", tk.END)
        text_area_editor.insert(tk.END, config_str)
