import os
from Models.VideoUploader import VideoUpload
import Util.CustomWidgets as cw
from PyQt6.QtWidgets import QHeaderView,QAbstractScrollArea

class VideoDialog(cw.Dialog):
    def __init__(self,showcase_id,video_files):
        super().__init__()
        self.showcase_id = showcase_id
        self.video_files = video_files
        
        self.setWindowTitle("Upload de Vídeos")
        self.resize(500, 300)

        self.table = cw.TableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Vídeo", "ID"])
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)  # Redimensiona colunas ao conteúdo
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)  # Redimensiona linhas ao conteúdo
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

        layout = cw.VBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.threads = []
        
        self.upload_videos()

    def add_video(self, video_name, video_id=""):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, cw.TableWidgetItem(os.path.basename(video_name)))
        self.table.setItem(row_position, 1, cw.TableWidgetItem(video_id))
        
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def upload_videos(self):

        for file_path in self.video_files:
            self.add_video(file_path)
            worker = VideoUpload.UploadWorker(self.showcase_id, file_path)
            worker.progress_signal.connect(self.update_progress)
            worker.finished_signal.connect(self.upload_finished)
            worker.error_signal.connect(self.upload_error)
            self.threads.append(worker)
            worker.start()

    def update_progress(self, percent, speed_str, remaining_time):
        current_row = self.table.rowCount() - 1
        self.table.setItem(current_row, 1, cw.TableWidgetItem(f"Progresso: {percent:.2f}% - Velocidade: {speed_str} - Tempo restante: {remaining_time:.2f} segundos"))
        
    def upload_finished(self, file_path, video_id):
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() == os.path.basename(file_path):
                self.table.setItem(row, 1, cw.TableWidgetItem(f"0nK/{video_id}"))
                break

    def upload_error(self, error_message):
        print(error_message)