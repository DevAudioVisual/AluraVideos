from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton,QFileDialog,QComboBox, QMessageBox
from PyQt6.QtCore import Qt,QTimer
from Models.S3 import S3Model


class Interface(QWidget):
    def __init__(self):
        super().__init__()
        
        self.model = S3Model.S3Model()
        self.GridLayout = QGridLayout()
        self.GridLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.GridLayout.setContentsMargins(10, 20, 10, 10)
        self.start()
        self.setLayout(self.GridLayout)
        
    def start(self):
      self.limpar()    
      if self.model.hasToken(): 
        bota_iniciar_conexao = QPushButton("Iniciar Conexão")
        bota_iniciar_conexao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        bota_iniciar_conexao.clicked.connect(lambda: bota_iniciar_conexao.setEnabled(False))
        bota_iniciar_conexao.clicked.connect(self.startconnection)
        self.GridLayout.addWidget(bota_iniciar_conexao,0,0)
      else:
        self.noCredentials() 
      
    def startconnection(self):      
      self.limpar()
      if self.model.hasToken(): 
          self.hasCredentials()   
      else: 
        self.noCredentials() 
        
    def hasCredentials(self):
      if self.model.setS3Client() == False:
        label_erro = QLabel("Erro de conexão ou credenciais inválidas.")
        def Reset():
          self.model.resetCredentials()
          self.limpar()
          self.noCredentials()
        botao_tentar_novamente = QPushButton("Tentar novamente")
        botao_tentar_novamente.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        botao_registrar_novas_credenciais = QPushButton("Registrar novas credenciais")
        botao_registrar_novas_credenciais.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        botao_tentar_novamente.clicked.connect(self.start)
        botao_registrar_novas_credenciais.clicked.connect(Reset)
        self.GridLayout.addWidget(label_erro,0,0)
        self.GridLayout.addWidget(botao_tentar_novamente,1,0)
        self.GridLayout.addWidget(botao_registrar_novas_credenciais,1,1)
        return
      
      label_h1 = QLabel("Upload Amazon S3")      

      label_local = QLabel("Selecione o diretório dentro do S3") 
      combo_local = QComboBox()
      combo_local.setCursor(QCursor(Qt.CursorShape.PointingHandCursor)) 
      combo_local.addItems(self.model.list_folders_s3(sort=True))
      
      campo_dir = QLineEdit()
      def setLocal():
        file_name = QFileDialog.getExistingDirectory(self, "Selecione uma pasta")
        campo_dir.setText(file_name)
      botao_buscar_dir = QPushButton("Buscar")
      botao_buscar_dir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
      botao_buscar_dir.clicked.connect(setLocal)
      
      def checkUploaded():
        if self.model.downloaded == True:
          self.setCursor(Qt.CursorShape.WaitCursor)
          botao_upload.setText("Realizar upload")
          botao_upload.setEnabled(True)
          return
        QTimer.singleShot(2000,checkUploaded)
        #Main.InterfaceMain.root.after(2000, checkUploaded) 
      def upload():
        if campo_dir.text() == "":
          QMessageBox.information(None,"Aviso","Arquivo para upload não fornecido.")
          return
        if combo_local.currentText() == "":
          QMessageBox.information(None,"Aviso","Pasta de destino não especificada")
          return
        checkUploaded()
        self.setCursor(Qt.CursorShape.ArrowCursor)
        botao_upload.setText("Realizando upload...")
        botao_upload.setEnabled(False)
        self.model.start(local_folder_path=campo_dir.text(), destination_folder=combo_local.currentText())
      
      botao_upload = QPushButton("Realizar upload")  
      botao_upload.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  
      botao_upload.clicked.connect(upload)
      
      self.GridLayout.addWidget(label_h1,0,0)
      self.GridLayout.addWidget(label_local,1,0)
      self.GridLayout.addWidget(combo_local,1,1)
      self.GridLayout.addWidget(campo_dir,2,0)
      self.GridLayout.addWidget(botao_buscar_dir,2,1)
      self.GridLayout.addWidget(botao_upload,3,0,1,1)
        
    def noCredentials(self):
      label_h1 = QLabel("Você não possui credenciais associadas ao AluraVideos!\n Por favor as associe agora.")
      label_access_key = QLabel("Access Key:")
      campo_access_key = QLineEdit()
      label_secret_key = QLabel("Secret Key:")
      campo_secret_key = QLineEdit()
      
      def register():
        secret_key = campo_secret_key.text()
        access_key = campo_access_key.text()
        if self.model.registerCredentials(secret_key=secret_key,access_key=access_key):
            self.limpar()
            self.hasCredentials()
      botaoRegistrar = QPushButton("Registrar")
      botaoRegistrar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  
      botaoRegistrar.clicked.connect(register)
      
      self.GridLayout.addWidget(label_h1,0,0)
      self.GridLayout.addWidget(label_access_key,1,0)
      self.GridLayout.addWidget(campo_access_key,2,0)
      self.GridLayout.addWidget(label_secret_key,3,0)
      self.GridLayout.addWidget(campo_secret_key,4,0)
      self.GridLayout.addWidget(botaoRegistrar,5,0)
         
    def limpar(self):
        for i in reversed(range(self.GridLayout.count())):  # Usa range reverso para evitar problemas ao remover
          item = self.GridLayout.itemAt(i)  # Obtém o item na posição i
          if item is not None:
              widget = item.widget()  # Obtém o widget associado ao item
              if widget is not None:
                  widget.deleteLater()  # Envia o widget para ser excluído
              self.GridLayout.removeItem(item)  # Remove o item do layout