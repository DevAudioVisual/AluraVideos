from functools import lru_cache
import os
from PyQt6.QtWidgets import QDialog,QTableWidgetItem,QHeaderView, QMessageBox
import jwt
import requests
import Util.CustomWidgets as cw

@lru_cache(maxsize=128,typed=True)
class TabelaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painel Administrativo")
        self.showMaximized()
        # Configuração do layout e da tabela
        self.layout = cw.VBoxLayout()
        self.tableWidget = cw.TableWidget()
        self.itensTabela()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget.cellClicked.connect(self.on_cell_clicked)
        
        self.group_adicionar = cw.GroupBox("Usuario")
        self.layout_adicionar = cw.GridLayout()
        self.group_adicionar.setLayout(self.layout_adicionar)
        
        self.group_mysql = cw.GroupBox("MySql")
        self.layout_mysql = cw.GridLayout()
        self.group_mysql.setLayout(self.layout_mysql)
        
        lbl_Nome = cw.Label("Nome para registro:")
        self.campoNome = cw.LineEdit()
        lbl_Time = cw.Label("Time para registro:")
        self.campoTime = cw.ComboBox()
        self.campoTime.addItems(["Videos","Creops","Instrutor","Produtor","Liderança","Estudio"])
        
        lbl_ComandoSQL = cw.Label("Comando MySql")
        self.campoComandoMySQL = cw.QLineEdit()
        botaoComandoMySql = cw.PushButton("Executar")
        botaoComandoMySql.clicked.connect(self.itensTabelaComando)
        
        botaoAdicionar = cw.PushButton("Adicionar")
        botaoAdicionar.clicked.connect(self.adicionar)
        botaoAdicionar.setStyleSheet("background-color: green;")
        botaoRemover = cw.PushButton("Remover")
        botaoRemover.setStyleSheet("background-color: red;")
        botaoRemover.clicked.connect(self.remover)
        botaoRecarregar = cw.PushButton("Recarregar tabela")
        botaoRecarregar.clicked.connect(self.recarregar)
        
        self.layout_adicionar.addWidget(lbl_Nome,0,0)
        self.layout_adicionar.addWidget(self.campoNome,1,0)
        self.layout_adicionar.addWidget(lbl_Time,2,0)
        self.layout_adicionar.addWidget(self.campoTime,3,0)
        self.layout_adicionar.addWidget(botaoAdicionar,4,0)
        self.layout_adicionar.addWidget(botaoRemover,4,1)
        
        self.layout_mysql.addWidget(lbl_ComandoSQL,0,0)
        self.layout_mysql.addWidget(self.campoComandoMySQL,1,0)
        self.layout_mysql.addWidget(botaoComandoMySql,1,1)
    
        
        self.layout.addWidget(self.group_adicionar)
        self.layout.addWidget(self.group_mysql)
        self.layout.addWidget(botaoRecarregar)
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        
    def on_cell_clicked(self, row, column):
        # Verifica se a coluna clicada é a coluna "Nome" (coluna 1 neste exemplo)
        if column == 0:
            nome_item = self.tableWidget.item(row, column)  # Obtem o item da célula
            if nome_item:  # Verifica se o item existe
                nome = nome_item.text()
                self.campoNome.setText(nome)
    def adicionar(self):
      username = self.decoded_jwt.get("username")
      password = self.decoded_jwt.get("password")
      response = requests.post("https://samuka.pythonanywhere.com/registrar",
                         json={
                             "username": username,
                             "password": password,
                             
                             "usernameRegistro": self.campoNome.text().upper(),
                             "cargoRegistro": self.campoTime.currentText(),
                             "adm": False},
                         
                         timeout=15)
      if response.status_code == 200:
          print("Autenticação bem-sucedida.")
      else:
          print("Falha na autenticação:", response.content)
      
      self.tableWidget.clearContents()
      self.itensTabela()  
    def remover(self):
      username = self.decoded_jwt.get("username")
      password = self.decoded_jwt.get("password")
      response = requests.post("https://samuka.pythonanywhere.com/deletar",
                         json={
                             "username": username,
                             "password": password,
                             
                             "usertoremove": self.campoNome.text().upper(),
                             },
                         
                         timeout=15)
      if response.status_code == 200:
          print("Autenticação bem-sucedida.")
      else:
          print("Falha na autenticação:", response.content)
      
      self.tableWidget.clearContents()
      self.itensTabela()  
    def itensTabela(self):    
        try:
          key = "O+k9G/kMiXqcm+FRKGvAWQ=="
          dir = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos")
          tokens = os.path.join(dir,"credentials.json") 
          with open(tokens, 'r') as f:
              encoded_jwt = f.read()  # Lê o token do arquivo
              self.decoded_jwt = jwt.decode(encoded_jwt, key, algorithms=['HS256'])
          response = requests.post("https://samuka.pythonanywhere.com/isadm",json=self.decoded_jwt,timeout=60)
          if response.status_code == 200:
            json_dados = response.json().get("dados")
            self.tableWidget.setRowCount(len(json_dados))
            self.tableWidget.setColumnCount(5)
            self.tableWidget.setHorizontalHeaderLabels(["Nome", "Senha", "Time", "ADM", "Logins"])
            # Populando a QTableWidget com os dados do JSON
            for row_index, row_data in enumerate(json_dados):
                self.tableWidget.setItem(row_index, 0, QTableWidgetItem(row_data["nome"]))
                self.tableWidget.setItem(row_index, 1, QTableWidgetItem(row_data["senha"]))
                self.tableWidget.setItem(row_index, 2, QTableWidgetItem(row_data["time"]))
                self.tableWidget.setItem(row_index, 3, QTableWidgetItem(str(row_data["adm"]))) 
                self.tableWidget.setItem(row_index, 4, QTableWidgetItem(str(row_data["LOGINS"]))) 
          else:
            print(response.content)
        except Exception as e:
          print(e)
    def itensTabelaComando(self):    
        try:
          key = "O+k9G/kMiXqcm+FRKGvAWQ=="
          dir = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos")
          tokens = os.path.join(dir,"credentials.json") 
          with open(tokens, 'r') as f:
              encoded_jwt = f.read()  # Lê o token do arquivo
              self.decoded_jwt = jwt.decode(encoded_jwt, key, algorithms=['HS256'])
          json = {
              "username": self.decoded_jwt["username"],
              "password": self.decoded_jwt["password"],
              "comando": self.campoComandoMySQL.text()
          }
          response = requests.post("https://samuka.pythonanywhere.com/comando",json=json,timeout=60)
          
          if response.status_code == 200:
            json_dados = response.json().get("dados")
            print(json_dados)
            self.tableWidget.setRowCount(len(json_dados))
            self.tableWidget.setColumnCount(5)
            self.tableWidget.setHorizontalHeaderLabels(["Nome", "Senha", "Time", "ADM", "Logins"])
            # Populando a QTableWidget com os dados do JSON
            for row_index, row_data in enumerate(json_dados):
                self.tableWidget.setItem(row_index, 0, QTableWidgetItem(row_data["nome"]))
                self.tableWidget.setItem(row_index, 1, QTableWidgetItem(row_data["senha"]))
                self.tableWidget.setItem(row_index, 2, QTableWidgetItem(row_data["time"]))
                self.tableWidget.setItem(row_index, 3, QTableWidgetItem(str(row_data["adm"]))) 
                self.tableWidget.setItem(row_index, 4, QTableWidgetItem(str(row_data["LOGINS"]))) 
          elif response.status_code == 401:
            QMessageBox.information(None,"Erro","Erro na requisição ao banco de dados.\nVerifique o comando e tente novamente.")
          else:
            QMessageBox.information(None,"Erro","Ocorreu um erro ao realizar sua requisição ao banco de dados.")
        except Exception as e:
          print(e)
    def recarregar(self):
        self.tableWidget.clearContents()
        self.itensTabela()  
        