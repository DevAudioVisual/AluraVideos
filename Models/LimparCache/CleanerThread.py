import ctypes
import os
import shutil
import stat
from PyQt6.QtCore import QThread, pyqtSignal
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