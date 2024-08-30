import os
import re
import subprocess
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk
import patoolib

import Main
from Modelos.CriarProjeto import CriarProjeto, InterfaceCriarProjeto
from Modelos.Interface import Interface
from Util import Util


evento_termino = threading.Event()        
        
def criar_barra_progresso(root):
    try:
        janela = tk.Toplevel(root)
        janela.title("Descompactando, aguarde...")

        # Trazer a janela para frente
        janela.protocol("WM_DELETE_WINDOW", lambda: None)
        janela.lift()
        janela.attributes('-topmost', True)
        janela.after_idle(janela.attributes, '-topmost', False)
        janela.resizable(False, False)

        barra_progresso = ttk.Progressbar(janela, orient="horizontal", length=300, mode="determinate")
        barra_progresso.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        barra_progresso['value'] = 0

        return janela, barra_progresso

    except Exception as e:  # Captura qualquer tipo de exceção
        Util.LogError("Descompactador",f"Ocorreu um erro ao criar a barra de progresso: {e}")
        return None, None  # Retorna None em caso de erro

def atualizar_barra(barra_progresso, tamanho_total, diretorio_saida, janela, evento_termino):  # Adiciona janela como argumento
    tamanho_extraido = 0
    try:
        while tamanho_extraido < tamanho_total and not evento_termino.is_set():
            tamanho_extraido = sum(
                os.path.getsize(os.path.join(diretorio_saida, f))
                for f in os.listdir(diretorio_saida)
                if os.path.isfile(os.path.join(diretorio_saida, f))
            )
            progresso = int((tamanho_extraido / tamanho_total) * 100)
            print(progresso)

            # Agendar atualização na thread principal
            if barra_progresso:
                print("atualizando barra",progresso)
                janela.after(100, lambda: barra_progresso.config(value=progresso))
    except Exception as e:
        Util.LogError("Descompactador",f"Ocorreu um erro ao atualizar a barra de progresso: {e}")

def converter_zip_rar(arquivo_entrada, diretorio_saida, barra_progresso, janela, evento_termino):
    try:
        #time.sleep(1)
        
        # Normalizar o caminho de entrada
        arquivo_entrada = os.path.normpath(arquivo_entrada)
        
        # Extrair apenas o nome do arquivo a partir do caminho
        nome_arquivo = os.path.basename(arquivo_entrada)
        
        # Remover caracteres problemáticos com regex do nome do arquivo
        novo_nome_arquivo = re.sub(r'[à-úÀ-Úâ-ûÂ-Ûã-õÃ-ÕçÇ\-\_]', ' ', nome_arquivo).strip()
        
        # Construir o caminho completo para o arquivo renomeado
        novo_caminho_completo = os.path.join(diretorio_saida, novo_nome_arquivo)
        
        # Renomear o arquivo
        os.rename(arquivo_entrada, novo_caminho_completo)

        # Descompactar o arquivo renomeado
        patoolib.extract_archive(novo_caminho_completo, outdir=diretorio_saida)

        # Fechar a janela após a descompactação
        janela.after(1, janela.destroy)
        janela.after(1, barra_progresso.destroy)
        def remover():
            os.remove(novo_caminho_completo)
        janela.after(5, remover)

    except patoolib.util.PatoolError as e:
        if isinstance(e, UnicodeDecodeError):         
            Util.LogError("Descompactador",f"Erro de codificação no arquivo '{arquivo_entrada}'. Tente renomear o arquivo manualmente ou usar outro programa para descompactar.")
        else:
            messagebox.showerror("Erro", f"Erro ao converter o arquivo '{arquivo_entrada}': {e}")
    except Exception as ex:
        Util.LogError("Descompactador",f"Erro inesperado: {ex}")
    finally:
        def extrair():
                    #messagebox.showinfo("Aviso",diretorio_saida)
                    for filename in os.listdir(diretorio_saida):
                        if filename.endswith(('.mp4', '.avi', '.mkv', '.mov')):  # Adicione mais extensões se necessário
                            video_path = os.path.join(diretorio_saida, filename)
                            video_path2 = os.path.normpath(video_path)
                            audio_filename = os.path.splitext(filename)[0] + '.wav'  # Use .wav para qualidade original
                            audio_path = os.path.join(diretorio_saida, audio_filename)
                            audio_path2 = os.path.normpath(audio_path)
                            

                            command = f'{Util.pegarFFMPEG()} -i "{video_path2}" "{audio_path2}"'

                            try:
                                subprocess.run(command, shell=True, check=True)
                                print(f'Áudio extraído com sucesso de "{filename}" para "{audio_filename}"')
                            except subprocess.CalledProcessError as e:
                                Util.LogError("Descompactador",f'Erro ao extrair áudio de "{filename}": {e}')
        global extrair_audio
        if InterfaceCriarProjeto.extrair_audio: 
            def e():
                Interface.root.after(1000, extrair)
            thread_audio = threading.Thread(target=e)
            thread_audio.daemon = True
            thread_audio.start()
        if janela:
            janela.after(1, janela.destroy)
            janela.after(1, barra_progresso.destroy)
        evento_termino.set()
