
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser
import Ajuda as Ajuda
import customtkinter as ctk
from PIL import Image
import os
import Main
from Modelos.Atalhos import Atalhos
from Modelos.LimparCache import InterfaceLimparCache
from Modelos.EditorVideo import InterfaceConversorMP4
from Modelos.CriarProjeto import InterfaceCriarProjeto
from Config import LoadConfigAtalhos, LoadConfigInterface, InterfaceConfigEditor
from Modelos.EditorAudio import EditorAudioInterFace
from Modelos.SegundoPlano import BandejaWindows
from Util import Util, Styles, CustomWidgets, VerificarAtualizações
from Modelos.ProcurarAssets import ImagensPixababy

root = tk.Tk()


class App():
    def __init__(self):
        self.configureRoot()
        self.registrarAtalhos()
        self.tabviewAudioEVideos = None

    def interfaceCarregamento():
        return

    def carregarInterfacePrincipal(self):
        self.createFrames()
        self.tab_widgets = {}
        for Janela in LoadConfigInterface.Janelas:
            self.tabview.add(Janela)
            if Janela == "Editar":
                self.tabviewAudioEVideos = CustomWidgets.CustomTabview(
                    self.tabview.tab("Editar"))
                self.tabviewAudioEVideos.pack(pady=(0, 0))
                self.tabviewAudioEVideos.add("Video")
                self.tabviewAudioEVideos.add("Audio")
                self.tab_widgets["Video"] = InterfaceConversorMP4.interfaceConversorMP4(
                    self.tabviewAudioEVideos)
                self.tab_widgets["Audio"] = EditorAudioInterFace.abrirConfigAudio(
                    self.tabviewAudioEVideos)
            elif Janela == "Limpar Cache":
                self.tab_widgets["Limpar Cache"] = InterfaceLimparCache.interfaceLimparCache(
                    self.tabview)
            elif Janela == "Projeto":
                self.tab_widgets["Projeto"] = InterfaceCriarProjeto.interfaceCriarProjeto(
                    self.tabview)

        def on_tab_change():
            selected_tab_name = self.tabview.get()
            selected_sub_tab_name = self.tabviewAudioEVideos.get(
            ) if self.tabviewAudioEVideos else None
            for tab_name, widgets in self.tab_widgets.items():

                if tab_name == selected_tab_name or selected_sub_tab_name:
                    widgets.pack(pady=(0, 0))
                else:
                    widgets.pack_forget()

        self.tabview.configure(command=on_tab_change)
        if self.tabviewAudioEVideos:
            self.tabviewAudioEVideos.configure(command=on_tab_change)

        for widgets in self.tab_widgets.values():
            widgets.pack_forget()

        on_tab_change()

        ctk.CTkLabel(self.frameBarraLateral, text=None, image=CustomWidgets.CustomImage(
            "icon.ico", 100, 100)).pack(side="top", fill="x", padx=10, pady=10)
        if LoadConfigInterface.MostrarUsuario:
            usuario = ",\n"+os.getlogin()
        else:
            usuario = " "

        def ajustar_tamanho_fonte(event):
            texto = label.cget("text")
            # Começa em 20 e diminui se passar de 30
            tamanho_fonte = max(10, 18 - (len(texto) - 30))
            label.configure(font=("Helvetica", tamanho_fonte, "bold"))
        label = ctk.CTkLabel(
            self.frameBarraLateral, text=f"Seja bem-vindo(a){usuario}", text_color=Styles.cor_texto)
        label.bind("<Configure>", ajustar_tamanho_fonte)
        label.pack(side="top", fill="x", padx=10, pady=10)
        button_frame = tk.Frame(
            master=self.frameBarraLateral, background="teal")
        # Posiciona o frame na parte inferior e preenche horizontalmente
        button_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        def EmBreve():
            messagebox.showwarning("Aviso", "Em breve!")
        CustomWidgets.CustomLabel(
            self.frameBarraLateral, text="O que vamos fazer hoje?", bg_color="teal").pack(side="top", padx=10)

        def gemini():
            return
            # ChatBotGemini.criarChatBot(root=root)
        CustomWidgets.CustomButton(self.frameBarraLateral, text="Pergunte ao Gemini", width=170, background="teal",
                                   command=gemini, Image=CustomWidgets.CustomImage("gemini.png", 20, 20)).pack(side="top", padx=10, pady=5)
        CustomWidgets.CustomButton(self.frameBarraLateral, text="Minhas tarefas", width=170, background="teal",
                                   command=EmBreve, Image=CustomWidgets.CustomImage("tarefas.png", 20, 20)).pack(side="top", padx=10, pady=5)
        CustomWidgets.CustomButton(self.frameBarraLateral, text="Buscar Imagens", width=170, background="teal",
                                   command=ImagensPixababy.abrirInterface, Image=CustomWidgets.CustomImage("photo.png", 20, 20)).pack(side="top", padx=10, pady=5)

        def abrirform():
            webbrowser.open_new(
                "https://docs.google.com/forms/d/e/1FAIpQLSdQJzQBVbLDwD8ZkEemNuLVBHlWHEhzag8cgwcC2fDyV6IhvQ/viewform?usp=sf_link")

        def abrirLogs():
            log_dir = os.path.join(os.path.expanduser(
                "~"), "Documents", "S_Videos", "Logs")
            webbrowser.open(log_dir)

        def abrirSite():
            webbrowser.open("https://www.samuelmariano.com/s-videos")

        CustomWidgets.CustomButton(button_frame, text="Configurações", width=170, background="teal", command=InterfaceConfigEditor.open_config_editor,
                                   Image=CustomWidgets.CustomImage("config.ico", 20, 20)).pack(side="top", padx=2, pady=5)
        CustomWidgets.CustomButton(button_frame, text="Formulário", width=170, background="teal", command=abrirform,
                                   Image=CustomWidgets.CustomImage("forms.png", 20, 20)).pack(side="top", padx=2, pady=5)
        CustomWidgets.CustomButton(button_frame, text="Logs", width=170, background="teal", command=abrirLogs,
                                   Image=CustomWidgets.CustomImage("logs.png", 20, 20)).pack(side="top", padx=2, pady=5)
        CustomWidgets.CustomButton(button_frame, text="Site oficial", width=170, background="teal", command=abrirSite,
                                   Image=CustomWidgets.CustomImage("icon.ico", 20, 20)).pack(side="top", padx=2, pady=5)

        # Frame de créditos na linha inferior
        credits_frame = tk.Frame(root, bg="gray")
        # Coloca o frame de créditos na linha 1 e na coluna 0, abrangendo ambas as colunas
        credits_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Função para abrir o link ao clicar no texto
        def abrir_link(event):
            # Substitua com o link desejado
            webbrowser.open_new("https://samuelmariano.com")

        # Adiciona o texto de créditos clicável no frame de créditos
        imagemSamuel = ctk.CTkImage(dark_image=Image.open(Util.pegarImagem(
            "penguin.png")), light_image=Image.open(Util.pegarImagem("penguin.png")), size=(25, 25))
        label_autor = ctk.CTkLabel(credits_frame, text="Por: Samuel Mariano", font=Styles.fonte_texto,
                                   cursor="hand2", image=imagemSamuel, compound="right", text_color="white")
        label_autor.pack(anchor="center", pady=5)

        def vaiseapaoxionar(event):
            Ajuda.interfaceAjuda()
        # Torna o texto clicável
        label_autor.bind("<Button-1>", abrir_link)
        label_autor.bind("<Button-3>", vaiseapaoxionar)

        def verificar_atualizacaoEvent(event=None):
            atualizacao = threading.Thread(target=VerificarAtualizações.verificar_atualizacao, args=(
                root,))  # Passar a função e argumentos corretamente
            atualizacao.daemon = True
            atualizacao.start()

        global Bandeja
        Bandeja = None
        if LoadConfigInterface.SegundoPlano == True:
            Bandeja = BandejaWindows.App(root)
        # Agende a verificação de atualização após 1 segundo (1000 milissegundos)
        root.after(1000, verificar_atualizacaoEvent)

    def createFrames(self):
        self.frameSoftwares = CustomWidgets.CustomFrame(root)
        self.frameSoftwares.grid(row=0, column=1, sticky="n", padx=0, pady=0)

        self.frameBarraLateral = ctk.CTkFrame(
            master=root, bg_color="teal", fg_color="teal")
        self.frameBarraLateral.grid(row=0, column=0, sticky="nsew")

        self.tabview = CustomWidgets.CustomTabview(self.frameSoftwares)
        self.tabview.pack(pady=(0, 0))

        # self.frameBarraLateral.grid_forget()
        # self.frameSoftwares.grid_forget()
        # self.tabview.pack_forget()

    def configureRoot(self):
        Styles.DefiniEstilo(ttk)
        root.title(Main.titulo)
        root.geometry("1250x800")
        root.update()
        root.state("zoomed")
        icone = Util.pegarImagem("icon.ico")
        root.iconbitmap(icone)
        root.configure(bg=Styles.cor_fundo)

        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=0)
        root.columnconfigure(0, weight=0)
        root.columnconfigure(1, weight=1)

    def registrarAtalhos(self):
        if LoadConfigAtalhos.TeclasDeAtalho:
            ata = Atalhos.TeclasAtalho()
            ata.registrarAtalhos()

    def reload(self):
        root.destroy()
        self.gerarInterface()

    def getRoot(self):
        return root
