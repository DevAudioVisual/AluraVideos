import json
import os
import subprocess
import sys
import tempfile
import tkinter as tk
from tkinter import messagebox
import webbrowser
import requests
from Util import Styles, Util
import Util.CustomWidgets as CustomWidgets
import urllib.request


def download_and_execute(url, root):

    # Melhoria: usar o diretório temporário padrão do sistema
    with tempfile.TemporaryDirectory() as temp_dir: 
        file_path = os.path.join(temp_dir, 'S_Videos setup.exe')

        try:
            if sys.platform == "win32":
                os.system(f'start cmd /k python "{__file__}"') 
            else:
                os.system(f'xterm -e "python3 \'{__file__}\'" &')
            # Download com gdown
            #gdown.download(url, file_path, quiet=False)
            urllib.request.urlretrieve(url, file_path)
            print("Arquivo baixado com sucesso:", file_path)

            # Melhoria: usar shell=True no Windows para evitar problemas com espaços em nomes de arquivos
            subprocess.Popen(file_path, shell=sys.platform == "win32")  

            # Melhoria: fechar a janela principal após iniciar a instalação
            root.destroy()  

        except FileNotFoundError as e:
            messagebox.showerror("Erro", f"Arquivo não encontrado: {e}")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro inesperado: {e}")

# URL do arquivo para download
url = "https://drive.google.com/uc?export=download&id=12Er8--c4KTEKM2C4aFU33nvSpF-JaK5m"










def mostrar_atualizacao(dados_versao, root):
    editor_window = tk.Toplevel(root) 
    editor_window.title("Atualização disponível")
    editor_window.resizable(False,False)
    editor_window.configure(bg=Styles.cor_fundo,padx=10,pady=10)
    mensagem = f"Nova versão disponível: {dados_versao['numero_versao']}\n\n"
    mensagem += "Notas de lançamento:\n"
    for nota in dados_versao["notas_lancamento"]:
        mensagem += f"- {nota}\n"
    mensagem += "https://samuelmariano.com/s-videos"
    CustomWidgets.CustomLabel(editor_window, text=mensagem).pack()
    def abrirsite():      
        # messagebox.showinfo("Aviso","Download será iniciado.\nPor favor, não feche o Software.\n\nClique em ok para continuar.")
        # thread_download = threading.Thread(target=download_and_execute, args=(url, root))
        # thread_download.daemon = True
        # thread_download.start()
        # editor_window.destroy()
        webbrowser.open("https://www.samuelmariano.com/s-videos")
    CustomWidgets.CustomButton(editor_window, text="Clique para baixar",command=abrirsite).pack(pady=10)
    #messagebox.showinfo("Atualização disponível", mensagem)

def verificar_atualizacao(root):
    url_versao = f"https://drive.google.com/uc?export=download&id=1hZ4gyn8ozFsYdG0XVFXIu4BdR_NENAp_"  # Substitua {FILE_ID} pelo ID do seu arquivo version.json

    try:
        print("verificando")
        response = requests.get(url_versao)
        response.raise_for_status()  # Lança uma exceção se a requisição falhar
        dados_versao = json.loads(response.text)
        versao_atual = Util.version  # Substitua pela versão atual do seu software

        if dados_versao["numero_versao"] > versao_atual:
            print("Nova versão disponível:", dados_versao["numero_versao"])
            mostrar_atualizacao(dados_versao, root)
            # Lógica para notificar o usuário (ex: exibir um popup)
    except requests.exceptions.RequestException as e:
        print("Erro ao verificar atualização:", e)
 