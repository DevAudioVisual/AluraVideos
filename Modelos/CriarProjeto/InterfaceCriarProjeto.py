import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Modelos.CriarProjeto import CriarProjeto, InterfaceConfigCriarProjeto
import Config.LoadConfigCriarProjeto as LoadConfig
import customtkinter as ctk
from Util import Util, Styles, CustomWidgets
import re
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode


def interfaceCriarProjeto(tabview):
    global input_dir_var, output_dir_var, nome_projeto_var, CriarEm, ArquivoVideos
    global criar_arquivos, criar_pastas, abrir_premiere, abrir_pasta, subpasta_vars, fechar_ao_criar, verificar_videos

    input_dir_var = ctk.StringVar()
    output_dir_var = ctk.StringVar()

    frame_auxiliar = CustomWidgets.CustomFrame(tabview.tab("Projeto"))

    dialog = CustomWidgets.CustomFrame(frame_auxiliar)
    dialog.pack()

    CustomWidgets.CustomLabel(
        dialog, text="Nome do projeto:", font=Styles.fonte_titulo).pack(pady=5, fill="x")

    nome_projeto_var = tk.StringVar(value="00_Novo Projeto")
    CustomWidgets.CustomEntry(dialog, textvariable=nome_projeto_var,
                              dica="Defina um nome para o projeto:", width=300).pack(pady=5, fill="x", side="top")

    CustomWidgets.CustomLabel(dialog, text="Diretório do projeto:",
                              font=Styles.fonte_titulo).pack(pady=5, fill="x")

    CriarEm = tk.StringVar(value=LoadConfig.diretorio_padrao)

    def changeDirectory():
        try:
            dir = filedialog.askdirectory()
            if not os.path.isdir(dir):
                raise FileNotFoundError(f"Diretório não encontrado: {dir}")
            CriarEm.set(dir)
        except FileNotFoundError as e:
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

    # Posiciona o Entry e o botão "Buscar" diretamente no dialog
    framebuscar = CustomWidgets.CustomFrame(dialog)
    framebuscar.pack(fill="x")
    CustomWidgets.CustomEntry(framebuscar, textvariable=CriarEm, width=300).pack(
        pady=5, fill="x", side="left")
    imagem_folder = CustomWidgets.CustomImage("folder.png", 20, 20)
    CustomWidgets.CustomButton(framebuscar, text="Buscar", dica="Clique para buscar um diretório para o projeto.",
                               Image=imagem_folder, command=changeDirectory).pack(pady=5, padx=5, fill="x", side="left")

    CustomWidgets.CustomLabel(dialog, text="Arquivo de vídeos (.rar ou .zip)",
                              font=Styles.fonte_titulo).pack(pady=5, fill="x")

    ArquivoVideos = tk.StringVar()
    global filepath
    filepath = None

    def changeDirectoryVideos():
        global filepath
        try:

            filepath = filedialog.askopenfilename(
                filetypes=[("Arquivos RAR e ZIP", "*.rar;*.zip")]
            )

            if not filepath:  # Usuário cancelou a seleção
                return

            # Verifica se é um arquivo (e não um diretório)
            if not os.path.isfile(filepath):
                Util.LogError("InterfaceCriarProjeto",
                              f"Arquivo não encontrado: {filepath}")
                return

            extensoes_validas = [".rar", ".zip"]
            if os.path.splitext(filepath)[1].lower() not in extensoes_validas:
                Util.LogError(
                    "InterfaceCriarProjeto", f"O arquivo selecionado não é um RAR ou ZIP: {filepath}")
                return

            ArquivoVideos.set(filepath)

        except (FileNotFoundError, ValueError) as e:
            Util.LogError("InterfaceCriarProjeto", "Erro", str(e))
        except Exception as e:
            Util.LogError("InterfaceCriarProjeto",
                          f"Ocorreu um erro inesperado: {e}")

    framebuscarVideos = CustomWidgets.CustomFrame(dialog)
    framebuscarVideos.pack()
    CustomWidgets.CustomEntry(framebuscarVideos, textvariable=ArquivoVideos, width=300).pack(
        pady=5, fill="x", side="left")
    imagem_folder = CustomWidgets.CustomImage("folder.png", 20, 20)

    def dialogo():
        global filepath
        dialogo = ctk.CTkInputDialog(
            text="Digite a URL completa", title="URL ")
        filepath = dialogo.get_input()
        ArquivoVideos.set(filepath)

        nome_projeto_var.set(limpar_texto(obter_nome_pasta(filepath)))

    checks_vars = {}
    checks = LoadConfig.checks.items()
    for ch, ci in checks:
        checks_vars[ch] = ci

    CustomWidgets.CustomButton(framebuscarVideos, text="Link Dropbox", dica=Util.quebrar_linhas("Clique para inserir o link publico para o dropbox"),
                               Image=CustomWidgets.CustomImage("link.ico", 20, 20), command=dialogo).pack(pady=5, padx=5, fill="x", side="right")
    CustomWidgets.CustomButton(framebuscarVideos, text="Buscar", dica="Clique para buscar o arquivo de vídeos",
                               Image=imagem_folder, command=changeDirectoryVideos).pack(pady=5, padx=5, fill="x", side="right")

    frameBoxes = CustomWidgets.CustomFrame(dialog)
    frameBoxes.pack(fill="x")

    frameAbrirProjetoEPasta = CustomWidgets.CustomFrame(frameBoxes)
    frameAbrirProjetoEPasta.pack(side="left", fill="x")

    abrir_premiere = tk.BooleanVar(value=checks_vars["Abrir_Premiere"])
    CustomWidgets.CustomCheckBox(master=frameAbrirProjetoEPasta, text="Abrir Premiere",
                                 dica="Selecione para abrir o premiere ao criar.", variable=abrir_premiere).pack(pady=(10, 0), padx=5, anchor="w", fill="x")

    abrir_pasta = tk.BooleanVar(value=checks_vars["Abrir_pasta_do_projeto"])
    CustomWidgets.CustomCheckBox(master=frameAbrirProjetoEPasta, text="Abrir pasta do projeto",
                                 dica="Selecione para abrir a pasta do projeto ao criar.", variable=abrir_pasta).pack(pady=(10, 0),padx=5, anchor="w", fill="x")

    #extrair_audio = tk.BooleanVar(value=checks_vars["Extrair_audio"])
    #CustomWidgets.CustomCheckBox(master=frameAbrirProjetoEPasta, text="Extrair audio",dica=None, variable=extrair_audio).pack(pady=(10, 0), padx=5, anchor="w", fill="x")

    CustomWidgets.CustomLabel(dialog, text="Sub-pastas para criar:",
                              dica="Selecione quais sub-pastas devem ser criadas.", font=Styles.fonte_titulo).pack(pady=10, fill="x")

    subpastas_frame = CustomWidgets.CustomFrame(dialog)
    subpastas_frame.pack(fill="x", expand=True, pady=10)

    global subpasta_vars
    subpasta_vars = {}

    coluna_atual = 0
    row = 0

    for subpasta, criar in LoadConfig.subpastas.items():
        subpasta_vars[subpasta] = tk.BooleanVar(value=criar)
        CustomWidgets.CustomCheckBox(master=subpastas_frame, text=subpasta, variable=subpasta_vars[subpasta]).grid(
            row=row, column=coluna_atual, sticky="w", pady=5
        )
        row += 1
        if row == 3:
            row = 0
            coluna_atual += 1
    fechar_ao_criar = LoadConfig.fechar_ao_criar
    fechar_ao_criar = tk.BooleanVar(value=bool(fechar_ao_criar))
    CustomWidgets.CustomButton(master=dialog, text="Criar", dica="Clique aqui para criar seu projeto.",
                               command=CriarProjeto.criar_pastas, width=200).pack(anchor="center", pady=10, side=("left"), padx=10, fill="x")
    CustomWidgets.CustomCheckBox(master=dialog, text="Fechar ao criar", dica="Selecione para fechar o Software ao criar.",
                                 variable=fechar_ao_criar).pack(anchor="center", side=("left"), fill="x")

    return frame_auxiliar


def obter_nome_pasta(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Dependendo da estrutura da página, você pode precisar ajustar esta seleção.
        # Aqui estamos supondo que o nome da pasta é encontrado em um elemento <title> ou similar.
        # É possível que você precise inspecionar a página e ajustar o seletor.
        title_tag = soup.find('title')

        if title_tag:
            title_text = title_tag.get_text()
            # partes = title_text.split(' - ')
            texto = str(title_text).replace(
                "Dropbox - ", "").replace(" - Simplify your life", "")
            return texto
        else:
            return 'Título não encontrado'
    else:
        return 'Erro na requisição'


def limpar_texto(texto):
    # Normaliza os acentos usando unidecode
    texto_normalizado = unidecode(texto)

    # Remove caracteres especiais, mantendo apenas letras e números
    texto_limpo = re.sub(r'[^a-zA-Z0-9\s-]', '', texto_normalizado)

    # Substitui "ç" por "c"
    texto_limpo = texto_limpo.replace('ç', 'c')

    return texto_limpo
