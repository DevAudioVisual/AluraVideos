import os
from tkinter import filedialog
from PyQt6.QtGui import QCursor,QStandardItemModel,QIcon
from PyQt6.QtCore import Qt,QTimer,QSortFilterProxyModel
from Interfaces.S3 import S3DialogFilaUploader
import Util.CustomWidgets as cw
from Models.S3 import S3Model
from Interfaces.S3.S3TreeItem import S3TreeItem
from Interfaces.S3.S3TreeView import S3TreeView

class Interface(cw.Widget):
    def __init__(self):
        super().__init__()
        
        self.model = S3Model.S3Model()
        self.GridLayout = cw.GridLayout()
        self.GridLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.GridLayout.setContentsMargins(10, 20, 10, 10)
        QTimer.singleShot(0, self.start)
        self.setLayout(self.GridLayout)
        
    def start(self):
        self.limpar()    
        if self.model.hasToken(): 
            self.startconnection()
        else:
            self.noCredentials() 
      
    def startconnection(self):      
        if self.model.hasToken(): 
            self.limpar()
            self.hasCredentials()   
        else: 
            self.noCredentials() 
        
    def hasCredentials(self):
      if self.model.setS3Client() == False:
        label_erro = cw.Label("Erro de conexão ou credenciais inválidas.")
        def Reset():
          self.model.resetCredentials()
          self.limpar()
          self.noCredentials()
        botao_tentar_novamente = cw.PushButton("Tentar novamente")
        botao_tentar_novamente.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        botao_registrar_novas_credenciais = cw.PushButton("Registrar novas credenciais")
        botao_registrar_novas_credenciais.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        botao_tentar_novamente.clicked.connect(self.start)
        botao_registrar_novas_credenciais.clicked.connect(Reset)
        self.GridLayout.addWidget(label_erro,0,0)
        self.GridLayout.addWidget(botao_tentar_novamente,1,0)
        self.GridLayout.addWidget(botao_registrar_novas_credenciais,1,1)
        return
      
      label_h1 = cw.Label("Amazon S3")    
      label_h1.setObjectName("grande")  
      
      def checkUploaded():
        if self.model.downloaded == True:
          return
        QTimer.singleShot(2000,checkUploaded)
      
      self.Standardmodel = QStandardItemModel()
      self.Standardmodel.setHorizontalHeaderLabels(['equipevideos Bucket'])
      
      self.proxy_model = MyFilterProxyModel()
      self.proxy_model.setSourceModel(self.Standardmodel)
      self.proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
      self.proxy_model.setFilterKeyColumn(-1)  # Filtrar em todas as colunas
      self.proxy_model.setFilterRegularExpression("") 

      self.search_input = cw.LineEdit()
      self.search_input.setPlaceholderText("Buscar")
      self.search_input.textChanged.connect(self.proxy_model.setFilterRegularExpression)
      search_input_action = self.search_input.addAction(QIcon(r"Assets\Icons\reload.ico"), cw.LineEdit.ActionPosition.TrailingPosition)
      search_input_action.setToolTip("Recarregar arvore de arquivos")
      search_input_action.triggered.connect(self.refresh_tree)
      
      self.tree_view = S3TreeView(self.model,self.proxy_model,self.Standardmodel)
      self.tree_view.header().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
      self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
      self.tree_view.customContextMenuRequested.connect(self.create_context_menu)  # Conecta o menu ao clique direito
      
      layout = cw.VBoxLayout()
      layout.addWidget(label_h1)
      layout.addWidget(self.search_input)
      layout.addWidget(self.tree_view)
      
      self.load_root()

      # Conectar o evento de expansão de itens
      self.tree_view.expanded.connect(self.on_item_expanded)
      self.GridLayout.addLayout(layout,1,0,1,1)
        
    def noCredentials(self):
      label_h1 = cw.Label("Você não possui credenciais associadas ao AluraVideos.\nPor favor as associe agora.")
      label_h1.setObjectName("grande")
      label_h1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
      label_access_key = cw.Label("Access Key:")
      campo_access_key = cw.LineEdit()
      campo_access_key.setPlaceholderText("Digite a sua access key")
      campo_access_key.setClearButtonEnabled(True)
      campo_access_key.setEchoMode(cw.LineEdit.EchoMode.Password)
      action_access_key = campo_access_key.addAction(QIcon(r"Assets\svg\eye.svg"), cw.LineEdit.ActionPosition.TrailingPosition)
      def alterarOfuscarAccessKey():
        if campo_access_key.echoMode() == cw.LineEdit.EchoMode.Password:
            campo_access_key.setEchoMode(cw.LineEdit.EchoMode.Normal)
            action_access_key.setIcon(QIcon(r"Assets\svg\eye-off.svg"))  # Ícone de olho aberto
        else:
            campo_access_key.setEchoMode(cw.LineEdit.EchoMode.Password)
            action_access_key.setIcon(QIcon(r"Assets\svg\eye.svg")) 
      action_access_key.triggered.connect(alterarOfuscarAccessKey)
          
      label_secret_key = cw.Label("Secret Key:")
      campo_secret_key = cw.LineEdit()
      campo_secret_key.setPlaceholderText("Digite a sua secret key")
      campo_secret_key.setClearButtonEnabled(True)
      campo_secret_key.setEchoMode(cw.LineEdit.EchoMode.Password)
      action_secret_key = campo_secret_key.addAction(QIcon(r"Assets\svg\eye.svg"), cw.LineEdit.ActionPosition.TrailingPosition)
      def alterarOfuscarSecretKey():
        if campo_secret_key.echoMode() == cw.LineEdit.EchoMode.Password:
            campo_secret_key.setEchoMode(cw.LineEdit.EchoMode.Normal)
            action_secret_key.setIcon(QIcon(r"Assets\svg\eye-off.svg"))  # Ícone de olho aberto
        else:
            campo_secret_key.setEchoMode(cw.LineEdit.EchoMode.Password)
            action_secret_key.setIcon(QIcon(r"Assets\svg\eye.svg")) 
      action_secret_key.triggered.connect(alterarOfuscarSecretKey)
      
      
      
      def register():
        secret_key = campo_secret_key.text()
        access_key = campo_access_key.text()
        if self.model.registerCredentials(secret_key=secret_key,access_key=access_key):
            self.limpar()
            self.hasCredentials()
      botaoRegistrar = cw.PushButton("Registrar")
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

        source_index = self.proxy_model.mapToSource(index)
        item = self.Standardmodel.itemFromIndex(source_index)
        full_path = item.full_path  # Obtém o caminho completo do item

        # Abre um diálogo para escolher o diretório de salvamento
        save_path = filedialog.askdirectory()
        if save_path:
            if item.is_folder:  # Se for uma pasta
                self.model.startDownload(full_path, save_path, True)
            else:  # Se for um arquivo
                self.model.startDownload(full_path, save_path, False)



    def upload_item(self):
        #upload_path = filedialog.askdirectory()
        index = self.tree_view.currentIndex()
        #if not index.isValid() or not upload_path:
        #    return  # Verifica se um item válido foi selecionado

        source_index = self.proxy_model.mapToSource(index)
        item = self.Standardmodel.itemFromIndex(source_index)
        full_path = item.full_path  # Obtém o caminho completo do item
        S3DialogFilaUploader.DialogUpload(full_path).exec()
        #self.model.startUpload(local_folder_path=upload_path,destination_folder=full_path)

    def rename_item(self):
        index = self.tree_view.currentIndex()
        if not index.isValid():
            return  # Verifica se um item válido foi selecionado

        source_index = self.proxy_model.mapToSource(index)
        item = self.Standardmodel.itemFromIndex(source_index)
        old_key = item.full_path

        # Caixa de diálogo para inserir o novo nome
        new_name, ok = cw.InputDialog.getText(self, "Renomear Item", "Novo nome:", text=item.text())
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
            cw.MessageBox.critical(self, "Erro", f"Falha ao renomear o item: {e}")
            return

        cw.MessageBox.information(self, "Sucesso!", "Item renomeado com sucesso.")
        
        
    def delete_item(self):
        index = self.tree_view.currentIndex()
        if not index.isValid():
            return  # Verifica se um item válido foi selecionado

        source_index = self.proxy_model.mapToSource(index)
        item = self.Standardmodel.itemFromIndex(source_index)
        full_path = item.full_path 
        folder_name = os.path.basename(full_path)
        
        msg_box = cw.MessageBox()
        msg_box.setIcon(cw.MessageBox.Icon.Question)
        msg_box.setWindowTitle("Confirmação")
        msg_box.setText(f"Confirmar remoção do item:\n{full_path}")
        msg_box.setStandardButtons(cw.MessageBox.StandardButton.Yes | cw.MessageBox.StandardButton.No)
        msg_box.setDefaultButton(cw.MessageBox.StandardButton.Yes)
        ret = msg_box.exec()
        msg_box.activateWindow()
        msg_box.raise_()
        if ret == cw.MessageBox.StandardButton.Yes:
            try:
                # Exclui todos os objetos com o prefixo full_path
                objects_to_delete = []
                response = self.model.s3_client.list_objects_v2(Bucket=self.model.bucket_name, Prefix=full_path)
                for obj in response.get('Contents', []):
                    objects_to_delete.append({'Key': obj['Key']})

                # Exclui os objetos em lotes de 1000
                for i in range(0, len(objects_to_delete), 1000):
                    self.model.s3_client.delete_objects(Bucket=self.model.bucket_name, Delete={'Objects': objects_to_delete[i:i+1000]})

                # Remove a linha do tree_view
                self.tree_view.model().removeRow(index.row(), index.parent())

                cw.MessageBox().information(None, "Sucesso!", "Item excluío com sucesso.")

            except Exception as e:
                cw.MessageBox().critical(None, "Erro!", f"Erro ao excluir pasta: {e}")
    def create_context_menu(self, position):
        # Cria o menu de contexto
        menu = cw.Menu()

        # Ação de download
        download_action = menu.addAction("Download")
        download_action.triggered.connect(self.download_item)

        upload_action = menu.addAction("Upload")
        upload_action.triggered.connect(self.upload_item)
        
        upload_action = menu.addAction("Renomear")
        upload_action.triggered.connect(lambda: cw.MessageBox.information(self, "Aviso", "Em breve!"))
        menu.addSeparator()
        delete_action = menu.addAction("Excluir")
        delete_action.triggered.connect(self.delete_item)  # Conecte a um método para excluir

        # Exibe o menu no local do clique
        menu.exec(self.tree_view.viewport().mapToGlobal(position))
                    
    def refresh_tree(self):
      # Limpar o modelo existente
      self.Standardmodel.clear()  # Limpa todos os itens do modelo padrão
      self.Standardmodel.setHorizontalHeaderLabels(['equipevideos Bucket'])
      # Carregar os itens novamente
      self.load_root() 
      
    def load_root(self):
        self.tree_view.setModel(self.proxy_model)  
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
        # Mapeia o índice do proxy para o modelo subjacente
        source_index = self.proxy_model.mapToSource(index)
        item = self.Standardmodel.itemFromIndex(source_index)
        if isinstance(item, S3TreeItem) and item.is_folder:
            item.fetch_children()

                  
    def limpar(self):
        for i in reversed(range(self.GridLayout.count())):  # Usa range reverso para evitar problemas ao remover
          item = self.GridLayout.itemAt(i)  # Obtém o item na posição i
          if item is not None:
              widget = item.widget()  # Obtém o widget associado ao item
              if widget is not None:
                  widget.deleteLater()  # Envia o widget para ser excluído
              self.GridLayout.removeItem(item)  # Remove o item do layout
              
              
class MyFilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()

    def filterAcceptsRow(self, source_row, source_parent):
        index = self.sourceModel().index(source_row, 0, source_parent)
        item = self.sourceModel().itemFromIndex(index)

        # Verifique se o item é do tipo esperado (S3TreeItem)
        if isinstance(item, S3TreeItem):
            # Agora você pode acessar is_folder sem erro
            if item.is_folder:
                # Verifique se algum filho da pasta corresponde ao filtro
                for row in range(item.rowCount()):
                    child_item = item.child(row)
                    child_index = self.sourceModel().indexFromItem(child_item)  # Usar o model para acessar o índice do filho
                    if self.filterAcceptsRow(child_index.row(), child_index.parent()):
                        return True

        # Verifique o nome do item se for um arquivo (não pasta)
        return super().filterAcceptsRow(source_row, source_parent)


