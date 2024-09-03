import os
from pathlib import Path
import tkinter as tk
import json
import pandas as pd
from tkinter import messagebox, messagebox
import Modelos.Interface.InterfaceConfigInterface as InterfaceConfigInterface
from Util import Util

diretorio_atual = Path(__file__).parent.absolute()
config_file = os.path.join(diretorio_atual, 'ConfigInterface.json')

config_dir = os.path.join(os.path.expanduser(
    "~"), "Documents", "AluraVideos", "Config")  # Pasta de documentos do usuário
os.makedirs(config_dir, exist_ok=True)  # Cria o diretório se não existir
file_path = os.path.join(config_dir, "ConfigInterface.json")

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


def load_config():
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def salvar_configuracoes_json():
    editor_content = InterfaceConfigInterface.text_area_editor.get(
        "1.0", tk.END)
    try:
        data = json.loads(editor_content)
        save_config(data)
    except json.JSONDecodeError:
        print("Erro: O conteúdo do editor não é um JSON válido.")


def save_config(data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def iniciarConfig():  # Define o nome do arquivo padrão
    df = pd.read_json(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            print("ConfigInterface.json carregado com sucesso.")

            # Verificar se as chaves existem (incluindo MostrarUsuario2)
            required_keys = ["MostrarUsuario", "SegundoPlano", "OrdemJanelas"]
            for key in required_keys:
                if key not in data:
                    raise KeyError(
                        f"Chave '{key}' não encontrada no arquivo JSON")

            # Criar o DataFrame diretamente do dicionário (sem usar pd.read_json)
            ordem_janelas = data['OrdemJanelas']
            global Janelas, TodasJanelas

            # Criar o DataFrame DataJanelas
            DataJanelas = pd.DataFrame({'OrdemJanelas': ordem_janelas})

            # Extrair o dicionário da primeira linha do DataFrame
            ordem_janelas_dict = DataJanelas.loc[0, 'OrdemJanelas']

            # Filtrar as janelas visíveis
            janelas_visiveis = {chave: valor for chave,
                                valor in ordem_janelas_dict.items() if valor}

            # Criar um novo DataFrame a partir do dicionário filtrado
            JanelasVisiveis = pd.DataFrame(
                {'OrdemJanelas': [janelas_visiveis]})
            TodasAsJanelas = pd.DataFrame(
                {'OrdemJanelas': [ordem_janelas_dict]})

            # Atribuir a coluna 'OrdemJanelas' do novo DataFrame à variável global Janelas
            Janelas = JanelasVisiveis['OrdemJanelas'].iloc[0]
            TodasJanelas = TodasAsJanelas['OrdemJanelas'].iloc[0]
            global MostrarUsuario
            if 'MostrarUsuario' in df.columns:
                MostrarUsuario = df['MostrarUsuario'].iloc[0]
            else:
                raise KeyError(
                    "Chave 'MostrarUsuario' não encontrada no arquivo JSON")

            global SegundoPlano
            if 'SegundoPlano' in df.columns:
                SegundoPlano = df['SegundoPlano'].iloc[0]
            else:
                raise KeyError(
                    "Chave 'SegundoPlano' não encontrada no arquivo JSON")

    except (FileNotFoundError, ValueError, KeyError, IndexError) as e:
        Util.LogError("LoadConfigInterface",
                      f"Erro ao ler ou processar o arquivo de configuração: {e}")
