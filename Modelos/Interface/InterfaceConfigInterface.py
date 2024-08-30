import json
import pandas as pd
import Config.LoadConfigInterface as LoadConfigInterface;
from tkinter import ttk
import tkinter as tk
from Util import Styles,CustomWidgets


def ConfigInterfaceInterface(tabview):
    config_data = LoadConfigInterface.load_config()
    frame = CustomWidgets.CustomFrame(tabview.tab("Config Interface"))
    frame.pack(fill="both",pady=10,padx=10)
    
      
    global text_area_editor
    text_area_editor = tk.Text(frame, wrap='word', width=50, height=15)
    #text_area_editor.pack()
    def update_config_from_widgets():
        ordem = app.ordem()
        valores = {}
        for o in ordem:
            valores[o] = Janelas[o]
        config_data = {
            "MostrarUsuario": MostrarUsuario.get(),
            "SegundoPlano": SegundoPlano.get(),
            "OrdemJanelas": [{key: var.get() for key, var in valores.items()}]
        }
        
        text_area_editor.delete("1.0", tk.END)
        text_area_editor.insert(tk.END, json.dumps(config_data, indent=4))
      


    MostrarUsuario = tk.BooleanVar(value=bool(LoadConfigInterface.MostrarUsuario))
    CustomWidgets.CustomCheckBox(frame,text="Mostrar usuário na barra lateral",command=update_config_from_widgets,variable=MostrarUsuario).pack(pady=10,fill="x")
    
    SegundoPlano = tk.BooleanVar(value=bool(LoadConfigInterface.SegundoPlano))
    CustomWidgets.CustomCheckBox(frame,text="Perguntar se deseja o app em segundo plano ao fechar",command=update_config_from_widgets,variable=SegundoPlano).pack(pady=10,fill="x")
    
    Label = CustomWidgets.CustomLabel(frame,text="Ordem das janelas na interface principal",font=Styles.fonte_titulo)
    Label.pack()
    Label2 = CustomWidgets.CustomLabel(frame,text="(Clique e arraste para alterar)",font=Styles.fonte_input)
    Label2.pack()
   
    frameListChecks = CustomWidgets.CustomFrame(frame)
    frameListChecks.pack(pady=10)
    
    frameList = CustomWidgets.CustomFrame(frameListChecks)
    frameList.pack(side="left",padx=10,fill="both")
    
    frameChecks = CustomWidgets.CustomFrame(frameListChecks)
    frameChecks.pack(side="left",padx=10,fill="both")
    global app
    app = App(frameList,update_config_from_widgets)
    app.listbox.bind("<Button-1>", app.on_drag)  # Vincular eventos de arrastar e soltar
    app.pack(pady=10,fill="x")
    
    
    JanelasAtivadas = []
    Janelas = {}
    for Janela in LoadConfigInterface.Janelas:
        JanelasAtivadas.append(Janela)
        
    for Janela in LoadConfigInterface.TodasJanelas:
        if Janela in JanelasAtivadas:   
            Var = tk.BooleanVar(value=True)
            Janelas[Janela] = Var
            CustomWidgets.CustomCheckBox(frameChecks,text=Janela,variable=Var,command=update_config_from_widgets).pack(pady=10)
        else:
            Var = tk.BooleanVar(value=False)
            Janelas[Janela] = Var
            CustomWidgets.CustomCheckBox(frameChecks,text=Janela,variable=Var,command=update_config_from_widgets).pack(pady=10)
    
    
class App(ttk.Frame):
    def __init__(self, master=None, comando=None):
        super().__init__(master)
        self.comando = comando
        self.ordem_janelas = []
        
        self.config(style="Custom.TFrame")   
        self.listbox = tk.Listbox(self,
                                  bg=Styles.cor_fundo,                             
                                  fg=Styles.cor_texto,
                                  font=Styles.fonte_texto,
                                  highlightthickness=1,
                                  borderwidth=1,
                                  cursor="hand2",
                                  relief="flat",
                                  selectbackground=Styles.cor_ativo,
                                  selectmode="single")        
        
        
        linha = 0
        for j in LoadConfigInterface.TodasJanelas:
            self.ordem_janelas.insert(linha,j)
            linha += 1

        self.data_janelas = pd.DataFrame({"OrdemJanelas": self.ordem_janelas})

        for item in self.ordem_janelas:
            self.listbox.insert(tk.END, item)
        self.listbox.pack(pady=20)
        self.listbox.bind("<ButtonRelease-1>", self.on_drop)

        self.dragging = False
        
        self.listbox.pack()

    def ordem(self):
        return self.ordem_janelas   

    def on_drag(self, event):
        self.dragging = True
        self.drag_start_index = self.listbox.nearest(event.y)
        self.comando()

    def on_drop(self, event):
        if not self.dragging:
            return
        self.dragging = False

        drop_index = self.listbox.nearest(event.y)
        if drop_index == self.drag_start_index:
            return

        item = self.listbox.get(self.drag_start_index)
        self.listbox.delete(self.drag_start_index)
        self.listbox.insert(drop_index, item)

        # Atualizar DataFrame
        self.ordem_janelas.remove(item)
        self.ordem_janelas.insert(drop_index, item)
        self.data_janelas = pd.DataFrame({"OrdemJanelas": self.ordem_janelas}) 
        self.comando()
            