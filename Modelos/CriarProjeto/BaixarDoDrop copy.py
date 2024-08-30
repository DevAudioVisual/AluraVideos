import threading
import requests
import os
import tkinter as tk
from tkinter import messagebox, ttk
from Util import CustomWidgets

evento_termino = threading.Event()      
global foi_baixado 
foi_baixado = False
def transformar_link_dropbox(link):
    if "dl=0" in link:
        return link.replace("dl=0", "dl=1")
    return link
def baixar_pasta_dropbox(root,url_pasta, diretorio_destino):
    
    try:
        janela = tk.Toplevel(root)
        janela.title("Baixando arquivos...")
        janela.protocol("WM_DELETE_WINDOW", lambda: None)
        janela.lift()
        janela.attributes('-topmost', True)
        janela.after_idle(janela.attributes, '-topmost', False)
        janela.resizable(False, False)
        barra_progresso = ttk.Progressbar(janela, orient='horizontal', length=300, mode='determinate')
        barra_progresso.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        variavel = tk.StringVar()
        CustomWidgets.CustomEntry(janela,textvariable=variavel,width=200).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

      
      
        # Transformar o link de compartilhamento em link de download
        url_download = transformar_link_dropbox(url_pasta)

        response = requests.get(url_download, stream=True)
        response.raise_for_status()  # Verifica se o download foi bem-sucedido

        # Garantir que o diretório de destino exista
        os.makedirs(diretorio_destino, exist_ok=True)

        nome_arquivo = url_pasta.split("/")[-1].split("?")[0] + ".zip"
        global caminho_completo_tratado
        caminho_completo = os.path.join(diretorio_destino, nome_arquivo)
        

        tamanho_total = int(response.headers.get('content-length', 0))
        tamanho_baixado = 0
        bloco_tamanho = 4096

        with open(caminho_completo, 'wb') as f:
            for dados in response.iter_content(bloco_tamanho):
                tamanho_baixado += len(dados)
                f.write(dados)
                progresso = (tamanho_baixado / tamanho_total) * 100
                barra_progresso['value'] = progresso
                janela.update_idletasks() 
                print(f"Progresso: {progresso:.2f}%", end='\r')
                variavel.set(f"Progresso: {progresso:.2f}%")
        global foi_baixado        
        foi_baixado = True
        original = os.path.join(diretorio_destino, nome_arquivo)
        caminho_normalizado = original.replace('/', '\\').replace('\\', '\\\\')
        caminho_completo_tratado = rf"{original}"
        
        print("########### Download concluido",caminho_completo_tratado)
        #messagebox.showinfo("Sucesso", f"Pasta baixada com sucesso como '{caminho_completo}'!")
        janela.destroy()
        return True
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao baixar a pasta: {e}")
        return False

# Link de compartilhamento da pasta (modificado para download)
url_pasta = 'https://www.dropbox.com/scl/fo/hfng15msydyiviiu84uxx/ANmWgP238pk0Bd8FILnw4Xc?rlkey=vcx8vl25gxxiuxp3rsiictbs8&e=1&st=3oiz3w3e&dl=0'
#url_pasta = "https://www.dropbox.com/scl/fi/kqpymwaxn03hl4dxr7k1r/video2.mov?rlkey=yv5qww3sjfiwv9x8697lgov08&st=yk0z4fin&dl=0"

# Diretório de destino onde o arquivo será salvo
diretorio_destino = r'C:\Users\Samuel\Desktop\TesteDrop'

#baixar_pasta_dropbox(url_pasta, diretorio_destino)
