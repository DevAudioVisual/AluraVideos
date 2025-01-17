import os
from Models.LimparCache.CleanerThread import CleanerThread
import Util.CustomWidgets as cw
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
from Config import LoadConfigs
global Config

class Interface(cw.Widget):
    def __init__(self):
        super().__init__()
        
        layout = cw.GridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.setContentsMargins(10, 20, 10, 10)
        
        label = cw.Label("Pastas para limpar:")
        layout.addWidget(label,0,0)
        
        self.checkbox_vars = []
        self.checkbox_dict = {}
        self.Pastas = LoadConfigs.Config.getDataFrame("ConfigCache")
        row = 1
        for key, criar in self.Pastas['Pastas'].iloc[0].items():
            row += 1
            check = cw.CheckBox(key)
            check.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            check.setChecked(bool(criar))
            check.clicked.connect(self.updateConfig)
            self.checkbox_vars.append(check)
            self.checkbox_dict[key] = check
            check.clicked.connect(self.update_selected_keys)
            layout.addWidget(check,row,0)
            
        row += 1
        self.progressBar = cw.ProgressBar(self)
        self.progressBar.setGeometry(20, 60, 160, 20)
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar,row,0)
        
        row += 1
        botaoLimpar = cw.PushButton("Limpar")   
        botaoLimpar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        botaoLimpar.clicked.connect(self.limpar_pastas)
        layout.addWidget(botaoLimpar,row,0)
        
        self.setLayout(layout)
        
    def updateConfig(self):
        config = LoadConfigs.Config.getConfigData("ConfigCache")
        
        pastas = {}
        for pasta, var in self.checkbox_dict.items():
            pastas[pasta] = var.isChecked()
        config["Pastas"] = [pastas]
                
        LoadConfigs.Config.saveConfigDict("ConfigCache",config)    
        
    def update_selected_keys(self):
        for checks in self.checkbox_vars:
          if checks.isChecked():
            print("Chaves selecionadas:", checks.text())      
        
    def update_progress(self, value):
      self.progressBar.setValue(value)
      
    def limpar_pastas(self):
        pastas_selecionadas = []
        for checks in self.checkbox_vars:
            if checks.isChecked():
                chave = checks.text()
                pastas_selecionadas.append(chave)
        
        pastas = []
        for p in pastas_selecionadas:
          if p == "Temp":
            pastas.append("C:\\Windows\\Temp")
          if p == "PorcentoTemp" or p == "%temp%":
            pastas.append(self.get_temp_dir())
          if p == "Prefetch":
            pastas.append("C:\\Windows\\Prefetch")
          if p == "Adobe Cache":
            pastas.append(LoadConfigs.Config.getConfigData("ConfigCache","Cache_Adobe"))
          if p == "Lixeira":
            pastas.append("Lixeira")

        self.thread = CleanerThread(pastas)
        self.thread.progress_updated.connect(self.update_progress)
        self.thread.finished.connect(self.limpeza_concluida)
        self.thread.start()
        
    def limpeza_concluida(self):
        cw.MessageBox.information(None, "Sucesso!", "Limpeza concluida com sucesso!")
        self.progressBar.setValue(0)
        print("Limpeza concluida")    
      
    def get_temp_dir(self):
      temp_dir = os.environ.get('TEMP') or os.environ.get('TMP')
      if temp_dir is None:
          raise FileNotFoundError("Diretório temporário não encontrado.")
      return temp_dir