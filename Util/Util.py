import logging
import os
import string
import subprocess
import sys
from tkinter import messagebox
from urllib.parse import urlparse
import unicodedata
import winreg

def remover_extensao(nome_arquivo):
    try:
        nome, extensao = os.path.splitext(nome_arquivo)
        extensao = extensao.lower()  # Converter para minúsculas para comparação
        formatos_video = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.wav', '.mp3']  # Lista de formatos de vídeo
        if extensao in formatos_video:
            return nome
        else:
            return nome_arquivo
    except Exception as e:
        print(f"Erro ao remover extensão: {e}")
        return nome_arquivo

def format_size(size):
    if size >= 1024**3:  # GB
        return f"{size / (1024**3):.2f} GB"
    elif size >= 1024**2:  # MB
        return f"{size / (1024**2):.2f} MB"
    elif size >= 1024:  # KB
        return f"{size / 1024:.2f} KB"
    else:
        return f"{size} B"


def verificar_premiere_pro():
        """Verifica se o Adobe Premiere Pro está instalado no computador."""
        try:
            # Caminho da chave do registro para o Adobe Premiere Pro
            caminho_chave = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            
            # Abre a chave do registro
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, caminho_chave) as chave:
                # Itera sobre as subchaves
                for i in range(winreg.QueryInfoKey(chave)[0]):
                    try:
                        # Obtém o nome da subchave
                        nome_subchave = winreg.EnumKey(chave, i)
                        
                        # Abre a subchave
                        with winreg.OpenKey(chave, nome_subchave) as subchave:
                            # Verifica se o nome do programa é "Adobe Premiere Pro"
                            nome_programa = winreg.QueryValueEx(subchave, "DisplayName")[0]
                            if "adobe" in nome_programa.lower():
                                return True
                    except:
                        pass
            return False
        except Exception as e:
            print(f"Erro ao verificar a instalação do Premiere Pro: {e}")
            return False


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
    return os.path.join(r"Assets\Images", imagem)

def pegarFFMPEG():
    caminho_ffmpeg = os.path.join("ffmpeg", "ffmpeg.exe")
    if os.path.exists(caminho_ffmpeg):
        return caminho_ffmpeg
    else:
        return "ffmpeg"
def pegarFFMPLAY():
    caminho_ffplay = os.path.join("ffmpeg", "ffplay.exe")
    if os.path.exists(caminho_ffplay):
        return caminho_ffplay
    else:
        return "ffplay"
def pegarFFPROBRE():
    caminho_ffprobe = os.path.join("ffmpeg", "ffprobe.exe")
    if os.path.exists(caminho_ffprobe):
        return caminho_ffprobe
    else:
        return "ffprobe"



def frames_to_ms(frames, fps):
    # Calcula a duração de um frame em segundos
    frame_duration_sec = 1 / int(fps)
    # Converte para milissegundos
    frame_duration_ms = frame_duration_sec * 1000
    # Calcula o tempo total para o número de frames especificado
    total_time_ms = frames * frame_duration_ms
    return int(total_time_ms)


def logWarning(func,mensagem,dialog = True):
    logging.warn(f"Aviso na função {func}:", mensagem)
    print(f"Aviso na função {func}:", mensagem)
    if dialog:
        messagebox.showwarning("Aviso",quebrar_linhas(mensagem))
def logInfo(func,mensagem,dialog = True):
    logging.debug(f"Info na função {func}:", mensagem)
    print(f"Info na função {func}:", mensagem)
    if dialog:
        messagebox.showinfo("Info",quebrar_linhas(mensagem))
def LogError(func,mensagem,dialog = True):
    logging.error(f"Erro na função {func}:", mensagem)
    print(f"Erro na função {func}:", mensagem)
    if dialog:
        messagebox.showerror("Erro",quebrar_linhas(mensagem))