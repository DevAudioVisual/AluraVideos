import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

def renomear_arquivos(numeros_aulas, nomes_aulas):
    try:
        # Cria um dicionário para mapear os números das aulas com os nomes completos
        mapa_aulas = {}
        
        for numero in numeros_aulas:
            # Extrai o número com extensão do arquivo (ex: 1.1.ext)
            numero_extr = os.path.basename(numero)
            
            # Encontra o nome completo que corresponde ao número
            for nome in nomes_aulas:
                # Se o número (X.X) estiver no nome do arquivo completo, mapeia
                if os.path.splitext(numero_extr)[0] in os.path.basename(nome):  
                    mapa_aulas[numero] = nome
                    break

        # Verifica se o dicionário foi corretamente preenchido
        if not mapa_aulas:
            raise ValueError("Nenhuma correspondência encontrada entre números e nomes de aulas.")

        # Renomeia os arquivos
        for numero, nome_completo in mapa_aulas.items():
            try:
                nome_arquivo_antigo = numero  # Caminho do arquivo com o número (X.X) e extensão
                # Novo nome do arquivo, mantendo o caminho e alterando o nome baseado no número completo
                nome_arquivo_novo = os.path.join(os.path.dirname(nome_arquivo_antigo), os.path.basename(nome_completo))
                
                os.rename(nome_arquivo_antigo, nome_arquivo_novo)
                print(f"Arquivo renomeado: {nome_arquivo_antigo} -> {nome_arquivo_novo}")
            except FileNotFoundError:
                print(f"Erro: Arquivo não encontrado: {nome_arquivo_antigo}")
            except PermissionError:
                print(f"Erro: Permissão negada para renomear: {nome_arquivo_antigo}")
            except Exception as e:
                print(f"Erro ao renomear {nome_arquivo_antigo}: {e}")

    except Exception as e:
        QMessageBox.critical(None, "Erro", f"Ocorreu um erro ao renomear os arquivos:\n{e}")

class Interface(QWidget):
    def __init__(self):
        super().__init__()

        self.setContentsMargins(10, 10, 10, 10)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)


        self.label_videos = QLabel("Videos para renomear:")
        self.campo_videos = QLineEdit()
        self.campo_videos.setPlaceholderText("Diga os vídeos para renomear")
        self.campo_videos.setClearButtonEnabled(True)
        self.action_campo_videos = self.campo_videos.addAction(QIcon(r"Assets\Images\folder.png"),QLineEdit.ActionPosition.TrailingPosition)
        self.action_campo_videos.triggered.connect(self.selecionar_pasta_numeros)     
        
        self.label_reference = QLabel("Videos de referência:")
        self.campo_reference = QLineEdit()
        self.campo_reference.setPlaceholderText("Diga os vídeos de referência")
        self.campo_reference.setClearButtonEnabled(True)
        self.action_campo_reference = self.campo_reference.addAction(QIcon(r"Assets\Images\folder.png"),QLineEdit.ActionPosition.TrailingPosition)
        self.action_campo_reference.triggered.connect(self.selecionar_pasta_nomes)     
        

        self.botao_renomear = QPushButton("Renomear Arquivos")
        self.botao_renomear.clicked.connect(self.renomear)
        
        
        layout.addWidget(self.label_videos)
        layout.addWidget(self.campo_videos)
        layout.addWidget(self.label_reference)
        layout.addWidget(self.campo_reference)
        layout.addWidget(self.botao_renomear)

        self.setLayout(layout)

    def selecionar_pasta_numeros(self):
        self.pasta_numeros = QFileDialog.getExistingDirectory(self, "Selecione a pasta com os arquivos de números das aulas")
        self.campo_videos.setText(self.pasta_numeros)

    def selecionar_pasta_nomes(self):
        self.pasta_nomes = QFileDialog.getExistingDirectory(self, "Selecione a pasta com os arquivos de nomes completos das aulas")
        self.campo_reference.setText(self.pasta_nomes)

    def renomear(self):
        if not self.pasta_numeros or not self.pasta_nomes:
            QMessageBox.warning(None, "Aviso", "Selecione ambas as pastas com os números e os nomes das aulas.")
            return

        try:
            # Busca todos os arquivos nas pastas selecionadas
            numeros_aulas = [os.path.join(self.pasta_numeros, f) for f in os.listdir(self.pasta_numeros) if os.path.isfile(os.path.join(self.pasta_numeros, f))]
            nomes_aulas = [os.path.join(self.pasta_nomes, f) for f in os.listdir(self.pasta_nomes) if os.path.isfile(os.path.join(self.pasta_nomes, f))]
            
            renomear_arquivos(numeros_aulas, nomes_aulas)
            QMessageBox.information(None, "Sucesso", "Arquivos renomeados com sucesso!")
        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Ocorreu um erro ao renomear os arquivos:\n{e}")