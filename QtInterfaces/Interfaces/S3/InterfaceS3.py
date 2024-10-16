import os
from PyQt6.QtGui import QCursor,QStandardItemModel,QIcon
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton,QFileDialog,QInputDialog, QMessageBox,QVBoxLayout,QMenu
from PyQt6.QtCore import Qt,QTimer
from Models.S3 import S3Model
from QtInterfaces.Interfaces.S3.S3TreeItem import S3TreeItem
from QtInterfaces.Interfaces.S3.S3TreeView import S3TreeView


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
      
      label_h1 = QLabel("Amazon S3")    
      label_h1.setObjectName("grande")  
      
      def checkUploaded():
        if self.model.downloaded == True:
          return
        QTimer.singleShot(2000,checkUploaded)
      
      self.search_input = QLineEdit()
      self.search_input.setPlaceholderText("Buscar pastas ou itens... (EM BREVE)")
      search_input_action = self.search_input.addAction(QIcon(r"Assets\Icons\reload.ico"), QLineEdit.ActionPosition.TrailingPosition)
      search_input_action.triggered.connect(self.refresh_tree)
      #self.search_input.textChanged.connect(self.filter_tree)
      
      self.Standardmodel = QStandardItemModel()
      self.Standardmodel.setHorizontalHeaderLabels(['equipevideos Bucket'])
      self.tree_view = S3TreeView(self.model)
      self.tree_view.setModel(self.Standardmodel)
      self.tree_view.header().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
      self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
      self.tree_view.customContextMenuRequested.connect(self.create_context_menu)  # Conecta o menu ao clique direito
      
      layout = QVBoxLayout()
      layout.addWidget(label_h1)
      layout.addWidget(self.search_input)
      layout.addWidget(self.tree_view)
      
      self.load_root()

      # Conectar o evento de expansão de itens
      self.tree_view.expanded.connect(self.on_item_expanded)
      self.GridLayout.addLayout(layout,1,0,1,1)
        
    def noCredentials(self):
      label_h1 = QLabel("Você não possui credenciais associadas ao AluraVideos.\nPor favor as associe agora.")
      label_h1.setObjectName("grande")
      label_h1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
      label_access_key = QLabel("Access Key:")
      campo_access_key = QLineEdit()
      campo_access_key.setPlaceholderText("Digite a sua access key")
      campo_access_key.setClearButtonEnabled(True)
      campo_access_key.setEchoMode(QLineEdit.EchoMode.Password)
      action_access_key = campo_access_key.addAction(QIcon(r"Assets\Icons\eye_on.ico"), QLineEdit.ActionPosition.TrailingPosition)
      def alterarOfuscarAccessKey():
        if campo_access_key.echoMode() == QLineEdit.EchoMode.Password:
            campo_access_key.setEchoMode(QLineEdit.EchoMode.Normal)
            action_access_key.setIcon(QIcon(r"Assets\Icons\eye_off.ico"))  # Ícone de olho aberto
        else:
            campo_access_key.setEchoMode(QLineEdit.EchoMode.Password)
            action_access_key.setIcon(QIcon(r"Assets\Icons\eye_on.ico")) 
      action_access_key.triggered.connect(alterarOfuscarAccessKey)
          
      label_secret_key = QLabel("Secret Key:")
      campo_secret_key = QLineEdit()
      campo_secret_key.setPlaceholderText("Digite a sua secret key")
      campo_secret_key.setClearButtonEnabled(True)
      campo_secret_key.setEchoMode(QLineEdit.EchoMode.Password)
      action_secret_key = campo_secret_key.addAction(QIcon(r"Assets\Icons\eye_on.ico"), QLineEdit.ActionPosition.TrailingPosition)
      def alterarOfuscarSecretKey():
        if campo_secret_key.echoMode() == QLineEdit.EchoMode.Password:
            campo_secret_key.setEchoMode(QLineEdit.EchoMode.Normal)
            action_secret_key.setIcon(QIcon(r"Assets\Icons\eye_off.ico"))  # Ícone de olho aberto
        else:
            campo_secret_key.setEchoMode(QLineEdit.EchoMode.Password)
            action_secret_key.setIcon(QIcon(r"Assets\Icons\eye_on.ico")) 
      action_secret_key.triggered.connect(alterarOfuscarSecretKey)
      
      
      
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
      
    def download_item(self):
        index = self.tree_view.currentIndex()
        if not index.isValid():
            return  # Verifica se um item válido foi selecionado

        item = self.Standardmodel.itemFromIndex(index)
        full_path = item.full_path  # Obtém o caminho completo do item

        # Abre um diálogo para escolher o diretório de salvamento
        save_path = QFileDialog.getExistingDirectory(self, "Escolha o diretório para salvar")
        if save_path:
            if item.is_folder:  # Se for uma pasta
                self.model.startDownload(full_path, save_path, True)
            else:  # Se for um arquivo
                self.model.startDownload(full_path, save_path, False)



    def upload_item(self):
        upload_path = QFileDialog.getExistingDirectory(self, "Escolha o diretório para subir")
        index = self.tree_view.currentIndex()
        if not index.isValid():
            return  # Verifica se um item válido foi selecionado

        item = self.Standardmodel.itemFromIndex(index)
        full_path = item.full_path  # Obtém o caminho completo do item
        self.model.startUpload(local_folder_path=upload_path,destination_folder=full_path)

    def rename_item(self):
        index = self.tree_view.currentIndex()
        if not index.isValid():
            return  # Verifica se um item válido foi selecionado

        item = self.Standardmodel.itemFromIndex(index)
        old_key = item.full_path

        # Caixa de diálogo para inserir o novo nome
        new_name, ok = QInputDialog.getText(self, "Renomear Item", "Novo nome:", text=item.text())
        if not ok:
            return  # Cancelado pelo usuário

        old_path = os.path.dirname(old_key)
        old_path = os.path.normpath(old_path)
        new_key = os.path.join(old_path, new_name)
        new_key = os.path.normpath(new_key)

        try:
            self.model.s3_client.copy_object(
                Bucket=self.model.bucket_name,
                CopySource={'Bucket': self.model.bucket_name, 'Key': old_key},
                Key=new_key
            )
            self.model.s3_client.delete_object(Bucket=self.model.bucket_name, Key=old_key)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao renomear o item: {e}")
            return

        QMessageBox.information(self, "Sucesso!", "Item renomeado com sucesso.")
        
        
    def delete_item(self):
        index = self.tree_view.currentIndex()
        if not index.isValid():
            return  # Verifica se um item válido foi selecionado

        item = self.Standardmodel.itemFromIndex(index)
        full_path = item.full_path 
        folder_name = os.path.basename(full_path)
        
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle("Confirmação")
        msg_box.setText(f"Confirmar remoção da pasta:\n{folder_name}")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Yes)
        ret = msg_box.exec()
        msg_box.activateWindow()
        msg_box.raise_()
        if ret == QMessageBox.StandardButton.Yes:
            print(full_path)
            #self.model.s3_client.delete_object(Bucket=self.model.bucket_name, Key=full_path)
            self.tree_view.model().removeRow(index.row(), index.parent())  
            QMessageBox().information(None,"Sucesso!","Arquivo excluido com exito.")
        
    def create_context_menu(self, position):
        # Cria o menu de contexto
        menu = QMenu()

        # Ação de download
        download_action = menu.addAction("Download")
        download_action.triggered.connect(self.download_item)

        upload_action = menu.addAction("Upload")
        upload_action.triggered.connect(self.upload_item)
        #upload_action = menu.addAction("Renomear")
        #upload_action.triggered.connect(self.rename_item)
        #delete_action = menu.addAction("Excluir")
        #delete_action.triggered.connect(self.delete_item)  # Conecte a um método para excluir

        # Exibe o menu no local do clique
        menu.exec(self.tree_view.viewport().mapToGlobal(position))
        
    def filter_tree(self, text):
    # Percorre todos os itens na árvore e filtra com base na entrada
        for i in range(self.Standardmodel.rowCount()):
            item = self.Standardmodel.item(i)
            self.filter_item(item, text)

    def filter_item(self, item, text):
        # Verifica se o item deve ser exibido com base na pesquisa
        item.setVisible(False)  # Esconde o item inicialmente
        if text.lower() in item.text().lower():  # Verifica se o texto está no nome do item
            item.setVisible(True)  # Exibe o item se houver correspondência
        elif item.hasChildren():  # Se o item tiver filhos, verifica recursivamente
            for row in range(item.rowCount()):
                child = item.child(row)
                self.filter_item(child, text)
                if child.isVisible():  # Se algum filho for visível, mostra o pai
                    item.setVisible(True)
                    
    def refresh_tree(self):
      # Limpar o modelo existente
      self.Standardmodel.clear()  # Limpa todos os itens do modelo padrão
      self.Standardmodel.setHorizontalHeaderLabels(['equipevideos Bucket'])
      # Carregar os itens novamente
      self.load_root() 
      
    def load_root(self):
        #print("Carregando pastas e arquivos do bucket...")  # Adicionando log para verificar o carregamento
        # Carregar a raiz do bucket
        root_item = self.Standardmodel.invisibleRootItem()
        self.Standardmodel.removeRows(0, self.Standardmodel.rowCount())
        result = self.model.s3_client.list_objects_v2(Bucket=self.model.bucket_name, Delimiter='/')

        folders = result.get('CommonPrefixes', [])
        files = result.get('Contents', [])

        #print(f"Pastas encontradas: {folders}")  # Verificando se pastas estão sendo retornadas
        #print(f"Arquivos encontrados: {files}")  # Verificando se arquivos estão sendo retornados

        # Adicionar as pastas na raiz em ordem alfabética
        folders_sorted = sorted(folders, key=lambda f: f['Prefix'])
        for folder in folders_sorted:
            folder_name = folder['Prefix'].split('/')[-2]  # Extrair o nome da pasta
            #print(f"Adicionando pasta: {folder_name}")
            folder_item = S3TreeItem(folder_name, True, self.model.bucket_name, folder['Prefix'], self.model)
            root_item.appendRow(folder_item)

        # Adicionar arquivos na raiz em ordem alfabética
        files_sorted = sorted(files, key=lambda f: f['Key'])
        for file in files_sorted:
            file_name = file['Key'].split('/')[-1]  # Extrair o nome do arquivo
            #print(f"Adicionando arquivo: {file_name}")
            file_item = S3TreeItem(file_name, False, self.model.bucket_name, file['Key'], self.model)
            root_item.appendRow(file_item)




    # Evento chamado quando uma pasta é expandida
    # No on_item_expanded
    def on_item_expanded(self, index):
        item = self.Standardmodel.itemFromIndex(index)
        if isinstance(item, S3TreeItem) and item.is_folder:
            item.fetch_children()  # Carrega os filhos apenas quando a pasta é expandida

                  
    def limpar(self):
        for i in reversed(range(self.GridLayout.count())):  # Usa range reverso para evitar problemas ao remover
          item = self.GridLayout.itemAt(i)  # Obtém o item na posição i
          if item is not None:
              widget = item.widget()  # Obtém o widget associado ao item
              if widget is not None:
                  widget.deleteLater()  # Envia o widget para ser excluído
              self.GridLayout.removeItem(item)  # Remove o item do layout