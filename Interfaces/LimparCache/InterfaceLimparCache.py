import ctypes
import os
import shutil
import stat
import Util.CustomWidgets as cw
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt,QThread, pyqtSignal
from Config import LoadConfigs
global Config

class CleanerThread(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, pastas_selecionadas):
        super().__init__()
        self.pastas_selecionadas = pastas_selecionadas

    def run(self):
      total_arquivos = 0  # Contador de arquivos
      for pasta in self.pastas_selecionadas:
          if pasta != "Lixeira":  # Ignorar a Lixeira para contagem de arquivos
              for _, _, files in os.walk(pasta):
                  total_arquivos += len(files)

      arquivos_processados = 0  # Contador de arquivos processados

      for pasta in self.pastas_selecionadas:
          if pasta == "Lixeira":
              self.esvaziar_lixeira()
          else:
              if not os.path.exists(pasta):
                  print(f"A pasta {pasta} não existe")
              else:
                  for root, dirs, files in os.walk(pasta):
                      for file in files:
                          file_path = os.path.join(root, file)
                          try:
                                os.chmod(file_path, stat.S_IWRITE)  
                                if os.path.isfile(file_path):
                                    # Ignora permissões do arquivo e o remove
                                    os.remove(file_path)
                                elif os.path.isdir(file_path):
                                    # Remove a pasta e seu conteúdo recursivamente, ignorando erros
                                    shutil.rmtree(file_path, ignore_errors=True)  
                          except PermissionError:
                              print(f"Erro de permissão ao remover {file_path}. Pulando para o próximo arquivo.")
                          except Exception as e:
                              print(f"Erro ao remover {file_path}: {e}")

                          arquivos_processados += 1
                          progresso = int((arquivos_processados / total_arquivos) * 100)
                          self.progress_updated.emit(progresso)

                      for dir in dirs:
                        dir_path = os.path.join(root, dir)
                        try:
                            os.rmdir(dir_path)
                        except OSError:
                            pass

      self.finished.emit()
    def esvaziar_lixeira(self):
        SHERB_NOCONFIRMATION = 0x00000001
        SHERB_NOPROGRESSUI = 0x00000002
        SHERB_NOSOUND = 0x00000004
        flags = SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI | SHERB_NOSOUND

        # Obter o caminho da Lixeira
        caminho_lixeira = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Microsoft\Windows\Explorer\desktop.ini')

        # Chamar a função SHEmptyRecycleBinW da API do Windows
        if ctypes.windll.shell32.SHEmptyRecycleBinW(None, caminho_lixeira, flags):
            print("Lixeira esvaziada com sucesso!")
        else:
            print("Erro ao esvaziar a Lixeira.")

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