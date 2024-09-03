from collections import OrderedDict
import os
from pathlib import Path
import tkinter as tk
import json
import pandas as pd
from tkinter import messagebox, messagebox

from Modelos.Atalhos import InterfaceConfigAtalhos
from Util import Util


diretorio_atual = Path(__file__).parent.absolute()
config_file = os.path.join(diretorio_atual, 'ConfigAtalhos.json')

config_dir = os.path.join(os.path.expanduser(
    "~"), "Documents", "AluraVideos", "Config")  # Pasta de documentos do usuário
os.makedirs(config_dir, exist_ok=True)  # Cria o diretório se não existir
file_path = os.path.join(config_dir, "ConfigAtalhos.json")


def resetar_config():
    try:
        os.remove(file_path)
        messagebox.showinfo("Aviso", "Configuração resetada com sucesso!")
        print(f"Arquivo '{file_path}' apagado com sucesso!")
        Util.reabrir()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
    except PermissionError:
        print(f"Erro: Você não tem permissão para apagar o arquivo '{
              file_path}'.")
    except Exception as e:
        print(f"Erro inesperado: {e}")


if not Path(file_path).exists():
    # Criar o diretório de destino se não existir
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Criar o arquivo de destino com conteúdo vazio
    with open(file_path, 'w') as f:
        json.dump({}, f)
    print(f"Arquivo de destino criado em: {file_path}")


def comparar_e_atualizar_json(config_file, file_path):
    if not Path(config_file).exists():
        raise FileNotFoundError(
            f"Arquivo original não encontrado: {config_file}")
    if not Path(file_path).exists():
        # Criar o diretório de destino se não existir
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Criar o arquivo de destino com conteúdo vazio
        with open(file_path, 'w') as f:
            json.dump(config_file, f)
        print(f"Arquivo de destino criado em: {file_path}")

    # Carregar os arquivos JSON
    try:
        with open(config_file, 'r') as f1:
            dados1 = json.load(f1)
        with open(file_path, 'r') as f2:
            dados2 = json.load(f2)
    except json.JSONDecodeError:
        raise ValueError("Um ou ambos os arquivos JSON estão inválidos.")

    # Obter as chaves dos dicionários como conjuntos
    chaves1 = set(dados1.keys())
    chaves2 = set(dados2.keys())

    # Verificar se há chaves faltando no arquivo de destino
    chaves_faltando = chaves1 - chaves2

    # Adicionar as chaves faltando do arquivo original para o de destino
    if chaves_faltando:
        for chave in chaves_faltando:
            if chave not in dados2:  # Verifica se a chave já existe no arquivo de destino
                # Copia apenas se a chave não existir
                dados2[chave] = dados1[chave]

        # Salvar o arquivo de destino atualizado
        with open(file_path, 'w') as f2:
            json.dump(dados2, f2, indent=4)
        print("Arquivo de destino atualizado com sucesso!")
    else:
        print("O arquivo de destino já contém todas as chaves do arquivo original.")


comparar_e_atualizar_json(config_file, file_path)


def salvar_configuracoes_json():
    editor_content = InterfaceConfigAtalhos.text_area_editor.get("1.0", tk.END)
    try:
        data = json.loads(editor_content)
        save_config(data)
    except json.JSONDecodeError:
        print("Erro: O conteúdo do editor não é um JSON válido.")


def load_config():
    try:
        with open(file_path, "r") as f:
            config_data = json.load(f)
            # Ordena as chaves em ordem alfabética
            sorted_config = OrderedDict(sorted(config_data.items()))
            return sorted_config
    except FileNotFoundError:
        return messagebox.showerror("Erro", "Erro ao carregar configurações de Cache")


def save_config(data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def iniciarConfig():
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("ConfigAtalhos.json carregado com sucesso.")

            # Verificar se as chaves existem
            required_keys = ["TeclasDeAtalho", "IniciarLimpeza",
                             "BuscarImagens", "Fechar", "Mostrar", "Esconder"]
            for key in required_keys:
                if key not in data:
                    raise KeyError(
                        f"Chave '{key}' não encontrada no arquivo JSON")

            # Converter o dicionário para um DataFrame
           # df = pd.read_json(file_path)
            # df = pd.DataFrame.from_dict(data, orient='index', columns=['Value']).reset_index()
            # df.rename(columns={'index': 'Key'}, inplace=True)
            # print(df)

            global TeclasDeAtalho
            TeclasDeAtalho = data['TeclasDeAtalho']
            global IniciarLimpeza
            IniciarLimpeza = data['IniciarLimpeza']
            global BuscarImagens
            BuscarImagens = data['BuscarImagens']
            global ForceStop
            ForceStop = data['Fechar']
            global ForceShow
            ForceShow = data['Mostrar']
            global ForceHide
            ForceHide = data['Esconder']
    except (FileNotFoundError, ValueError, KeyError, IndexError) as e:
        Util.LogError("LoadConfigAtalhos",
                      f"Erro ao ler ou processar o arquivo de configuração: {e}")
