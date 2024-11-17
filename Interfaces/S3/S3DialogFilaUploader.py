import os
import sys
from tkinter import filedialog
from PyQt6.QtCore import Qt
from Models.S3 import S3Model
import Util.CustomWidgets as cw

class Botao(cw.PushButton):
    def __init__(self):
        super().__init__()

        #self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAnimacao(False)
        self.setText('\n\n Busque ou arraste pastas para upload \n\n')
        self.setSizePolicy(cw.SizePolicy.Policy.Expanding,cw.SizePolicy.Policy.Expanding)
        self.setStyleSheet('''
            QPushButton{
                border: 4px dashed #aaa
            }
        ''')

class ItemWidget(cw.Widget):
    def __init__(self, nome):
        super().__init__()
        self.nome = nome
        layout = cw.HBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.label = cw.Label(nome)
        self.botao_excluir = cw.PushButton("Remover")
        self.botao_excluir.setSizePolicy(cw.SizePolicy.Policy.Fixed, cw.SizePolicy.Policy.Fixed)
        layout.addWidget(self.label)
        layout.addWidget(self.botao_excluir)
        self.setLayout(layout)


    def nome(self):
        return self.nome

    def conectar_botao_excluir(self, slot):
        self.botao_excluir.clicked.connect(slot)

class DialogUpload(cw.Dialog):
    def __init__(self, pathParaUpload):
        super().__init__()
        self.resize(400, 400)
        self.setAcceptDrops(True)
        
        self.pathParaUpload = pathParaUpload
        self.model = S3Model.S3Model()

        mainLayout = cw.VBoxLayout()
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        lbl_h1 = cw.Label(f"Upload para: <br><font face='Helvetica' size='10px' style='font-weight: normal;'>{self.pathParaUpload}</font>")
        lbl_h1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_h1.setObjectName("grande")

        self.botaoBuscar = Botao()
        self.botaoBuscar.clicked.connect(self.busca)
        
        mainLayout.addWidget(lbl_h1)
        mainLayout.addWidget(self.botaoBuscar)

        self.layout_itens = cw.VBoxLayout()
        self.layout_itens.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        mainLayout.addLayout(self.layout_itens)
        
        bttn_upload = cw.PushButton("Iniciar Upload")
        bttn_upload.clicked.connect(self.startUpload)
        mainLayout.addWidget(bttn_upload)

        self.setLayout(mainLayout)
        
        self.fila_Upload = []
    def startUpload(self):
        if self.fila_Upload:
            self.model.startUpload(local_folder_path=self.fila_Upload,destination_folder=self.pathParaUpload)
            self.destroy()
    def busca(self):
        dir = filedialog.askdirectory()
        if dir:
            self.adicionar_item(dir)
            
    def adicionar_item(self, nome):
        item_widget = ItemWidget(nome)
        item_widget.conectar_botao_excluir(lambda: self.excluir_item(item_widget))
        self.layout_itens.addWidget(item_widget)
        self.layout_itens.update()  # Atualiza o layout após adicionar o item
        self.fila_Upload.append(nome)
        print(self.fila_Upload)

    def excluir_item(self, item_widget):
        for i in range(self.layout_itens.count()):
            if self.layout_itens.itemAt(i).widget() == item_widget:
                self.fila_Upload.remove(item_widget.nome)
                self.layout_itens.takeAt(i).widget().deleteLater()
                break
        print(self.fila_Upload)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if os.path.isdir(file_path):  # Verifica se é um diretório
                    self.adicionar_item(file_path)
            event.accept()
        else:
            event.ignore()
    