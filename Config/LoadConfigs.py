from collections import OrderedDict
import os
from pathlib import Path
import json
import tkinter as tk
from tkinter import messagebox, messagebox
import pandas as pd
from Util import Util

class Configs():
  def __init__(self):
    self.config_dir = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos", "Config") 
    self.diretorio_atual = Path(__file__).parent.absolute()
    self.Configs = ["ConfigAtalhos","ConfigCache","ConfigCriarProjeto","ConfigInterface"]
    os.makedirs(self.config_dir, exist_ok=True)
    
    self.file_path = {}
    self.config_data = {}
    self.config_file = {}
    
    for c in self.Configs:
      self.file_path[c] = os.path.join(self.config_dir, f"{c}.json")
      self.config_file[c] = os.path.join(self.diretorio_atual, f'{c}.json')
      atualizar_json(self.config_file[c], self.file_path[c])
      
    self.Load()
  def getConfigs(self):
      return Configs
  def saveConfig(self,config,text_area_editor):
    editor_content = text_area_editor.get("1.0", tk.END)
    try:
        data = json.loads(editor_content)
        with open(self.file_path[config], 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
    except json.JSONDecodeError:
        print("Erro: O conteúdo do editor não é um JSON válido.")  
  def Reset(self,config):
    try:
        os.remove(self.file_path[config])
        messagebox.showinfo("Aviso", "Configuração resetada com sucesso!")
        print(f"Arquivo '{self.file_path[config]}' apagado com sucesso!")
        Util.reabrir()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{self.file_path[config]}' não encontrado.")
    except PermissionError:
        print(f"Erro: Você não tem permissão para apagar o arquivo '{self.file_path[config]}'.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
        
  def Load(self):
    for c in self.Configs:
      try:
          with open(self.file_path[c], 'r', encoding='utf-8') as f:
              self.config_data[c] = json.load(f)
      except FileNotFoundError:
          return messagebox.showerror("Erro", f"Erro ao carregar configurações de {c}")
        
  def getDataFrame(self,config):
      return pd.read_json(self.file_path[config])
  def getConfigData(self, config, data=None, should_be_sorted=False):
    try:
        config_data = self.config_data[config]
        if data:
            config_data = config_data[data]

        if should_be_sorted:
            return OrderedDict(sorted(config_data.items()))
        else:
            return config_data
    except KeyError as e:
        print(f"Erro: Chave '{e}' não encontrada no dicionário de configuração.")
        return None  # Ou você pode lançar uma exceção aqui, dependendo do seu caso de uso


def atualizar_chaves_recursivamente(dados1, dados2):
    for chave, valor1 in dados1.items():
        if chave not in dados2:
            dados2[chave] = valor1  # Adiciona a chave se não existir no segundo dicionário
        elif isinstance(valor1, dict) and isinstance(dados2[chave], dict):
            # Chama recursivamente apenas se ambos os valores forem dicionários
            dados2[chave] = atualizar_chaves_recursivamente(valor1, dados2[chave])

    # Remove chaves que existem em dados2 mas não em dados1
    for chave in list(dados2.keys()):
        if chave not in dados1:
            del dados2[chave]

    return dados2

def atualizar_json(arquivo1, arquivo2):
    # Verifica se o arquivo 1 existe
    if not os.path.exists(arquivo1):
        print(f"Erro: O arquivo '{arquivo1}' não foi encontrado.")
        return

    # Se o arquivo 2 não existir, copia o arquivo 1
    if not os.path.exists(arquivo2):
        with open(arquivo1, 'r') as f1, open(arquivo2, 'w') as f2:
            f2.write(f1.read())
        print(f"Arquivo '{arquivo2}' criado com sucesso a partir de '{arquivo1}'.")
        return

    # Carrega os dados dos dois arquivos
    with open(arquivo1, 'r') as f1, open(arquivo2, 'r') as f2:
        dados1 = json.load(f1)
        dados2 = json.load(f2)

    # Atualiza as chaves do segundo arquivo
    dados2_atualizados = atualizar_chaves_recursivamente(dados1, dados2)

    # Salva o segundo arquivo atualizado
    with open(arquivo2, 'w') as f2:
        json.dump(dados2_atualizados, f2, indent=4)

    #print(f"Arquivo '{arquivo2}' atualizado com sucesso!")

