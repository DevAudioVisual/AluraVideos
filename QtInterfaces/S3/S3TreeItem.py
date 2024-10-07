from PyQt6.QtGui import QIcon,QStandardItem

class S3TreeItem(QStandardItem):
    def __init__(self, name, is_folder, bucket_name, full_path, model):
        super().__init__(name)
        self.setEditable(False)
        self.is_folder = is_folder
        self.bucket_name = bucket_name
        self.model = model
        self.full_path = full_path
        self.fetched = False

        if self.is_folder:
            self.setEditable(False)
            # Adicionar um item filho "falso" para mostrar que ele pode ser expandido
            self.setIcon(QIcon(r"Assets\Images\folder.png"))
            self.appendRow(QStandardItem(''))  
        else:
            file_extension = self.full_path.split('.')[-1]
            self.setIcon(QIcon(rf"Assets\Icons\{file_extension}.ico"))  # Ícone específico para arquivos .prproj

    # Carregar o conteúdo da pasta quando ela for expandida
    def fetch_children(self):
        if self.fetched:
            return  # Se já buscamos os itens, não buscar novamente

        #print(f"Buscando subitens em {self.full_path} no bucket {self.bucket_name}")
        
        try:
            result = self.model.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=self.full_path, Delimiter='/')
            folders = result.get('CommonPrefixes', [])
            files = result.get('Contents', [])

            # Remover o item filho "falso"
            self.removeRows(0, self.rowCount())

            # Adicionar subpastas
            for folder in folders:
                folder_name = folder['Prefix'].split('/')[-2]  # Extrair o nome da subpasta
                folder_item = S3TreeItem(folder_name, True, self.bucket_name, folder['Prefix'], self.model)
                self.appendRow(folder_item)

            # Adicionar arquivos
            for file in files:
                if file['Key'] != self.full_path:  # Ignorar o próprio prefixo
                    file_name = file['Key'].split('/')[-1]
                    file_item = S3TreeItem(file_name, False, self.bucket_name, file['Key'], self.model)
                    self.appendRow(file_item)

            self.fetched = True  # Marcar como "fetch" realizado
        except Exception as e:
            print(f"Erro ao buscar subitens da pasta {self.full_path}: {e}")