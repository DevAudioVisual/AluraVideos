import os
import shutil
import sys
import webbrowser
from PyQt6.QtWidgets import QWidget, QVBoxLayout,QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt6.QtCore import Qt,QCoreApplication,QProcess
from PyQt6.QtGui import QCursor

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(10, 10, 10, 10)
        
        h1 = QLabel(f"{os.getlogin()}, seja bem vindo(a) ao AluraVideos!")
        h1.setObjectName("grande")
        h1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layoutPrincipal = QVBoxLayout()
        layoutPrincipal.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layoutPrincipal.addWidget(h1)
        
        self.dir = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos")
        self.tokens = os.path.join(self.dir,"tokens.yml")
        self.key = os.path.join(self.dir,"key.key")    
        arquivos_inexistentes = []
        arquivos = [self.tokens, self.key]
        for arquivo in arquivos:
            if not os.path.exists(arquivo):
                arquivos_inexistentes.append(arquivo)
        
        if arquivos_inexistentes:
            h2 = QLabel(f"<font color='red'>Você não está autenticado!</font>")
            h2.setObjectName("grande")
            h2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
            self.nome_arquivos = []
            for a in arquivos_inexistentes:
                self.nome_arquivos.append(os.path.basename(a))
            h3 = QLabel(f"Por favor, registre suas chaves de acesso:")
            h3.setWordWrap(True)
            h3.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
            h3.setObjectName("medio")
            
            label_key = QLabel(f"Key:")
            self.campo_key = QLineEdit()
            label_tokens = QLabel(f"Token:")
            self.campo_tokens = QLineEdit()
            
            salvar = QPushButton("Registrar")
            salvar.clicked.connect(self.salvarKeyEToken)
            
            layoutPrincipal.addWidget(h2)
            layoutPrincipal.addWidget(h3)
            layoutPrincipal.addWidget(label_key)
            layoutPrincipal.addWidget(self.campo_key)
            layoutPrincipal.addWidget(label_tokens)
            layoutPrincipal.addWidget(self.campo_tokens)
            layoutPrincipal.addWidget(salvar)
        else:  
            label_desc = QLabel("\n\nAluraVideos é um software desenvolvido por Samuel Mariano para o time de AudioVisual da Alura Online. Cujo seu principal objetivo é otimizar e automatizar processos do dia-dia.")
            label_desc.setWordWrap(True)
            label_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_desc.setObjectName("medio-normal")
            
            label_ajuda = QLabel("\nPrecisa de ajuda? Acesse a nossa documentação oficial e obtenha algumas dicas! xD\n")
            label_ajuda.setWordWrap(True)
            label_ajuda.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_ajuda.setObjectName("medio")
            
            button_ajuda = QPushButton("Acessar documentação")
            button_ajuda.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            button_ajuda.clicked.connect(lambda: webbrowser.open("https://www.notion.so/grupoalura/AluraVideos-8589d6eab57744b7a9ccf4080c0b6bca?pvs=25"))
            
            layoutPrincipal.addWidget(label_desc)
            layoutPrincipal.addWidget(label_ajuda)
            layoutPrincipal.addWidget(button_ajuda)
            #layoutPrincipal.addWidget(VimeoPlayer())
        
        self.setLayout(layoutPrincipal)
    def salvarKeyEToken(self):
        with open(self.key, 'w') as f:
            f.write(self.campo_key.text())
        with open(self.tokens, 'w') as f:
            f.write(self.campo_tokens.text())    
        QCoreApplication.quit()
        QProcess.startDetached(sys.executable, sys.argv)
    def buscarEregistrar(self):
        filenames, _ = QFileDialog.getOpenFileNames(
                self,
                "Selecione os arquivos",
                "",
                "Arquivos Key e YML (*.key *.yml)"  # Filtro modificado
            )
        if filenames:
            pasta_destino = self.dir

            for filename in filenames:
                try:
                    shutil.copy2(filename, pasta_destino)
                    os.remove(filename)
                    print(f"Arquivo {filename} movido com sucesso!")
                    QCoreApplication.quit()
                    QProcess.startDetached(sys.executable, sys.argv)
                    
                except Exception as e:
                    print(f"Erro ao mover o arquivo {filename}: {e}")