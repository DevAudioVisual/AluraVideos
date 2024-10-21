from PyQt6.QtWidgets import QTreeView, QAbstractItemView
import os



class S3TreeView(QTreeView):
    def __init__(self, model):
        super().__init__()
        self.s3_model = model
        self.setAcceptDrops(True)
        #self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    """
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():  # Verifica se os itens arrastados são arquivos
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        # Pegando o item sobre o qual os arquivos foram soltos
        index = self.indexAt(event.position().toPoint())
        if not index.isValid():
            return
        
        # Pegando o diretório S3 no qual os arquivos serão soltos
        item = self.model().itemFromIndex(index)
        s3_folder_key = item.full_path  # Atribua o caminho correto da pasta no S3

        # Pegando os arquivos soltos
        urls = event.mimeData().urls()
        local_paths = [url.toLocalFile() for url in urls]
        if len(local_paths) > 1:
          QMessageBox.information(None,"Aviso","É permitido subir apenas uma pasta por vez.")
          return

        # Fazer upload de cada arquivo/pasta solto
        for local_path in local_paths:
            if os.path.isdir(local_path):
                resposta = QMessageBox.question(None, "Confirme o upload", f"Deseja realizar o upload?\n\nOrigem: {local_path}\nDestido: {s3_folder_key}", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if resposta == QMessageBox.StandardButton.Yes:
                  self.s3_model.startUpload(local_folder_path=local_path,destination_folder=s3_folder_key)
                  #print(local_path, s3_folder_key)
            else:
                QMessageBox.information(None,"Aviso","Apenas pastas são permitidas")
"""