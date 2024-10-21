from concurrent.futures import ThreadPoolExecutor
import os
import numpy as np
import resampy
import soundfile as sf
from Models.VideoValidator.TableManager import criar_tabela
import Models.VideoValidator.audioset.yamnet.params as yamnet_params
import Models.VideoValidator.audioset.yamnet.yamnet as yamnet_model

class AudioAnalyse():
    def __init__(self,videos,limiar,classes_ativadas,classes_desativadas,audio_path):
        self.recusar = [""] #["Speech","Silence","Inside, small room"]
        
        self.audio_path = audio_path
        
        self.classes_ativadas = classes_ativadas
        self.classes_desativadas = classes_desativadas
        self.limiar = limiar / 100
        
        self.videos = videos
        
        self.resume = {}
        
        self.params = yamnet_params.Params()
        self.yamnet = yamnet_model.yamnet_frames_model(self.params)
        self.yamnet.load_weights(r'TensorModels\yamnet.h5')
        self.yamnet_classes = yamnet_model.class_names(r'TensorModels\yamnet_class_map.csv')

    def Analyse(self, video_path):
        print(f"Iniciando analise de {os.path.basename(video_path)}")
        # Verificar se o caminho do arquivo de áudio existe
        audio_file = self.audio_path.get(video_path, None)
        if not audio_file or not os.path.exists(audio_file):
            print(f"Falha ao converter ou encontrar o arquivo de áudio: {video_path}")
            return {}
        
        try:
            # Tente ler o arquivo de áudio
            resultado_sf_read = sf.read(audio_file, dtype=np.int16)
        except Exception as e:
            print(f"Erro ao ler o arquivo de áudio: {e}")
            return {}

        # Verifica se o resultado contém dados válidos
        if len(resultado_sf_read) != 2 or len(resultado_sf_read[0]) == 0:
            print(f"Erro ao ler o arquivo de áudio ou arquivo vazio: {audio_file}")
            return {}
        
        wav_data, sr = resultado_sf_read
        
        # Converta wav_data explicitamente para NumPy, caso ainda não seja
        waveform = np.array(wav_data) / 32768.0  # Normaliza para o intervalo [-1.0, +1.0]
        waveform = waveform.astype('float32')

        # Verifica se o áudio é estéreo e converte para mono se necessário
        if len(waveform.shape) > 1:
            waveform = np.mean(waveform, axis=1)
        
        # Ajuste a taxa de amostragem se necessário
        if sr != self.params.sample_rate:
            waveform = resampy.resample(waveform, sr, self.params.sample_rate)

        # Prever classes usando YAMNet
        scores, embeddings, spectrogram = self.yamnet(waveform)
        time_per_frame = self.params.patch_hop_seconds 
        
        video_resume = {}  # Dicionário para armazenar as anomalias e timecodes

        skip_frames = int(2 / time_per_frame)

        for i, score in enumerate(scores):
            if i < skip_frames:
                continue  # Pular os frames dos primeiros 2 segundos      
        
            top_class_index = np.argmax(score)
            top_class_name = self.yamnet_classes[top_class_index]
            top_class_score = score[top_class_index]

            if top_class_score > self.limiar and top_class_name in self.classes_ativadas and top_class_name not in self.classes_desativadas:
                timecode_seconds = i * time_per_frame
                minutes = int(timecode_seconds // 60)
                seconds = int(timecode_seconds % 60)
                timecode = f"{minutes:02d}:{seconds:02d}"

                # Se a anomalia já existir no resumo do vídeo, adicione o timecode e o score
                top_class_score = f"{top_class_score:.3f}"
                if top_class_name in video_resume:
                    video_resume[top_class_name].append({"timecode": timecode, "score": top_class_score})
                else:
                    video_resume[top_class_name] = [{"timecode": timecode, "score": top_class_score}]

                #print(f"{os.path.basename(video_path)} Anomalia detectada em {timecode}: {top_class_name} {top_class_score}")
        print(f"Analise concluida para {os.path.basename(video_path)}")
        return video_resume

        

    def start(self):
        resume = {}
        with ThreadPoolExecutor(max_workers=8):
            for video in self.videos:
                resume[os.path.basename(video)] = self.Analyse(video)
        #with open("relatorio.json", "w") as f:
        #    json.dump(resume, f, indent=4)
        criar_tabela(resume)
        #print(self.resume)
            
        print("##################################")
        print("Todas as tarefas foram concluídas!")
        print("##################################")
            