import csv
import tempfile
import os

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, 
                             QHeaderView, QFileDialog,QWidget)

def criar_tabela(video_resume):
    try:
        # Cria um arquivo temporário
        with tempfile.NamedTemporaryFile(mode='w', newline='', delete=False, suffix=".csv") as csvfile:
            nome_arquivo = csvfile.name
            writer = csv.writer(csvfile)

            # Escreve o cabeçalho
            writer.writerow(["Nome", "Timecode", "Classe", "Score"])

            # Escreve os dados, agrupando e adicionando separadores
            ultima_classe = None
            for video, itens in video_resume.items():
                for classe, ocorrencias in itens.items():
                    for ocorrencia in ocorrencias:
                        timecode = ocorrencia['timecode']
                        score = ocorrencia['score']
                        if video != ultima_classe:
                            writer.writerow([])  # Adiciona uma linha vazia como separador
                            ultima_classe = video
                        for item in itens:
                            writer.writerow([video, timecode, classe, score])

        # Abre a nova janela com a tabela (usando QDialog)
        tabela_dialog = TabelaDialog(nome_arquivo)
        tabela_dialog.exec()

    except Exception as e:
        print(f"Erro ao criar a tabela: {e}")

class TabelaDialog(QDialog):
    def __init__(self, nome_arquivo):
        super().__init__()
        self.setWindowTitle("Tabela")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Cria a tabela
        self.tabela = QTableWidget()
        layout.addWidget(self.tabela)

        # Abre o arquivo CSV
        with open(nome_arquivo, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)

            # Define o número de colunas
            self.tabela.setColumnCount(len(next(reader)))

            # Define o cabeçalho da tabela
            self.tabela.setHorizontalHeaderLabels(["Nome", "Timecode", "Classe", "Score"])

            # Adiciona as linhas à tabela, com separadores
            for linha in reader:
                row = self.tabela.rowCount()
                self.tabela.insertRow(row)
                if not any(linha):  # Verifica se a linha está vazia (separador)
                    self.tabela.setRowHidden(row, True)  # Oculta a linha do separador
                    continue
                for col, item in enumerate(linha):
                    self.tabela.setItem(row, col, QTableWidgetItem(item))

        # Ajusta o tamanho das colunas
        self.tabela.resizeColumnsToContents()
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Botão para salvar a tabela
        #botao_salvar = QPushButton("Salvar Tabela")
        #layout.addWidget(botao_salvar)
        #botao_salvar.clicked.connect(lambda: salvar_tabela(nome_arquivo, self.tabela))

def salvar_tabela(nome_arquivo_original, tabela):

    try:
        # Abre a caixa de diálogo para salvar o arquivo
        opcoes = QFileDialog.DontUseNativeDialog  # Corrigido: acessa a opção diretamente
        nome_arquivo, _ = QFileDialog.getSaveFileName(None, "Salvar Tabela", "", "CSV Files (*.csv);;All Files (*)", options=opcoes)
        if nome_arquivo:
            # Salva a tabela no novo arquivo
            with open(nome_arquivo, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Escreve o cabeçalho
                writer.writerow([tabela.horizontalHeaderItem(col).text() for col in range(tabela.columnCount())])
                # Escreve os dados
                for row in range(tabela.rowCount()):
                    writer.writerow([tabela.item(row, col).text() for col in range(tabela.columnCount())])

            print(f"Tabela salva em {nome_arquivo}")

            # Exclui o arquivo temporário original
            os.remove(nome_arquivo_original)
            print(f"Arquivo temporário excluído: {nome_arquivo_original}")

    except Exception as e:
        print(f"Erro ao salvar a tabela: {e}")
