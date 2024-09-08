import ctypes
import os
import Interfaces.LimparCacheInterface as LimparCacheInterface
from Interfaces import InterfaceMain
import Config.LoadConfigCache as LoadConfigCache
from tkinter import messagebox

from Util import Util

# Função para converter tamanho de bytes para uma forma legível
def converter_tamanho(tamanho_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if tamanho_bytes < 1024:
            return f"{tamanho_bytes:.2f} {unit}"
        tamanho_bytes /= 1024

# Função para excluir arquivos de uma pasta
def excluir_arquivos_pasta(caminho_pasta, progress_bar, total_arquivos, arquivos_processados, janela):
    espaço_liberado = 0
    arquivos_deletados = 0
    arquivos_erro = 0
    for root_dir, _, arquivos in os.walk(caminho_pasta):
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(root_dir, arquivo)
            try:
                tamanho_arquivo = os.path.getsize(caminho_arquivo)
                os.remove(caminho_arquivo)
                espaço_liberado += tamanho_arquivo
                arquivos_deletados += 1
            except PermissionError:
                arquivos_erro += 1
            finally:
                arquivos_processados += 1
                progress_bar['value'] = (arquivos_processados / total_arquivos) * 100
                #progress_bar['value'] = 0
                janela.update_idletasks()
    return espaço_liberado, arquivos_deletados, arquivos_erro, arquivos_processados

# Função para contar todos os arquivos nas pastas selecionadas
def contar_arquivos(pastas):
    total = 0
    for pasta in pastas:
        for _, _, arquivos in os.walk(pasta):
            total += len(arquivos)
    return total

# Função para esvaziar a lixeira
def esvaziar_lixeira():
    SHERB_NOCONFIRMATION = 0x00000001
    SHERB_NOPROGRESSUI = 0x00000002
    SHERB_NOSOUND = 0x00000004
    flags = SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI | SHERB_NOSOUND

    # Obter o caminho da Lixeira
    caminho_lixeira = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Microsoft\Windows\Explorer\desktop.ini')

    # Chamar a função SHEmptyRecycleBinW da API do Windows
    if ctypes.windll.shell32.SHEmptyRecycleBinW(None, caminho_lixeira, flags):
        print("Lixeira esvaziada com sucesso!")
    else:
        print("Erro ao esvaziar a Lixeira.")

# Função para iniciar a limpeza
def get_temp_dir():
    temp_dir = os.environ.get('TEMP') or os.environ.get('TMP')
    if temp_dir is None:
        raise FileNotFoundError("Diretório temporário não encontrado.")
    return temp_dir

def iniciar_limpeza():
    pastas_limpar = []
    for key in LimparCacheInterface.selected_keys:
        
        if (key == "Temp"): pastas_limpar.append("C:\\Windows\\Temp")     
        elif (key == "PorcentoTemp"): pastas_limpar.append(get_temp_dir())    
        elif (key == "Prefetch"): pastas_limpar.append("C:\\Windows\\Prefetch")   
        elif (key == "Adobe Cache"): pastas_limpar.append(LoadConfigCache.Diretorio_CacheAdobe)
        elif (key == "Lixeira"): esvaziar_lixeira()
    #print(pastas_limpar)
    total_arquivos = contar_arquivos(pastas_limpar)
    arquivos_processados = 0

    resultados_por_pasta = {}
    espaço_total_liberado = 0
    #print(pastas_limpar)
    for pasta in pastas_limpar:
         if pasta: 
            espaço_liberado, arquivos_deletados, arquivos_erro, arquivos_processados = excluir_arquivos_pasta(
                 pasta, LimparCacheInterface.progress_bar, total_arquivos, arquivos_processados, InterfaceMain.root
            )
            resultados_por_pasta[pasta] = (espaço_liberado, arquivos_deletados, arquivos_erro)
            espaço_total_liberado += espaço_liberado
    


    espaço_total_liberado_legivel = converter_tamanho(espaço_total_liberado)
    Util.logInfo("Limpeza", f"Arquivos deletados.\nEspaço total liberado: {espaço_total_liberado_legivel}\nPastas limpas: {LimparCacheInterface.selected_keys}")