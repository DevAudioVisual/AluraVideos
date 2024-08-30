import re
import threading
import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
from Util import CustomWidgets, Styles, Util
import os
import datetime

class criarChatBot():
    def __init__(self, root):
        # TODO bloquear a API key
        genai.configure(api_key='AIzaSyA-yUmOxeC31ud7fhgCkzTnHqxez0Z2DHo')
        self.janela = tk.Toplevel(root, padx=20, pady=20)
        self.janela.title("Google Gemini - ChatBot")
        icone = Util.pegarImagem("gemini.png")
        self.janela.iconbitmap(False, icone)
        self.janela.configure(bg=Styles.cor_fundo, padx=10, pady=10)

        self.historico = scrolledtext.ScrolledText(
            self.janela,
            wrap=tk.WORD,
            font=("Helvetica", 12),
            foreground="white",
            relief=tk.SUNKEN,
            borderwidth=2,
            padx=10,
            pady=5,
            background=Styles.cor_fundo
        )

        # Configurar tags com diferentes estilos e alinhamentos
        self.historico.tag_configure("voce", foreground="teal", font=("Helvetica", 12, "bold"), justify='left')
        self.historico.tag_configure("gemini", foreground="green", font=("Helvetica", 12, "bold"), justify='left',
                                     spacing1=10)
        self.historico.tag_configure("mensagem", foreground="white", font=("Inter", 12))

        self.historico.pack(fill=tk.BOTH, expand=True)

        self.entrada = CustomWidgets.CustomEntry(self.janela, width=800)
        self.entrada.pack(side='left', pady=20)

        self.botao_enviar = CustomWidgets.CustomButton(self.janela, text="Enviar", command=self.enviar_mensagem)
        self.botao_enviar.pack(padx=10, side='left', pady=20)

        self.entrada.getEntry().bind("<Return>", self.enviar_mensagem)

        self.diretorio_salvar = os.path.join(os.path.expanduser("~"), "Documents", "S_Videos", "ChatBot")
        os.makedirs(self.diretorio_salvar, exist_ok=True)

        self.data_inicio_conversa = datetime.datetime.now().strftime('%Y-%m-%d')
        self.primeira_pergunta = None
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_janela)



    def enviar_mensagem(self, event=None):
        self.mensagem_usuario = self.entrada.getEntry().get()
        if self.primeira_pergunta is None:
            self.primeira_pergunta = self.mensagem_usuario

        self.historico.insert(tk.END, "Você: ", "voce")
        self.historico.insert(tk.END, self.mensagem_usuario + "\n\n", "mensagem")  # Adicionar pady extra
        self.entrada.getEntry().delete(0, tk.END)

        # Exibir "Aguardando..." imediatamente
        self.historico.insert(tk.END, "Gemini: ", "gemini")
        self.historico.insert(tk.END, "Aguardando...\n\n", "mensagem")
        self.historico.see(tk.END)  # Rolar para o final

        # Iniciar uma thread para obter a resposta do Gemini
        threading.Thread(target=self.obter_resposta_gemini).start()

    def obter_resposta_gemini(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro') 
        #self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.response = self.model.generate_content(self.historico.get('1.0', tk.END))
        self.janela.after(0, self.atualizar_historico)

    def atualizar_historico(self):
        self.historico.delete("end-3l", tk.END) 
        self.historico.insert(tk.END, "Gemini: ", "gemini")
        resposta_sem_formatacao = re.sub(r'<[^>]+>', '', self.response.text.replace("Assistente:", ""))
        self.historico.insert(tk.END, resposta_sem_formatacao + "\n", "mensagem") 
        self.janela.after(100, lambda: self.historico.insert(tk.END, "\n", "mensagem"))  # Adicionar o padding após o atraso
        self.historico.see(tk.END)

    def fechar_janela(self):
        nome_arquivo_seguro = re.sub(r'[<>:"/\\|?*]', '', self.primeira_pergunta[:50])
        if nome_arquivo_seguro:
            nome_arquivo = f"{nome_arquivo_seguro}_{self.data_inicio_conversa}.md"
        else:
            nome_arquivo = f"conversa_{self.data_inicio_conversa}.md"

        caminho_arquivo = os.path.join(self.diretorio_salvar, nome_arquivo)

        conteudo = self.historico.get('1.0', tk.END)
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)

        self.janela.destroy()

        self.janela.destroy()
        
