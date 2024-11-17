import os
from PyQt6.QtWidgets import QTreeView, QAbstractItemView, QMessageBox

from Interfaces.S3 import S3DialogFilaUploader


class S3TreeView(QTreeView):
    def __init__(self, model,proxy_model,Standardmodel):
        super().__init__()
        self.s3_model = model
        self.proxy_model = proxy_model
        self.Standardmodel = Standardmodel
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():  # Verifica se os itens arrastados são arquivos
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()
        index = self.indexAt(event.position().toPoint())  # Use position().toPoint() aqui
        if index.isValid():
            self.setCurrentIndex(index)  # Seleciona o item

    def dropEvent(self, event):
        # Pegando o índice onde o item foi solto
        index = self.indexAt(event.position().toPoint())
        
        # Verifique se o índice é válido
        if not index.isValid():
            return
        
        source_index = self.proxy_model.mapToSource(index)
        item = self.Standardmodel.itemFromIndex(source_index)
        
        if item is None:
            print("Erro: Nenhum item encontrado para o índice.")
            return

        # Agora você pode acessar o caminho do item
        try:
            s3_folder_key = item.full_path  # Ou qualquer atributo que armazene o caminho
            print(f'Item dropado no caminho: {s3_folder_key}')
        except AttributeError:
            print("Erro: O item não possui o atributo 'full_path'. Verifique a estrutura dos itens.")
            return

        # Pegando os arquivos soltos
        urls = event.mimeData().urls()
        local_paths = [url.toLocalFile() for url in urls]

        dialog = S3DialogFilaUploader.DialogUpload(s3_folder_key)
        # Fazer upload de cada arquivo/pasta solto
        for local_path in local_paths:
            if os.path.isdir(local_path):
                dialog.adicionar_item(local_path)
                #self.s3_model.startUpload(local_folder_path=local_path,destination_folder=s3_folder_key)
                #print(local_path, s3_folder_key)
            else:
                QMessageBox.information(None, "Aviso", "Apenas pastas são permitidas")
        dialog.exec()
