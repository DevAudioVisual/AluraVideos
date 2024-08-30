import os
import json
from pathlib import Path
import pandas as pd
from Modelos.CriarProjeto import InterfaceConfigCriarProjeto
import tkinter as tk

from Util import Util

diretorio_atual = Path(__file__).parent.absolute()
config_file = os.path.join(diretorio_atual, 'ConfigCriarProjeto.json')

config_dir = os.path.join(os.path.expanduser("~"), "Documents", "S_Videos", "Config")  # Pasta de documentos do usuário
os.makedirs(config_dir, exist_ok=True)  # Cria o diretório se não existir
file_path = os.path.join(config_dir, "ConfigCriarProjeto.json")

if not Path(file_path).exists():
        # Criar o diretório de destino se não existir
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Criar o arquivo de destino com conteúdo vazio
        with open(file_path, 'w') as f:
            json.dump({}, f)
        print(f"Arquivo de destino criado em: {file_path}")


def comparar_e_atualizar_json(config_file, file_path):
    if not Path(config_file).exists():
        raise FileNotFoundError(f"Arquivo original não encontrado: {config_file}")
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
                dados2[chave] = dados1[chave]  # Copia apenas se a chave não existir

        # Salvar o arquivo de destino atualizado
        with open(file_path, 'w') as f2:
            json.dump(dados2, f2, indent=4)
        print("Arquivo de destino atualizado com sucesso!")
    else:
        print("O arquivo de destino já contém todas as chaves do arquivo original.")

comparar_e_atualizar_json(config_file, file_path)

def load_config():
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_config(data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def salvar_configuracoes_json():
        editor_content = InterfaceConfigCriarProjeto.text_area_editor.get("1.0", tk.END)
        try:
            data = json.loads(editor_content)
            save_config(data)
        except json.JSONDecodeError:
            print("Erro: O conteúdo do editor não é um JSON válido.")
               
def IniciarConfig():
    global caminho_atual, lista_agendas,subpastas,checks,fechar_ao_criar,diretorio_padrao
    caminho_atual = diretorio_atual
    #caminho_atual = r"C:\Users\Samuel\Desktop\Trabalho e Estudos\Projetos\00_Fazendo"
    try:
        df = pd.read_json(file_path)             
        if 'diretorio_padrao' in df.columns:
            diretorio_padrao = df['diretorio_padrao'].iloc[0]
            #print("Subpastas:", subpastas)
            
        if 'fechar_ao_criar' in df.columns:
            fechar_ao_criar = df['fechar_ao_criar'].iloc[0]
            #print("Subpastas:", subpastas)
        else:
            raise KeyError("Chave 'checks' não encontrada no arquivo JSON")
        
        if 'checks' in df.columns:
            checks = df['checks'].iloc[0]
            #print("Subpastas:", subpastas)
        else:
            raise KeyError("Chave 'checks' não encontrada no arquivo JSON")
        
        if 'subpastas' in df.columns:
            subpastas = df['subpastas'].iloc[0]
            #print("Subpastas:", subpastas)
        else:
            raise KeyError("Chave 'subpastas' não encontrada no arquivo JSON")

        print("ConfigCriarPastas.json carregado com sucesso.")
       

    except (FileNotFoundError, ValueError, KeyError, IndexError) as e:
        Util.LogError("LoadConfigCriarProjeto",f"Erro ao ler ou processar o arquivo de configuração: {e}")
        lista_agendas = []  # Define uma lista vazia como padrão em caso de erro