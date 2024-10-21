from concurrent.futures import ThreadPoolExecutor
import os
import tempfile
from tkinter import filedialog
from PyQt6.QtGui import QIcon
import moviepy.editor as mp
from QtInterfaces.Interfaces.VideoValidator.InterfaceAudioAnalyse import InterfaceAudio
from QtInterfaces.Interfaces.VideoValidator.InterfaceVideoAnalyse import InterfaceVideo
import Util.CustomWidgets as cw
global Config

class Interface(cw.Widget):
    def __init__(self):
        super().__init__() 
        self.setContentsMargins(10, 10, 10, 10)
        
        self.videos = [] 

        self.campo_videos = cw.LineEdit()
        self.campo_videos.setPlaceholderText("Diga os vídeos para analizar")
        self.campo_videos.setClearButtonEnabled(True)
        self.action_campo_videos = self.campo_videos.addAction(QIcon(r"Assets\Images\folder.png"),cw.LineEdit.ActionPosition.TrailingPosition)
        self.action_campo_videos.triggered.connect(self.buscarVideos)
        
        self.buttonanalisar = cw.PushButton("Iniciar análise")
        self.buttonanalisar.clicked.connect(self.iniciar)
        
        self.group_audio = cw.GroupBox("Audio:")
        layout_group_audio = cw.VBoxLayout()
        self.group_audio.setLayout(layout_group_audio)
        self.InterfaceAudio = InterfaceAudio()
        layout_group_audio.addWidget(self.InterfaceAudio)

        self.group_video = cw.GroupBox("Video:")
        layout_group_video = cw.VBoxLayout()
        self.group_video.setLayout(layout_group_video)
        self.InterfaceVideo = InterfaceVideo()
        layout_group_video.addWidget(self.InterfaceVideo)

        # Criar o widget container para o group_audio e group_video
        widget_container = cw.Widget()
        layout_container = cw.VBoxLayout()
        widget_container.setLayout(layout_container)
        layout_container.addWidget(self.group_video)  # Corrigido: adiciona group_video
        layout_container.addWidget(self.group_audio)

        # Criar a QScrollArea
        scroll_area = cw.ScrollArea()
        scroll_area.setWidget(widget_container)
        scroll_area.setWidgetResizable(True)  # Permite que o conteúdo seja redimensionado

        # Configurar a política de redimensionamento do widget container
        widget_container.setSizePolicy(cw.SizePolicy.Policy.Expanding, cw.SizePolicy.Policy.Expanding)

        # Adicionar a scroll_area ao layout principal
        layout_main = cw.VBoxLayout()
        self.setLayout(layout_main)
        layout_main.addWidget(self.campo_videos)
        layout_main.addWidget(scroll_area)  # Adicionar a scroll_area
        layout_main.addWidget(self.buttonanalisar)
        
    def iniciar(self):     
        try: 
            videos = {}
            for v in self.videos:
                    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio_file:
                        video = mp.VideoFileClip(v)
                        video.audio.write_audiofile(temp_audio_file.name, codec='pcm_s16le', ffmpeg_params=['-ar', '16000'])
                        videos[v] = temp_audio_file.name   
                
            items = [self.InterfaceAudio.lista_selecionados.item(i).text() for i in range(self.InterfaceAudio.lista_selecionados.count())]
            items_desativados = [self.InterfaceAudio.lista_desativada_selecionados.item(i).text() for i in range(self.InterfaceAudio.lista_desativada_selecionados.count())]
            
            # from Models.VideoValidator.VideoAnalyse import VideoAnalyse
            # VideoAnalyse(analise_videos=self.videos,
            #                  checkEnquadramento=self.InterfaceVideo.check_enquadramento.isChecked(),
            #                  checkFPS=self.InterfaceVideo.check_frame_rate.isChecked()).Validar()
            
            from Models.VideoValidator.AudioAnalyse import AudioAnalyse
            AudioAnalyse(videos=self.videos,
                          classes_ativadas=items,
                          classes_desativadas=items_desativados,
                          limiar=self.InterfaceAudio.getslider_limiar().value(),
                          audio_path=videos).start()
            
        except Exception as e:
            print(f"Ocorreu um erro ao converter: {e}")
        
    def buscarVideos(self):
        filters = "*.mp4 *.avi *.mov *.mkv"
        file_names = filedialog.askopenfilenames(filetypes=[("Arquivos de Vídeo", filters)])
        if file_names:
            self.campo_videos.setText(file_names[0])
            for file_name in file_names:
                self.videos.append(file_name)

