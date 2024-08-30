import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import keyboard
import subprocess
from Util import CustomWidgets


def funcao1():
    print("Função 1 executada")


def funcao2():
    print("Função 2 executada")


def funcao3():
    print("Função 3 executada")


def abrir_diretorio_ou_software(caminho):
    try:
        if os.path.isdir(caminho):
            os.startfile(caminho)
        elif os.path.isfile(caminho):
            subprocess.Popen(caminho)
        else:
            messagebox.showerror("Erro", "Caminho inválido.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))


FUNCOES = {
    "Função 1": funcao1,
    "Função 2": funcao2,
    "Função 3": funcao3,
    "Abrir Diretório": abrir_diretorio_ou_software
}


class GerenciadorAtalhos:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerenciador de Atalhos")
        # Ajuste o tamanho da janela conforme necessário
        self.master.geometry("800x500")

        self.json_file = "atalhos.json"
        self.atalhos = self.carregar_atalhos()

        # Interface
        self.frame = CustomWidgets.CustomFrame(self.master)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # TODO AutocompleteEntryListbox
        self.listbox = tk.Listbox(self.frame, height=15)
        self.listbox.pack(padx=5, pady=5, side=tk.LEFT,
                          fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(
            self.frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        self.frame_right = CustomWidgets.CustomFrame(self.frame)
        self.frame_right.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.frameApelido = CustomWidgets.CustomFrame(self.frame_right)
        self.frameApelido.pack(fill="x", pady=10)
        self.apelido_label = CustomWidgets.CustomLabel(
            self.frameApelido, text="Apelido:")
        self.apelido_label.pack(fill="x", side="left")
        self.apelido_entryy = CustomWidgets.CustomEntry(
            self.frameApelido, width=400)
        self.apelido_entry = self.apelido_entryy.getEntry()
        self.apelido_entryy.pack(fill="x", side="left", padx=10)

        self.frameFuncao = CustomWidgets.CustomFrame(self.frame_right)
        self.frameFuncao.pack(fill="x", pady=10)
        self.funcao_label = CustomWidgets.CustomLabel(
            self.frameFuncao, text="Função:")
        self.funcao_label.pack(fill="x", side="left")
        self.funcao_var = tk.StringVar()
        self.funcao_combobox = CustomWidgets.CustomComboBox(self.frameFuncao, variable=self.funcao_var, width=400, Values=list(
            FUNCOES.keys()), command=self.atualizar_visibilidade_caminho)
        self.funcao_combobox.pack(fill="x", side="left", padx=10)

        self.FrameTecla = CustomWidgets.CustomFrame(self.frame_right)
        self.FrameTecla.pack(fill="x", pady=10)
        self.tecla_label = CustomWidgets.CustomLabel(
            self.FrameTecla, text="Atalho:")
        self.tecla_label.pack(fill="x", side="left")
        self.tecla_entryy = CustomWidgets.CustomEntry(
            self.FrameTecla, width=400)
        self.tecla_entryy.pack(fill="x", side="left", padx=10)
        self.tecla_entry = self.tecla_entryy.getEntry()

        self.frameCaminho = CustomWidgets.CustomFrame(self.frame_right)
        self.frameCaminho.pack(fill="x", pady=10)
        self.diretorio_label = CustomWidgets.CustomLabel(
            self.frameCaminho, text="Caminho:")
        self.diretorio_label.pack(fill="x", side="left")
        self.diretorio_entryy = CustomWidgets.CustomEntry(
            self.frameCaminho, width=400)
        self.diretorio_entryy.pack(fill="x", side="left", padx=10, pady=10)
        self.diretorio_entry = self.diretorio_entryy.getEntry()

        self.tecla_entry.bind("<FocusIn>", self.iniciar_captura_tecla)
        self.tecla_entry.bind("<FocusOut>", self.parar_captura_tecla)
        self.tecla_entry.bind("<Key>", self.ignorar_input)

        self.FrameBotoes = CustomWidgets.CustomFrame(self.frame_right)
        self.FrameBotoes.pack(fill="x", pady=10)

        self.add_button = CustomWidgets.CustomButton(
            self.FrameBotoes, text="Adicionar Atalho", command=self.adicionar_atalho)
        self.add_button.pack(fill="x", side="left")

        self.remove_button = CustomWidgets.CustomButton(
            self.FrameBotoes, text="Remover Atalho", command=self.remover_atalho)
        self.remove_button.pack(fill="x", side="left", padx=10)

        self.remove_button = CustomWidgets.CustomButton(
            self.FrameBotoes, text="Limpar", command=self.remover_atalho)
        self.remove_button.pack(fill="x", side="left", padx=10)

        # self.funcao_combobox.bind("<<ComboboxSelected>>", self.atualizar_visibilidade_caminho)

        self.atualizar_lista()
        self.registrar_atalhos()
        self.diretorio_label.pack(fill="x", side="left")
        self.diretorio_entryy.pack(fill="x", side="left", padx=10)
        self.atualizar_visibilidade_caminho(None)

    def iniciar_captura_tecla(self, event):
        self.teclas_pressionadas = []
        self.tecla_entry.delete(0, tk.END)
        keyboard.hook(self.capturar_evento_tecla)

    def capturar_evento_tecla(self, evento):
        if evento.event_type == 'down':
            tecla_atual = evento.name.upper()
            if tecla_atual == "BACKSPACE":
                self.tecla_entry.delete(0, tk.END)
                self.teclas_pressionadas.clear()
            elif tecla_atual not in self.teclas_pressionadas:
                self.teclas_pressionadas.append(tecla_atual)
                combinacao_teclas = '+'.join(self.teclas_pressionadas)
                self.tecla_entry.delete(0, tk.END)
                self.tecla_entry.insert(0, combinacao_teclas)

    def parar_captura_tecla(self, event):
        keyboard.unhook_all()

    def ignorar_input(self, event):
        return "break"

    def carregar_atalhos(self):
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r') as file:
                    data = file.read()
                    if data:
                        return json.loads(data)
                    return {}
            except json.JSONDecodeError:
                return {}
        return {}

    def salvar_atalhos(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.atalhos, file, indent=4)

    def registrar_atalhos(self):
        keyboard.unhook_all()
        for tecla, dados in self.atalhos.items():
            funcao = dados['funcao']
            if funcao in FUNCOES:
                if funcao == "Abrir Diretório":
                    caminho = dados.get('caminho', '')

                    def abrir_com_caminho():
                        abrir_diretorio_ou_software(caminho)
                    keyboard.add_hotkey(tecla, abrir_com_caminho)
                else:
                    keyboard.add_hotkey(tecla, FUNCOES[funcao])

    def atualizar_lista(self):
        self.listbox.delete(0, tk.END)
        for tecla, dados in self.atalhos.items():
            funcao = dados['funcao']
            apelido = dados.get('apelido', funcao)
            if funcao == "Abrir Diretório":
                caminho = dados.get('caminho', '')
                if caminho and os.path.exists(caminho):
                    nome = os.path.basename(os.path.normpath(caminho))
                    self.listbox.insert(tk.END, f"{apelido} -> {nome}")
                else:
                    self.listbox.insert(
                        tk.END, f"{apelido} -> [Caminho inválido]")
            else:
                self.listbox.insert(tk.END, f"{apelido} -> {tecla}")

    def on_select(self, event):
        selecionado = self.listbox.curselection()
        if selecionado:
            texto = self.listbox.get(selecionado[0])
            if "->" in texto:
                partes = texto.split(" -> ")
                if len(partes) == 2:
                    apelido = partes[0]
                    valor = partes[1]
                    self.apelido_entry.delete(0, tk.END)
                    self.apelido_entry.insert(0, apelido)
                    for tecla, dados in self.atalhos.items():
                        if dados.get('apelido') == apelido:
                            self.funcao_var.set(dados['funcao'])
                            if dados['funcao'] == "Abrir Diretório":
                                self.diretorio_label.pack(
                                    fill="x", side="left")
                                self.diretorio_entryy.pack(
                                    fill="x", side="left", padx=10)
                                self.diretorio_entry.delete(0, tk.END)
                                self.diretorio_entry.insert(
                                    0, dados.get('caminho', ''))
                            else:
                                self.diretorio_entryy.pack_forget()
                                self.diretorio_label.pack_forget()
                            self.tecla_entry.delete(0, tk.END)
                            self.tecla_entry.insert(0, tecla)
                            break

    def atualizar_visibilidade_caminho(self, event):
        if self.funcao_var.get() == "Abrir Diretório":
            self.diretorio_label.pack(fill="x", side="left")
            self.diretorio_entryy.pack(fill="x", side="left", padx=10)
        else:
            self.diretorio_entryy.pack_forget()
            self.diretorio_label.pack_forget()

    def adicionar_atalho(self):
        funcao = self.funcao_var.get()
        tecla = self.tecla_entry.get()
        apelido = self.apelido_entry.get()
        caminho = self.diretorio_entry.get() if self.diretorio_entry.winfo_ismapped() else ""
        if not apelido:
            apelido = funcao
        if funcao and tecla:
            if tecla in self.atalhos:
                keyboard.remove_hotkey(tecla)
            if funcao in FUNCOES:
                if funcao == "Abrir Diretório":
                    if os.path.exists(caminho):
                        self.atalhos[tecla] = {
                            'funcao': funcao, 'caminho': caminho, 'apelido': apelido}
                    else:
                        messagebox.showwarning(
                            "Aviso", "O caminho especificado não existe.")
                        return
                else:
                    self.atalhos[tecla] = {
                        'funcao': funcao, 'apelido': apelido}
            self.salvar_atalhos()
            self.registrar_atalhos()
            self.atualizar_lista()
        else:
            messagebox.showwarning(
                "Aviso", "Complete todos os campos necessários.")

    def remover_atalho(self):
        selecionado = self.listbox.curselection()
        if selecionado:
            texto = self.listbox.get(selecionado[0])
            if "->" in texto:
                apelido = texto.split(" -> ")[0]
                for tecla, dados in self.atalhos.items():
                    if dados.get('apelido') == apelido:
                        del self.atalhos[tecla]
                        keyboard.remove_hotkey(tecla)
                        self.salvar_atalhos()
                        self.registrar_atalhos()
                        self.atualizar_lista()
                        break
