import os
import Util.CustomWidgets as cw
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog
global Config

class FileSelector(cw.Widget):
    def __init__(self):
        super().__init__()
        
        self.main_layout = cw.VBoxLayout()
        
        self.select_button = cw.PushButton("Selecionar Arquivos")
        self.select_button.clicked.connect(self.select_files)
        self.main_layout.addWidget(self.select_button)
        
        self.clear_button = cw.PushButton("Limpar")
        self.clear_button.clicked.connect(self.clear)
        self.main_layout.addWidget(self.clear_button)

        self.file_list = cw.ListWidget()
        self.main_layout.addWidget(self.file_list)

        self.count_label = cw.Label("Arquivos selecionados: 0")
        self.main_layout.addWidget(self.count_label)
        
        self.setLayout(self.main_layout)
    def clear(self):
        self.file_list.clear()
        self.update_count_label()
    def select_files(self):
        """Abre uma janela de diálogo para selecionar arquivos de vídeo 
        e adiciona os arquivos selecionados à lista."""
        file_names, _ = QFileDialog.getOpenFileNames(
            self, 
            "Selecionar Arquivos de Vídeo", 
            os.getcwd(), 
            "Arquivos de Vídeo (*.mp4 *.avi *.mov *.mkv);;Todos os Arquivos (*)"
        )
        for file_name in file_names:
            self.file_list.addItem(file_name)
        self.update_count_label()

    def update_count_label(self):
        """Atualiza o rótulo com o número de arquivos selecionados."""
        count = self.file_list.count()
        self.count_label.setText(f"Arquivos selecionados: {count}")

    def get_selected_files(self):
        """Retorna uma lista com os caminhos dos arquivos selecionados, ordenados alfabeticamente."""
        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        return sorted(files)