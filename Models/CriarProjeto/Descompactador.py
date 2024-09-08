import os
import re
import subprocess
import threading
import tkinter as tk
from tkinter import ttk
import patoolib
from Interfaces import InterfaceMain
from Util import Util


evento_termino = threading.Event()


def criar_barra_progresso(root, titulo):
    try:
        janela = tk.Toplevel(root)
        janela.title(titulo)

        # Trazer a janela para frente
        janela.protocol("WM_DELETE_WINDOW", lambda: None)
        janela.lift()
        janela.attributes('-topmost', True)
        janela.after_idle(janela.attributes, '-topmost', False)
        janela.resizable(False, False)

        barra_progresso = ttk.Progressbar(
            janela, orient="horizontal", length=300, mode="determinate")
        barra_progresso.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        barra_progresso['value'] = 0

        return janela, barra_progresso

    except Exception as e:  # Captura qualquer tipo de exceção
        Util.LogError("Descompactador",
                      f"Ocorreu um erro ao criar a barra de progresso: {e}")
        return None, None  # Retorna None em caso de erro

def criar_barra_progresso_audios(root, titulo):
    try:
        janela = tk.Toplevel(root)
        janela.title(titulo)

        # Trazer a janela para frente
        janela.protocol("WM_DELETE_WINDOW", lambda: None)
        janela.lift()
        janela.attributes('-topmost', True)
        janela.after_idle(janela.attributes, '-topmost', False)
        janela.resizable(False, False)

        barra_progresso = ttk.Progressbar(
            janela, orient="horizontal", length=300, mode="determinate")
        barra_progresso.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        barra_progresso['value'] = 0

        return janela, barra_progresso

    except Exception as e:  # Captura qualquer tipo de exceção
        Util.LogError("Descompactador",
                      f"Ocorreu um erro ao criar a barra de progresso: {e}")
        return None, None  # Retorna None em caso de erro

# Adiciona janela como argumento
def atualizar_barra(barra_progresso, tamanho_total, diretorio_saida, janela, evento_termino):
    tamanho_extraido = 0
    extensoes_ignoradas = ['.zip', '.rar']  # Adicione outras extensões, se necessário

    try:
        while tamanho_extraido < tamanho_total and not evento_termino.is_set():
            tamanho_extraido = sum(
                os.path.getsize(os.path.join(diretorio_saida, f))
                for f in os.listdir(diretorio_saida)
                if os.path.isfile(os.path.join(diretorio_saida, f)) and 
                   not any(f.endswith(ext) for ext in extensoes_ignoradas)
            )
            progresso = int((tamanho_extraido / tamanho_total) * 100)
            print(progresso)

            # Agendar atualização na thread principal
            if progresso < 99:
                print("atualizando barra", progresso)
                janela.after(100, lambda: barra_progresso.config(value=progresso))
            else:
                break
    except Exception as e:
        Util.LogError("Descompactador", f"Ocorreu um erro ao atualizar a barra de progresso: {e}")

def converter_zip_rar(arquivo_entrada, diretorio_saida, barra_progresso, janela, evento_termino):
    try:
        arquivo_entrada = os.path.normpath(arquivo_entrada)
        nome_arquivo = os.path.basename(arquivo_entrada)
        novo_nome_arquivo = re.sub(r'[à-úÀ-Úâ-ûÂ-Ûã-õÃ-ÕçÇ\-_\+ ]', ' ', nome_arquivo).strip()
        novo_caminho_completo = os.path.join(diretorio_saida, novo_nome_arquivo)
        os.rename(arquivo_entrada, novo_caminho_completo)
        patoolib.extract_archive(novo_caminho_completo, outdir=diretorio_saida)
        
        os.remove(novo_caminho_completo)
        
        # Fechar a janela após a descompactação
        janela.after(1, janela.destroy)
        janela.after(1, barra_progresso.destroy)


    except patoolib.util.PatoolError as e:
        if isinstance(e, UnicodeDecodeError):
            Util.LogError("Descompactador", f"Erro de codificação no arquivo '{arquivo_entrada}'. Tente renomear o arquivo manualmente ou usar outro programa para descompactar.")
        else:
            Util.LogError("Descompactador", f"Erro ao converter o arquivo '{arquivo_entrada}': {e}")
    except Exception as ex:
        Util.LogError("Descompactador", f"Erro inesperado: {ex}")
    finally:
        global extrair_audio
        #if InterfaceCriarProjeto.extrair_audio.get() == True:
        janela2, barra_progresso2 = criar_barra_progresso_audios(InterfaceMain.root,"Extraindo áudios...")
        def extrair():
            total_videos = sum(1 for filename in os.listdir(diretorio_saida) if filename.endswith(('.mp4', '.avi', '.mkv', '.mov')))
            audios_extraidos = 0    
            diretorio_audio = os.path.dirname(diretorio_saida)
            diretorio_audio2 = os.path.join(diretorio_audio, "02_Audio")
            def atualizar_bar():            
                while audios_extraidos < total_videos:
                    progresso = int((audios_extraidos / total_videos) * 100)
                    print(progresso)
                    if janela2 and barra_progresso2:
                        janela2.after(100, lambda: barra_progresso2.config(value=progresso))
                else: 
                    evento_termino.set()
                    if barra_progresso2:
                        barra_progresso2.destroy()
                    if janela2:
                        janela2.destroy()
            thread_barra = threading.Thread(target=atualizar_bar)
            thread_barra.daemon = True
            thread_barra.start()
            for filename in os.listdir(diretorio_saida):
                # Adicione mais extensões se necessário
                if filename.endswith(('.mp4', '.avi', '.mkv', '.mov')):
                    video_path = os.path.join(diretorio_saida, filename)
                    video_path2 = os.path.normpath(video_path)
                    # Use .wav para qualidade original
                    audio_filename = os.path.splitext(filename)[0] + '.wav'
                    audio_path = os.path.join(diretorio_audio2, audio_filename)
                    audio_path2 = os.path.normpath(audio_path)

                    command = f'{Util.pegarFFMPEG()} -loglevel quiet -i "{video_path2}" "{audio_path2}"'

                    try:
                        subprocess.run(command, shell=True, check=True)
                        #print(f'Áudio extraído com sucesso de "{filename}" para "{audio_filename}"')
                        audios_extraidos +=1     
                        print("Audios extraidos: ", audios_extraidos)              
                    except subprocess.CalledProcessError as e:
                        Util.LogError("Descompactador", f'Erro ao extrair áudio de "{filename}": {e}')
        #if InterfaceCriarProjeto.extrair_audio.get() == True:
        def e():
            InterfaceMain.root.after(1000, extrair)
        thread_audio = threading.Thread(target=e)
        thread_audio.daemon = True
        thread_audio.start()
        #else:
            #evento_termino.set()
        if janela:
            janela.after(1, janela.destroy)
            janela.after(1, barra_progresso.destroy)
        #evento_termino.set()
