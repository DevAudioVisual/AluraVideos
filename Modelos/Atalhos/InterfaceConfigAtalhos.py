import tkinter as tk
import re
import customtkinter as ctk
from Config import  LoadConfigAtalhos
from Util import CustomWidgets, Styles

def ConfigAtalhosInterface(tabview):
    config_data = LoadConfigAtalhos.load_config()
    
    frame = CustomWidgets.CustomScroolabeFrame(tabview.tab("Atalhos"))
    frame.pack(pady=10,padx=10,fill="both")
    
    CustomWidgets.CustomLabel(frame,text="Teclas de atalho",font=Styles.fonte_titulo).pack()
    
    global text_area_editor
    text_area_editor = tk.Text(frame, wrap='word', width=50, height=15)
    #text_area_editor.pack()
    
    c = ConfigAtalhos(config_data=config_data,frame=frame,text_area_editor=text_area_editor)
    c.update_config_from_widgets()
    
    CustomWidgets.CustomButton(frame,text="Resetar configurações",command=LoadConfigAtalhos.resetar_config).pack(pady=10)

class ConfigAtalhos:
    def __init__(self, config_data,frame,text_area_editor):
        self.atalhos = {}
        self.checkbox_vars = {}
        self.frame = frame
        self.text_area_editor = text_area_editor
        
        usarTeclas = tk.BooleanVar(value=LoadConfigAtalhos.TeclasDeAtalho)
        self.checkbox_vars["TeclasDeAtalho"] = usarTeclas
        CustomWidgets.CustomCheckBox(frame,text="Habilitar teclas de atalho",variable=usarTeclas,command=self.update_config_from_widgets).pack(fill="x",expand=True,pady=10)

        for key, label in config_data.items():
            if key != "TeclasDeAtalho":
                var = tk.StringVar(value=label)
                FramePai = CustomWidgets.CustomFrame(frame)        
                FramePai.pack(side="top",pady=10,fill="x",expand=True) 
                frameLabelAtalho = CustomWidgets.CustomFrame(FramePai)        
                frameLabelAtalho.pack(side="left",pady=10,fill="both",expand=True) 
                frameEntryAtalho = CustomWidgets.CustomFrame(FramePai)        
                frameEntryAtalho.pack(side="left",pady=10) 
                CustomWidgets.CustomLabel(frameLabelAtalho,text="" + key,font=Styles.fonte_titulo).pack(side="left",fill="x",expand=True)  
                entry = CustomWidgets.CustomEntry(frameEntryAtalho, textvariable=var, width=100,font=Styles.fonte_input)
                entry.pack(side="left",fill="x",expand=True)
                def update(event):
                    self.update_config_from_widgets()
                entry.getEntry().bind("<KeyRelease>", update)
                self.atalhos[key] = [var.get(),entry]

    def atualizar_atalho(self, key, novo_atalho):
        self.atalhos[key] = novo_atalho
        
    def update_config_from_widgets(self):
        with open(LoadConfigAtalhos.file_path, 'r', encoding='utf-8') as f:
            config_str = f.read()


        for key, value in self.checkbox_vars.items():
            pattern = f'"{key}": (true|false)'
            replacement = f'"{key}": {str(value.get()).lower()}'
            config_str = re.sub(pattern, replacement, config_str)

        for key, (var,entry) in self.atalhos.items():
            pattern = rf'"{key}": ".*?"'
            new_value = entry.get().replace("\\", "\\\\")
            replacement = rf'"{key}": "{new_value}"'
            config_str = re.sub(pattern, replacement, config_str)

        # Atualiza o texto na área de texto
        self.text_area_editor.delete("1.0", tk.END)
        self.text_area_editor.insert(tk.END, config_str)
