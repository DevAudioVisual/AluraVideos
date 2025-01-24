import os
from Models.VideoUploader import VideoUpload
import Util.CustomWidgets as cw
from PyQt6.QtWidgets import QSizePolicy,QAbstractScrollArea,QHeaderView,QMenu

class UploadTable(cw.TableWidget):
    def __init__(self):
        super().__init__()
        
        self.files = []
        
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Vídeo", "ID"])
        
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Redimensiona colunas ao conteúdo
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Redimensiona linhas ao conteúdo
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.context_menu = QMenu(self)
        remove_action = self.context_menu.addAction("Remover")
        remove_action.triggered.connect(self.remover_linha)
        
        self.contextMenuEvent = self.table_context_menu_event
    

        self.threads = []
        
    def table_context_menu_event(self, event):
        item = self.itemAt(event.pos())
        if item:
            self.context_menu.exec(event.globalPos())

    def remover_linha(self):
        current_row = self.currentRow()
        valor = self.item(current_row,0).text()
        print("Removendo item: ", valor)

        for item in self.files:
            if valor in item:
                self.files.remove(item)
                break
        print(self.files)
            
        self.removeRow(current_row)
    def add_video(self, video_name, video_id="Aguardando upload..."):
        row_position = self.rowCount()
        self.insertRow(row_position)
        self.setItem(row_position, 0, cw.TableWidgetItem(extrair_apos_ultimo_hifen(os.path.basename(video_name))))
        self.setItem(row_position, 1, cw.TableWidgetItem(video_id))
        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def upload_videos(self,showcase_id,upload_paralelo):    
        self.showcase_id = showcase_id
        self.video_files = self.files
        self.upload_paralelo = upload_paralelo
        
        self.queue = self.video_files.copy()  # Cria uma fila com os arquivos de vídeo
        self.active_workers = 0  # Contador de workers ativos
        self.process_queue()

    def process_queue(self):
        while self.queue and self.active_workers < int(self.upload_paralelo):  # Inicia workers até atingir o limite de 3
            file_path = self.queue.pop(0)
            #self.add_video(file_path)
            worker = VideoUpload.UploadWorker(self.showcase_id, file_path)
            worker.progress_signal.connect(self.update_progress)
            worker.finished_signal.connect(self.upload_finished)
            worker.error_signal.connect(self.upload_error)
            worker.finished_signal.connect(self.worker_finished)  # Conecta o sinal finished para atualizar o contador e processar a fila
            self.threads.append(worker)
            worker.start()
            self.active_workers += 1

    def worker_finished(self):
        self.active_workers -= 1  # Decrementa o contador de workers ativos
        self.process_queue()

    def update_progress(self, file_path, percent, remaining_time):
        for row in range(self.rowCount()):
            if self.item(row, 0).text() == extrair_apos_ultimo_hifen(os.path.basename(file_path)):
                self.setItem(row, 1, cw.TableWidgetItem(f"Progresso: {percent:.2f}% - Tempo restante: {remaining_time}"))
                break
        #current_row = self.rowCount() - 1
       # self.setItem(current_row, 1, cw.TableWidgetItem(f"Progresso: {percent:.2f}% - Tempo restante: {remaining_time}"))
        
    def upload_finished(self, file_path, video_id):
        for row in range(self.rowCount()):
            if self.item(row, 0).text() == extrair_apos_ultimo_hifen(os.path.basename(file_path)):
                pre_id = str(video_id)[:3]
                self.setItem(row, 1, cw.TableWidgetItem(f"{pre_id}/{video_id}"))
                break
            
    def upload_error(self, file_path):
        for row in range(self.rowCount()):
            if self.item(row, 0).text() == extrair_apos_ultimo_hifen(os.path.basename(file_path)):
                self.setItem(row, 1, cw.TableWidgetItem(f"ERROR"))
                break

        
def extrair_apos_ultimo_hifen(texto):
  try:
    #ultimo_hifen = texto.rindex("-")
    #texto_final = texto[ultimo_hifen + 1:]
    texto_final = texto
    texto_final = texto_final.replace(".mp4", "")
    texto_final = texto_final.replace(".mov", "")
    return texto_final
  except ValueError:
    return ""