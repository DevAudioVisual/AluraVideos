import json
import re
import threading
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QCheckBox, QFileDialog,QVBoxLayout,QGroupBox,QPushButton, QGridLayout, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QCursor, QAction
from Config import LoadConfigs
global Config

class Interface(QWidget):
    def __init__(self):
        super().__init__() 
        self.df = LoadConfigs.Config.getDataFrame("ConfigCriarProjeto")
        self.config = LoadConfigs.Config.getConfigData("ConfigCriarProjeto")
        
        self.setContentsMargins(10, 20, 10, 10)
        self.interface()
    def save(self):
        try:
            self.dict = {}
            self.dict["fechar_ao_criar"] = self.check_fechar_ao_criar.isChecked()
            self.dict["diretorio_padrao"] = self.campo_dir.text()
            self.dict["monitorar_area_transferencia"] = self.check_monitorar_area_transferencia.isChecked()
            self.dict["checks"] = [{
                "Abrir_Premiere": self.check_abrir_premiere.isChecked(),
                "Abrir_pasta_do_projeto": self.check_abrir_pasta_do_projeto.isChecked()
            }]
            self.dict["subpastas"] = [{
                "01_Bruto": self.subpasta_vars["01_Bruto"].isChecked(),
                "03_Assets": self.subpasta_vars["03_Assets"].isChecked(),
                "04_Premiere": self.subpasta_vars["04_Premiere"].isChecked(),
                "05_AfterEfects": self.subpasta_vars["05_AfterEfects"].isChecked(),
                "06_Photoshop-Illustrator": self.subpasta_vars["06_Photoshop-Illustrator"].isChecked(),
                "07_Render": self.subpasta_vars["07_Render"].isChecked()
            }]
            LoadConfigs.Config.saveConfigDict("ConfigCriarProjeto",self.dict)
            QMessageBox.information(None,"Aviso","Configurações salvas com sucesso!")
        except Exception as e:
            QMessageBox.information(None,"Aviso","Erro ao salvar as configurações!")
    def interface(self):
        self.titulo = QLabel("Preferencias Criar Projeto")
        self.titulo.setObjectName("grande")
        
        self.label_dir = QLabel("Diretório padrão:")
        self.campo_dir = QLineEdit()
        self.campo_dir.setText(self.config["diretorio_padrao"])
        self.campo_dir.setPlaceholderText("Diretório padrão onde o projeto será criado")
        self.campo_dir.setClearButtonEnabled(True)
        self.dir_action = self.campo_dir.addAction(QIcon(r"Assets\Images\folder.png"), QLineEdit.ActionPosition.TrailingPosition)
        
        self.tool_button = self.campo_dir.findChildren(QAction)[0] 
        self.tool_button.setToolTip("Buscar vídeos")
        
        self.dir_action.triggered.connect(self.open_folder_dialog)
        
        self.layout = QVBoxLayout()      
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        self.group_processos = QGroupBox("Processos")
        self.layout_processos = QGridLayout()
        
        checks_vars = {}
        checks = self.df['checks'].iloc[0].items()
        for ch, ci in checks:
            checks_vars[ch] = ci
        
        self.check_abrir_premiere = QCheckBox(text="Abrir Premiere")
        self.check_abrir_pasta_do_projeto = QCheckBox(text="Abrir pasta do projeto")
        self.check_abrir_pasta_do_projeto.setChecked(bool(checks_vars["Abrir_pasta_do_projeto"]))
        self.check_fechar_ao_criar = QCheckBox(text="Fechar ao criar")
        self.check_fechar_ao_criar.setChecked(bool(self.config["fechar_ao_criar"]))
        self.check_monitorar_area_transferencia = QCheckBox(text="Monitorar Área de transferência")
        self.check_monitorar_area_transferencia.setChecked(bool(self.config["monitorar_area_transferencia"]))
        self.check_monitorar_area_transferencia.setToolTip("Habilite para o AluraVideos monitora em segundo plano possiveis links do dropbox na área de transferência")
        
        self.layout_processos.addWidget(self.check_abrir_premiere,0,0)
        self.layout_processos.addWidget(self.check_abrir_pasta_do_projeto,0,1)
        self.layout_processos.addWidget(self.check_fechar_ao_criar,0,2)
        self.layout_processos.addWidget(self.check_monitorar_area_transferencia,0,3)
        self.group_processos.setLayout(self.layout_processos)
        
        self.group_sub_pastas = QGroupBox("Sub-pastas")
        self.layout_sub_pastas = QGridLayout()
        self.group_sub_pastas.setLayout(self.layout_sub_pastas)
        
        self.subpasta_vars = {}
        row = 0
        coluna_atual = 0
        
        for subpasta, criar in self.df['subpastas'].iloc[0].items():
            checkbox = QCheckBox(f"{subpasta}")
            checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.subpasta_vars[subpasta] = checkbox
            checkbox.setChecked(bool(criar))
            self.layout_sub_pastas.addWidget(checkbox,row,coluna_atual)
            row += 1
            if row == 3:
                row = 0
                coluna_atual += 1
        
        self.button_salvar = QPushButton(text="Salvar")
        self.button_salvar.clicked.connect(self.save)
        
        self.layout.addWidget(self.titulo)
        self.layout.addWidget(self.label_dir)
        self.layout.addWidget(self.campo_dir)
        self.layout.addWidget(self.group_processos)
        self.layout.addWidget(self.group_sub_pastas)
        self.layout.addWidget(self.button_salvar)
        
        self.setLayout(self.layout)
        
    def open_folder_dialog(self):
        file_name = QFileDialog.getExistingDirectory(self, "Selecione uma pasta")
        if file_name:
            print(f"Pasta selecionado: {file_name}")
            self.campo_dir.setText(rf"{file_name}")