import os
import sys
import webbrowser
from PyQt6.QtCore import Qt, QCoreApplication, QProcess
from PyQt6.QtWidgets import QMessageBox
import jwt
import requests
from Util import Tokens, Util
import Util.CustomWidgets as cw

class Interface(cw.Widget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(10, 10, 10, 10)
        
        h1 = cw.Label(f"{os.getlogin()}, seja bem vindo(a) ao AluraVideos!")
        h1.setObjectName("grande")
        h1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layoutPrincipal = cw.VBoxLayout()
        layoutPrincipal.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layoutPrincipal.addWidget(h1)
        
        self.dir = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos")
        self.tokens = os.path.join(self.dir,"credentials.json") 
        arquivos_inexistentes = []
        arquivos = [self.tokens]
        for arquivo in arquivos:
            if not os.path.exists(arquivo):
                arquivos_inexistentes.append(arquivo)
        
        if arquivos_inexistentes:
            h2 = cw.Label(f"<font color='red'>Você não está autenticado!</font>")
            h2.setObjectName("grande")
            h2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
            
            h3 = cw.Label(f"Por favor, se registre agora:")
            h3.setWordWrap(True)
            h3.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
            h3.setObjectName("medio")
            
            label_key = cw.Label(f"Login:")
            self.campo_key = cw.LineEdit()
            label_tokens = cw.Label(f"Senha:")
            self.campo_tokens = cw.LineEdit()
            
            salvar = cw.PushButton("Registrar")
            salvar.clicked.connect(self.salvarKeyEToken)
            
            layoutPrincipal.addWidget(h2)
            layoutPrincipal.addWidget(h3)
            layoutPrincipal.addWidget(label_key)
            layoutPrincipal.addWidget(self.campo_key)
            layoutPrincipal.addWidget(label_tokens)
            layoutPrincipal.addWidget(self.campo_tokens)
            layoutPrincipal.addWidget(salvar)
        else:  
            if not Tokens.LoadKeys():
                h2 = cw.Label(f"<font color='red'>Seus tokens de acesso estão desatualizados!</font>")
                h2.setObjectName("grande")
                h2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

                h3 = cw.Label(f"Por favor, atualize suas chaves de acesso:")
                h3.setWordWrap(True)
                h3.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
                h3.setObjectName("medio")
                
                label_key = cw.Label(f"Login:")
                self.campo_key = cw.LineEdit()
                label_tokens = cw.Label(f"Senha:")
                self.campo_tokens = cw.LineEdit()
                
                salvar = cw.PushButton("Registrar")
                salvar.clicked.connect(self.salvarKeyEToken)
                
                layoutPrincipal.addWidget(h2)
                layoutPrincipal.addWidget(h3)
                layoutPrincipal.addWidget(label_key)
                layoutPrincipal.addWidget(self.campo_key)
                layoutPrincipal.addWidget(label_tokens)
                layoutPrincipal.addWidget(self.campo_tokens)
                layoutPrincipal.addWidget(salvar)
                
            else:
                label_desc = cw.Label("\n\nAluraVideos é um software desenvolvido por Samuel Mariano para o time de AudioVisual da Alura Online. Cujo seu principal objetivo é otimizar e automatizar processos do dia-dia.")
                label_desc.setWordWrap(True)
                label_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label_desc.setObjectName("medio-normal")
                
                label_ajuda = cw.Label("\nPrecisa de ajuda? Acesse a nossa documentação oficial e obtenha algumas dicas! xD\n")
                label_ajuda.setWordWrap(True)
                label_ajuda.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label_ajuda.setObjectName("medio")
                
                button_ajuda = cw.PushButton("Acessar documentação")
                cw.setSizePolicy(button_ajuda).setFixed()
                button_ajuda.clicked.connect(lambda: webbrowser.open("https://www.notion.so/grupoalura/AluraVideos-8589d6eab57744b7a9ccf4080c0b6bca?pvs=25"))
                
                layoutPrincipal.addWidget(label_desc)
                layoutPrincipal.addWidget(label_ajuda)
                layoutPrincipal.addLayout(cw.alignWidget(button_ajuda))
        
        self.setLayout(layoutPrincipal)
        
    def salvarKeyEToken(self):
        try:
            os.remove(self.tokens)
        except Exception as e:
            print(e)         
        
        payload = {
            "username": self.campo_key.text().upper(),
            "password": self.campo_tokens.text()
        }
        try:
            response = requests.post("https://aluravideosapi.onrender.com/login",
                            json=payload,
                            timeout=60)
            
            if response.status_code == 200:
                # Se a autenticação for bem-sucedida, obtem o token de acesso
                print("Autenticação bem-sucedida.")
                
                key = "O+k9G/kMiXqcm+FRKGvAWQ=="
                encoded_jwt = jwt.encode(payload, key, algorithm='HS256')
            
                with open(self.tokens, 'w') as f:
                    f.write(encoded_jwt)    
                    
                QCoreApplication.quit()
                QProcess.startDetached(sys.executable, sys.argv)  
            else:
                # Em caso de erro
                QMessageBox.information(None,"Erro","Dados de login inválidos!")
                print("Falha na autenticação:", response.json().get("message"))
        except Exception as e:
            Util.LogError("Home/Auth","Ocorreu um erro ao processar seu login na API.",True)