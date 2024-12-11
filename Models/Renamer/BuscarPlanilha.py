import re
import tempfile
import pandas as pd
import requests
from Models.Renamer.ExtrairTituloPlanilha import extrair_titulo_planilha
from Util import Util

def buscar_na_planilha(carregando,campo_formato,campo_sheets,campo_id,dados):
        campo_formato.setText("{id}-video{aula}-{titulo}-{sufixo}")
        if carregando == True:
            return
        carregando = True
        
        spreadsheet_url = campo_sheets.text()
        if spreadsheet_url:
            campo_id.setText(extrair_titulo_planilha(spreadsheet_url))
            padrao_id = r"/spreadsheets/d/([a-zA-Z0-9-_]+)"
            match = re.search(padrao_id, spreadsheet_url)
            try:
                if match:
                    spreadsheet_id = match.group(1)
                    
                    padrao_gid = r"gid=(\d+)"
                    match_gid = re.search(padrao_gid, spreadsheet_url)
                    
                    gid = None
                    
                    if match_gid:
                        gid = match_gid.group(1)
                        csv_export_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}'
                    else:
                        csv_export_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv'
                    
                    response = requests.get(csv_export_url)
                    response.raise_for_status()
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
                        temp_file.write(response.content)
                        temp_file_path = temp_file.name
                    df = pd.read_csv(temp_file_path, header=None,skiprows=2)
                    
                    coluna_a = df.iloc[:, 0]
                    coluna_b = df.iloc[:, 1]
                    if df.shape[1] > 3:  # Verifica se existem pelo menos 4 colunas
                        coluna_d = df.iloc[:, 3]
                    else:
                        coluna_d = None
                        
                    try:
                        if coluna_d is not None and not coluna_d.empty: 
                            padrao_aula = r"(\d+\.\d+)-(.*)"
                            for i in range(len(coluna_d)):
                                 if pd.notna(coluna_d[i]) and re.search(padrao_aula, str(coluna_d[i])):
                                     match = re.match(r"(\d+\.\d+)-(.*)", str(coluna_d.iloc[i]))  # Aplica a regex
                                     if match:
                                         numero_aula = match.group(1)
                                         nome_aula = match.group(2).strip()
                                         dados[f"Aula {numero_aula}"] = nome_aula
                        else:
                            padrao_aula = r"Aula \d+\.\d+"
                            for i in range(len(coluna_a)):
                                match = re.match(padrao_aula, str(coluna_a[i]))
                                if match:
                                    if pd.notna(coluna_a[i]) and re.search(padrao_aula, str(coluna_a[i])):
                                        dados[coluna_a[i]] = coluna_b[i]
                    except Exception as e:
                        print(e)  
            except Exception as e:
                Util.LogError("RenamerSheets",f"Erro: {e}")