import os
import re
import subprocess
from Util import Util
import Util.CustomWidgets as cw
from PyQt6.QtCore import Qt,QThread,pyqtSignal
from PyQt6.QtGui import QIcon
from tkinter import filedialog

class Interface(cw.Widget):
    def __init__(self):
        super().__init__()

        self.setContentsMargins(10, 10, 10, 10)

        self.layoutPrincipal = cw.VBoxLayout()
        self.layoutGrid = cw.GridLayout()
        
        self.label_arquivos = cw.Label("Arquivos:")
        self.campo_videos = cw.LineEdit()
        self.campo_videos.setPlaceholderText("Arquivos para converter")
        self.campo_videos.setClearButtonEnabled(True)
        self.action_campo_videos = self.campo_videos.addAction(QIcon(r"Assets\svg\folder.svg"),cw.LineEdit.ActionPosition.TrailingPosition)
        self.action_campo_videos.setToolTip("Buscar")
        self.action_campo_videos.triggered.connect(self.setVideos)
        
        self.label_saida = cw.Label("Saida:")
        self.campo_saida = cw.LineEdit()
        self.campo_saida.setPlaceholderText("Pasta de saída")
        self.campo_saida.setClearButtonEnabled(True)
        self.action_campo_saida = self.campo_saida.addAction(QIcon(r"Assets\svg\folder.svg"),cw.LineEdit.ActionPosition.TrailingPosition)
        self.action_campo_saida.setToolTip("Buscar")
        self.action_campo_saida.triggered.connect(self.setDirSaida)
        
        self.label_converter_para = cw.Label("Converter para:")
        self.combo_tipo = cw.ComboBox()
        self.combo_tipo.addItems([".mp4",".avi",".mov",".mkv"])
        
        self.checkbox_ativar = cw.CheckBox("Manter as propriedades originais", self)
        self.checkbox_ativar.stateChanged.connect(self.ativar_widgets)
        self.checkbox_ativar.setChecked(True)
        
        self.label_Encoder = cw.Label("Encoder:")
        self.combo_Encoder = cw.ComboBox()
        self.combo_Encoder.addItems(["h264_nvenc","libx264"])
        
        self.label_preset = cw.Label("Preset:")
        self.combo_preset = cw.ComboBox()
        self.combo_preset.addItems(["fast","medium","slow"])
        
        self.label_crf = cw.Label("CRF: 10")
        def atualizar_label():
          self.label_crf.setText(f"CRF: {self.slider_crf.value()}")
        self.slider_crf = cw.Slider(Qt.Orientation.Horizontal)
        self.slider_crf.setTickPosition(cw.Slider.TickPosition.TicksBelow)
        self.slider_crf.valueChanged.connect(atualizar_label)
        self.slider_crf.setTickInterval(10)  
        self.slider_crf.setMaximum(51)
        self.slider_crf.setMinimum(1)
        self.slider_crf.setValue(10)
        
        self.label_resolucao = cw.Label("Resolução:")
        self.combo_resolucao = cw.ComboBox()
        self.combo_resolucao.addItem("Original")
        self.combo_resolucao.addItem("Dual-HD 3840x1080 32:9")
        self.combo_resolucao.addItem("UW-HD 2560x720 21:9)")
        self.combo_resolucao.addItem("---------------------------")
        self.combo_resolucao.addItem("8K 7680x4320 16:9")
        self.combo_resolucao.addItem("4K 3840x2160 16:9")
        self.combo_resolucao.addItem("2K 2560x1440 16:9")
        self.combo_resolucao.addItem("FHD 1920x1080 16:9")
        self.combo_resolucao.addItem("HD 1280x720 16:9")
        # Desabilita o item de índice 4
        self.combo_resolucao.model().item(3).setEnabled(False)
        
        self.progressbar= cw.ProgressBar()
        
        self.botao_converter = cw.PushButton("Converter")
        self.botao_converter.clicked.connect(self.converter)
        
        self.layoutPrincipal.addWidget(self.label_arquivos)
        self.layoutPrincipal.addWidget(self.campo_videos)
        self.layoutPrincipal.addWidget(self.label_saida)
        self.layoutPrincipal.addWidget(self.campo_saida)
        self.layoutPrincipal.addWidget(self.label_converter_para)
        self.layoutPrincipal.addWidget(self.combo_tipo)
        self.layoutPrincipal.addWidget(self.checkbox_ativar)
        
        self.layoutPrincipal.addLayout(self.layoutGrid)
        
        self.layoutGrid.addWidget(self.label_Encoder, 0, 0)
        self.layoutGrid.addWidget(self.combo_Encoder, 1, 0)
        
        self.layoutGrid.addWidget(self.label_preset, 0, 1)
        self.layoutGrid.addWidget(self.combo_preset, 1, 1)
        
        self.layoutGrid.addWidget(self.label_crf, 0, 2)
        self.layoutGrid.addWidget(self.slider_crf, 1, 2)
        
        self.layoutGrid.addWidget(self.label_resolucao, 2, 0)
        self.layoutGrid.addWidget(self.combo_resolucao, 3, 0)
        
        self.layoutPrincipal.addWidget(self.progressbar)
        self.layoutPrincipal.addWidget(self.botao_converter)
        
        self.setLayout(self.layoutPrincipal)
        
        self.videos = []
        self.dir_saida = ""
        self.ativar_widgets(True)
    def ativar_widgets(self, estado):
      estado_booleano = not bool(estado)
      for i in range(self.layoutGrid.count()):
          item = self.layoutGrid.itemAt(i)
          # Verifica se o item realmente contém um widget
          if item and item.widget():
              widget = item.widget()
              widget.setEnabled(estado_booleano)
    def setVideos(self):
      files = filedialog.askopenfilenames()
      self.campo_videos.setText(str(files))
      for file in files:
        self.videos.append(file)
        
    def setDirSaida(self):
      files = filedialog.askdirectory()
      self.campo_saida.setText(files)
      self.dir_saida = files
      
    def update_progress(self, value):
      self.progressbar.setValue(value) 
      
    def finalizado():
      cw.MessageBox.information(None,"Sucesso!","Videos convertidos com exito.")
      
    def converter(self):
      self.thread = ConvertThread(self.videos, self.combo_tipo, self.slider_crf, self.dir_saida, self.combo_resolucao, self.checkbox_ativar,self.combo_Encoder, self.combo_preset)
      self.thread.progress_updated.connect(self.update_progress)
      self.thread.finished.connect(self.finalizado)
      self.thread.start()
      
