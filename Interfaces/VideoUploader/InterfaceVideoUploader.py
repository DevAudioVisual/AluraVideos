import os
import sys
import webbrowser
from Config import LoadConfigs
from Interfaces.VideoUploader import UploadingTable
from Models.VideoUploader import CreateShowCase, GetShowcase
import Util.CustomWidgets as cw
from PyQt6.QtCore import Qt, QCoreApplication, QProcess
from PyQt6.QtWidgets import QFileDialog
global Config

class Interface(cw.Widget):
    def __init__(self):
        super().__init__()
        
        self.main_layout = cw.VBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        if LoadConfigs.Config.getConfigData(config="Credentials",data="VideoUploaderToken") == "" or not GetShowcase.get_showcases("teste"):
          self.lbl_registrar = cw.Label("<font color='red'>Você não tem um token valido! Por favor, registre agora.</font>")
          self.lbl_registrar.setObjectName("grande")
          self.lbl_registrar.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
          self.main_layout.addWidget(self.lbl_registrar)
          
          self.campo_token = cw.LineEdit()
          self.main_layout.addWidget(self.campo_token)
          
          self.btn_gerar_token = cw.PushButton("Gerar Token")
          self.btn_gerar_token.clicked.connect(lambda: webbrowser.open("https://video-uploader.alura.com.br/token/list"))
          self.main_layout.addWidget(self.btn_gerar_token)
          
          self.btn_registrar = cw.PushButton("Registrar")
          self.btn_registrar.clicked.connect(self.registrarToken)
          self.main_layout.addWidget(self.btn_registrar)   
        else:
          self.lbl_showcase_name = cw.Label("Nome do Showcase:")
          self.main_layout.addWidget(self.lbl_showcase_name)
          
          self.campo_showcase_name = cw.LineEdit()
          self.main_layout.addWidget(self.campo_showcase_name)
          
        
          self.file_selector = cw.PushButton("Selecionar arquivos")
          self.file_selector.clicked.connect(self.select_files)
          self.main_layout.addWidget(self.file_selector)
          
          self.uploading_table = UploadingTable.UploadTable()
          self.main_layout.addWidget(self.uploading_table,stretch=2)
          
          self.lbl_upload_paralelo = cw.Label("Uploads simultâneos:")
          self.main_layout.addWidget(self.lbl_upload_paralelo)
          self.spin_upload_paralelo = cw.SpinBox()
          self.spin_upload_paralelo.setValue(3)
          self.main_layout.addWidget(self.spin_upload_paralelo)
          
          self.upload_btn = cw.PushButton("Upload")
          self.upload_btn.clicked.connect(self.upload)
          self.main_layout.addWidget(self.upload_btn)
        
        self.setLayout(self.main_layout)
        
        self.showcase_id = None
    def select_files(self):
        file_names, _ = QFileDialog.getOpenFileNames(
            self, 
            "Selecionar Arquivos de Vídeo", 
            os.getcwd(), 
            "Arquivos de Vídeo (*.mp4 *.avi *.mov *.mkv);;Todos os Arquivos (*)"
        )
        for file_name in file_names:
            self.uploading_table.files.append(file_name)
            self.uploading_table.add_video(file_name)
        
    def upload(self):
      if self.campo_showcase_name.text() == "":
        print("Nome do showcase não pode ser vazio.")
        return
      if not self.uploading_table.files:
        print("Nenhum arquivo selecionado.")
        return
      self.upload_btn.setEnabled(False)
      self.upload_btn.setText("Uploading...")
      self.verifyShowcase()
      
      print(f"Iniciando upload na showcase_id: {self.showcase_id}")
      self.uploading_table.upload_videos(self.showcase_id, self.spin_upload_paralelo.value())

    def verifyShowcase(self):
      showcase = GetShowcase.get_showcases(self.campo_showcase_name.text())
      if showcase:
        self.showcase_id = showcase[0]["id"]
        print(self.showcase_id)
      else:
        self.createShowcase()
      
    def createShowcase(self):
      response = CreateShowCase.create_showcase(self.campo_showcase_name.text())

      if response.status_code == 200:
        print("Showcase criada com sucesso!\n",response.json())
      else:
        print(f"Erro ao criar a showcase: {response.status_code}")
        print(response.text)
        
    def registrarToken(self):
      data = LoadConfigs.Config.getConfigData(config="Credentials") 
      data['VideoUploaderToken'] = self.campo_token.text()
      LoadConfigs.Config.saveConfigDict("Credentials",data)
      
      QCoreApplication.quit()
      QProcess.startDetached(sys.executable, sys.argv)  