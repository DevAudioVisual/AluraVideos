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
            self.setIcon(QIcon(r"Assets\svg\folder.svg"))
            self.appendRow(QStandardItem(''))  
        else:
            file_extension = self.full_path.split('.')[-1]
            self.setIcon(QIcon(rf"Assets\Icons\{file_extension}.ico"))  # Ícone específico para arquivos .prproj

    # Carregar o conteúdo da pasta quando ela for expandida
    def fetch_children(self):
        if self.fetched:
            return

        try:
            paginator = self.model.s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(Bucket=self.bucket_name, Prefix=self.full_path, Delimiter='/')
            
            # Remover o item filho "falso"
            self.removeRows(0, self.rowCount())

            # Iterar por todas as páginas do paginator
            for page in page_iterator:
                folders = page.get('CommonPrefixes', [])
                files = page.get('Contents', [])

                # Adicionar subpastas
                for folder in folders:
                    folder_name = folder['Prefix'].split('/')[-2]
                    folder_item = S3TreeItem(folder_name, True, self.bucket_name, folder['Prefix'], self.model)
                    self.appendRow(folder_item)

                # Adicionar arquivos
                for file in files:
                    if file['Key'] != self.full_path:
                        file_name = file['Key'].split('/')[-1]
                        file_item = S3TreeItem(file_name, False, self.bucket_name, file['Key'], self.model)
                        self.appendRow(file_item)

            # Se passou por todas as páginas com sucesso, marque como "fetched"
            self.fetched = True

        except Exception as e:
            print(f"Erro ao buscar subitens da pasta {self.full_path}: {e}")