class ConvertThread(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, videos, combo_tipo, slider_crf, dir_saida, combo_resolucao, checkbox_ativar, combo_Encoder, combo_preset):
        super().__init__()
        self.videos = videos
        self.combo_tipo = combo_tipo
        self.slider_crf = slider_crf
        self.dir_saida = dir_saida
        self.combo_resolucao = combo_resolucao
        self.checkbox_ativar = checkbox_ativar
        self.combo_Encoder = combo_Encoder
        self.combo_preset = combo_preset

    def run(self):
        try:
            if not self.videos or not self.dir_saida:
                return
            formato_video = self.combo_tipo.currentText()
            for video in self.videos:
                print("Iniciando conversão para:", video)
                nome = os.path.basename(video)
                nome = os.path.splitext(nome)[0] + formato_video
                caminho_completo = os.path.join(self.dir_saida, nome)
                crf_value = int(self.slider_crf.value())
                res_item = self.combo_resolucao.currentText()
                res_regex = r"(\d+)x(\d+)"
                res_match = re.search(res_regex, res_item)
                if res_match:
                    largura = res_match.group(1)
                    altura = res_match.group(2)
                    resolucao = f"{largura}:{altura}"
                else:
                    resolucao = "Original"

                if not self.checkbox_ativar.isChecked():
                    if resolucao != "Original":
                        command = [
                            Util.pegarFFMPEG(),
                            "-hwaccel", "cuda",
                            "-i", video,
                            "-y",
                            "-s", resolucao,
                            "-c:v", self.combo_Encoder.currentText(),
                            "-crf", str(crf_value),
                            "-profile:v", "high",
                            "-preset", self.combo_preset.currentText(),
                            caminho_completo
                        ]
                    else:
                        command = [
                            Util.pegarFFMPEG(),
                            "-hwaccel", "cuda",
                            "-i", video,
                            "-y",
                            "-c:v", self.combo_Encoder.currentText(),
                            "-crf", str(crf_value),
                            "-profile:v", "high",
                            "-preset", self.combo_preset.currentText(),
                            caminho_completo
                        ]
                else:
                    command = [Util.pegarFFMPEG(), "-i", video, "-y", "-c", "copy", caminho_completo]

                print("Comando gerado:", command)

                # Usar Popen para rodar o ffmpeg e capturar o stderr
                process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)

                duration = None
                for line in process.stderr:
                    print(line, end='') 
                    if duration is None:
                        duration_match = re.search(r"Duration:\s*(\d{2}):(\d{2}):(\d{2})\.(\d{2})", line)
                        if duration_match:
                            duration = (int(duration_match.group(1)) * 3600 +
                                        int(duration_match.group(2)) * 60 +
                                        int(duration_match.group(3)) +
                                        float(duration_match.group(4)) / 100)
                    else:
                        time_match = re.search(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})", line)
                        if time_match:
                            elapsed_time = (int(time_match.group(1)) * 3600 +
                                            int(time_match.group(2)) * 60 +
                                            int(time_match.group(3)) +
                                            float(time_match.group(4)) / 100)
                            progress = (elapsed_time / duration) * 100
                            if progress >= 100: progress = 0
                            self.progress_updated.emit(int(progress))  # Emite o progresso como inteiro
                
                process.wait()  # Espera o processo terminar
                self.finished.emit()  # Emite o sinal de finalização

        except Exception as e:
            print(f"Erro ao converter o vídeo: {e}")
