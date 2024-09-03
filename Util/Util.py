import logging
import os
from pathlib import Path
import string
import subprocess
import sys
from tkinter import messagebox
from urllib.parse import urlparse
import unicodedata

version = "1.0.6"


global diretorio_atual
global icone
diretorio_atual = Path(__file__).parent.absolute()
icone = os.path.join(diretorio_atual, 'icon.ico')

def reabrir():
    try:
        if getattr(sys, 'frozen', False):  # If the program is compiled as an executable
            executable = sys.executable
            subprocess.Popen([executable])
        else:
            subprocess.Popen([sys.executable] + sys.argv)
    finally:
        sys.exit()

def is_url(path):
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def sanitize_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    # Divide o caminho em diretório e nome do arquivo
    diretorio, nome_arquivo = os.path.split(filename)

    # Sanitiza apenas o nome do arquivo, mantendo o diretório original
    nome_arquivo_limpo = unicodedata.normalize('NFKD', nome_arquivo).encode('ASCII', 'ignore').decode()
    nome_arquivo_limpo = ''.join(c for c in nome_arquivo_limpo if c in valid_chars)

    # Reconstrói o caminho completo com o nome de arquivo sanitizado
    return os.path.join(diretorio, nome_arquivo_limpo)

def quebrar_linhas(texto, max_comprimento=80):
    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        if len(linha_atual) + len(palavra) + 1 > max_comprimento:
            linhas.append(linha_atual)
            linha_atual = palavra
        else:
            if linha_atual:
                linha_atual += " "
            linha_atual += palavra

    if linha_atual:
        linhas.append(linha_atual)

    return "\n".join(linhas)

def pegarTemplate(template):
    return os.path.join("Templates", template)

def pegarImagem(imagem):
    return os.path.join("Imagens", imagem)

def pegarFFMPEG():
    return os.path.join("ffmpeg", "ffmpeg.exe")

def pegarFFMPLAY():
    return os.path.join("ffmpeg", "ffplay.exe")
def pegarFFPROBRE():
    return os.path.join("ffmpeg", "ffprobe.exe")


def frames_to_ms(frames, fps):
    # Calcula a duração de um frame em segundos
    frame_duration_sec = 1 / int(fps)
    # Converte para milissegundos
    frame_duration_ms = frame_duration_sec * 1000
    # Calcula o tempo total para o número de frames especificado
    total_time_ms = frames * frame_duration_ms
    return int(total_time_ms)


def logWarning(func,mensagem,dialog = True):
    logging.warn(f"Aviso na função {func} ", quebrar_linhas(mensagem))
    print(f"Aviso na função {func} ", quebrar_linhas(mensagem))
    if dialog:
        messagebox.showwarning("Aviso",mensagem)
def logInfo(func,mensagem,dialog = True):
    logging.debug(f"Info na função {func} ", quebrar_linhas(mensagem))
    print(f"Info na função {func} ", quebrar_linhas(mensagem))
    if dialog:
        messagebox.showwarning("Info",mensagem)
def LogError(func,mensagem,dialog = True):
    logging.error(f"Erro na função {func} ", quebrar_linhas(mensagem))
    print(f"Erro na função {func} ", quebrar_linhas(mensagem))
    if dialog:
        messagebox.showwarning("Erro",quebrar_linhas(mensagem))