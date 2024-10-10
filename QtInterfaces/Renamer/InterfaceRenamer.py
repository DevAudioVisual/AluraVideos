
import os
import re
import time
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QScrollArea, QPushButton ,QFileDialog,QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from bs4 import BeautifulSoup
import pandas as pd
import requests
from Config import LoadConfigs
global Config

class Interface(QWidget):
    def __init__(self):
        super().__init__() 
        
        self.setContentsMargins(10, 20, 10, 10)
        
        self.entrada_videos = {}
        self.dados = {}
        
        self.df = LoadConfigs.Config.getDataFrame("ConfigCriarProjeto")
        self.config = LoadConfigs.Config.getConfigData("ConfigCriarProjeto")
        
        self.label_h1 = QLabel("Renomeador de arquivos")
        self.label_h1.setObjectName("grande")
        self.label_h1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label_h2 = QLabel("Os videos precisam estar no formato X.X para serem reconhecidos")
        self.label_h2.setObjectName("medio")
        self.label_h2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label_videos = QLabel("Videos:")
        self.campo_videos = QLineEdit()
        self.campo_videos.setPlaceholderText("Busque pelos vídeos para renomear")
        self.campo_videos.setClearButtonEnabled(True)
        self.action_campo_videos = self.campo_videos.addAction(QIcon(r"Assets\Images\folder.png"),QLineEdit.ActionPosition.TrailingPosition)
        self.action_campo_videos.triggered.connect(self.buscarVideos)
        
        self.label_sheets = QLabel("Planilha:")
        self.campo_sheets = QLineEdit()
        self.campo_sheets.setPlaceholderText("Digite o link para a planilha")
        self.campo_sheets.setClearButtonEnabled(True)
        self.action_campo_sheets = self.campo_sheets.addAction(QIcon(r"Assets\Images\forms.png"),QLineEdit.ActionPosition.TrailingPosition)
        self.action_campo_sheets.triggered.connect(lambda: self.buscar_na_planilha())
        
        self.label_id = QLabel("ID do curso:")
        self.campo_id = QLineEdit()
        self.campo_id.setPlaceholderText("Digite o ID do curso ou busque pela planilha")
        self.campo_id.setClearButtonEnabled(True)
        
        self.label_sufixo = QLabel("Sufixo:")
        self.campo_sufixo = QLineEdit()
        self.campo_sufixo.setPlaceholderText("Digite o ID do curso ou busque pela planilha")
        self.campo_sufixo.setClearButtonEnabled(True)
        
        self.label_formato = QLabel("Padrão:")
        self.campo_formato = QLineEdit()
        self.campo_formato.setText("{id}-video{aula}-{video}")
        self.campo_formato.setReadOnly(True)
        
        self.buttonrenomear = QPushButton("Renomear")
        self.buttonrenomear.clicked.connect(self.renomear)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        layout.addWidget(self.label_h1)
        layout.addWidget(self.label_videos)
        layout.addWidget(self.campo_videos)
        layout.addWidget(self.label_sheets)
        layout.addWidget(self.campo_sheets)
        layout.addWidget(self.label_id)
        layout.addWidget(self.campo_id)
        layout.addWidget(self.label_sufixo)
        layout.addWidget(self.campo_sufixo)
        layout.addWidget(self.label_formato)
        layout.addWidget(self.campo_formato)
        
        
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Widget de conteúdo para a área de rolagem
        widget_conteudo = QWidget()
        scroll_area.setWidget(widget_conteudo)

        # Layout do widget de conteúdo
        layout_conteudo = QVBoxLayout(widget_conteudo)  

        # Seu layout2 (com os outros layouts)
        self.layout2 = QGridLayout()
        self.layout2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.layoutvideos = QVBoxLayout()
        self.layoutvideos.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.layoutnovosvideos = QVBoxLayout()
        self.layoutnovosvideos.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.layout2.addLayout(self.layoutvideos, 0, 0)
        self.layout2.addLayout(self.layoutnovosvideos, 0, 1)

        # Adiciona layout2 ao layout de conteúdo da scroll area
        layout_conteudo.addLayout(self.layout2)  
        layout.addWidget(self.buttonrenomear)

        self.setLayout(layout)
    def renomear(self):
        pasta = os.path.dirname(self.campo_videos.text())
        erro = False
        for arquivo_original, entrada_nome in self.entrada_videos.items():
            novo_nome = entrada_nome.text()
            arquivo_original_tratado = arquivo_original
            if novo_nome:
                nome_sem_extensao, extensao = os.path.splitext(arquivo_original_tratado)
                
                numero_aula_regex = r"(\d+\.\d+)"
                match = re.search(numero_aula_regex, nome_sem_extensao)
                if match:
                    numero_aula = match.group(1)
                else:
                    numero_aula = None
                
                novo_nome_arquivo = f"{self.campo_id.text()}-video{numero_aula}-{novo_nome}-{self.campo_sufixo.text()}{extensao}" if self.campo_sufixo.text() != "" else f"{self.campo_id.text()}-video{numero_aula}-{novo_nome}{extensao}"
                caminho_antigo = os.path.join(pasta, arquivo_original_tratado)
                caminho_novo = os.path.join(pasta, novo_nome_arquivo)
                MAX_TENTATIVAS = 2
                TEMPO_ESPERA = 1
                for tentativa in range(MAX_TENTATIVAS):
                    try:
                        os.rename(os.path.normpath(caminho_antigo), os.path.normpath(caminho_novo))
                        break  
                    except PermissionError as e:
                        if tentativa < MAX_TENTATIVAS - 1:
                            print(f"Tentativa {tentativa + 1} falhou. Aguardando {TEMPO_ESPERA} segundos...")
                            time.sleep(TEMPO_ESPERA)
                        else:
                            erro = True
                            print(f"Erro: Não foi possível renomear o arquivo {caminho_antigo} após {MAX_TENTATIVAS} tentativas. {e}")
        if erro == False:
            print("Sucesso!")
            #messagebox.showinfo("Sucesso", "Vídeos renomeados com sucesso!")
        else:
            print("Erro")
            #messagebox.showerror("Erro", "Não foi possivel renomear os arquivos.")   
    def atualizar_entradas_videos(self):
        for arquivo, entrada_nome in self.entrada_videos.items():
            nome_sem_extensao, _ = os.path.splitext(os.path.basename(arquivo))
            
            numero_aula_regex = r"(\d+\.\d+)"
            match = re.search(numero_aula_regex, nome_sem_extensao)
            if match:
                numero_aula = match.group(1)
            else:
                numero_aula = None
            
            nome_aula = self.dados.get(f"Aula {numero_aula}", "")
            entrada_nome.setText(nome_aula)
            if nome_aula:
                print(nome_aula)
                
    def buscarVideos(self):
        options = QFileDialog.Option.ReadOnly
        # Define os filtros para arquivos de vídeo
        filters = "Arquivos de Vídeo (*.mp4 *.avi *.mov *.mkv);;Todos os Arquivos (*)"
        # Abre a caixa de diálogo para seleção de múltiplos arquivos
        file_names, _ = QFileDialog.getOpenFileNames(self, "Selecionar Vídeos", "", filters, options=options)
        if file_names:
            self.campo_videos.setText(file_names[0])
            for file_name in file_names:
                campo_video = QLineEdit()
                campo_video.setText(os.path.basename(file_name))
                campo_video.setReadOnly(True)
                
                campo_video_novo = QLineEdit()
                self.layoutvideos.addWidget(campo_video)
                self.layoutnovosvideos.addWidget(campo_video_novo)
                self.entrada_videos[os.path.basename(file_name)] = campo_video_novo
                
    def buscar_na_planilha(self):
        spreadsheet_url = self.campo_sheets.text()
        #if self.entradas_videos == None:
            #messagebox.showerror("Erro", "Nenhum arquivo de vídeo fornecido.")
            #return  
        def extrair_titulo_planilha(url_planilha):
            try:
                # Faz a requisição à página da planilha
                response = requests.get(url_planilha)
                response.raise_for_status()  # Lança uma exceção se houver erro na requisição

                # Analisa o HTML da página
                soup = BeautifulSoup(response.content, 'html.parser')

                # Tenta encontrar o título na estrutura HTML (pode precisar ajustar isso)
                titulo_elemento = soup.find('title')
                if titulo_elemento:
                    titulo = titulo_elemento.text.strip()
                    # Remove o sufixo "- Google Sheets" se existir
                    titulo = titulo.replace(" - Google Sheets", "")
                    padrao = r"^\d{4}"  # Expressão regular para encontrar 4 dígitos no início da string
                    correspondencia = re.match(padrao, titulo)
                    return correspondencia.group(0)
                else:
                    return None  # Retorna None se não encontrar o título

            except requests.exceptions.RequestException as e:
                print(f"Erro ao acessar a página: {e}")
                return None
        if spreadsheet_url:
            self.campo_id.setText(extrair_titulo_planilha(spreadsheet_url))
            padrao_id = r"/spreadsheets/d/([a-zA-Z0-9-_]+)"
            match = re.search(padrao_id, spreadsheet_url)
            try:
                if match:
                    spreadsheet_id = match.group(1)
                    csv_export_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv'

                    df = pd.read_csv(csv_export_url, header=None)
                    try:
                        coluna_a = df.iloc[:, 0]
                        coluna_b = df.iloc[:, 1]

                        padrao_aula = r"Aula \d+\.\d+"

                        for i in range(len(coluna_a)):
                            match = re.match(padrao_aula, str(coluna_a[i]))
                            if match:
                                if pd.notna(coluna_a[i]) and re.search(padrao_aula, str(coluna_a[i])):
                                    self.dados[coluna_a[i]] = coluna_b[i]
                            else: 
                                #Forçar erro
                                df.iloc[:,20]

                        self.atualizar_entradas_videos()
                        print("Tentando planejamento")
                    except Exception as e:
                        try:
                            padrao = r"gid=(\d+)"
                            gid = re.search(padrao, spreadsheet_url).group(1)
                            csv_export_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}'
                            df = pd.read_csv(csv_export_url, header=0,skiprows=2)
                            coluna_d = df.iloc[:, 3]

                            padrao_aula = r"(\d+\.\d+)-(.*)"

                            for i in range(len(coluna_d)):
                                if pd.notna(coluna_d[i]) and re.search(padrao_aula, str(coluna_d[i])):
                                    match = re.match(r"(\d+\.\d+)-(.*)", str(coluna_d.iloc[i]))  # Aplica a regex
                                    if match:
                                        numero_aula = match.group(1)
                                        nome_aula = match.group(2).strip()
                                        self.dados[f"Aula {numero_aula}"] = nome_aula

                            print("Tentando matriz")
                            self.atualizar_entradas_videos()
                        except Exception as e:
                            print(e)
            except Exception as e:
                print(e)
        
