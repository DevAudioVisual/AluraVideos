import tempfile
import numpy as np
import soundfile as sf
import tensorflow as tf
import yamnet as yamnet_model
import params as yamnet_params
import csv
import moviepy as mp

def comparar(file_path):
    # Carregar o modelo YAMNet
    params = yamnet_params.Params()
    model = yamnet_model.yamnet_frames_model(params)
    model.load_weights('yamnet.h5')

    # Carregar o mapeamento de classes (as 521 classes do AudioSet)
    class_map_path = yamnet_model.CLASS_MAP_PATH
    class_names = []
    with open(class_map_path) as csvfile:
        reader = csv.reader(csvfile)
        class_names = [row[0] for row in reader]

    # Função para processar o áudio
    def process_audio():
        # Carregar o áudio usando soundfile
        waveform, sr = sf.read(file_path)
        
        # A YAMNet requer uma taxa de amostragem de 16kHz
        if sr != 16000:
            raise ValueError('A taxa de amostragem do áudio deve ser 16kHz')

        # Convertendo para tensor do TensorFlow
        waveform_tensor = tf.convert_to_tensor(waveform, dtype=tf.float32)

        # Executar o modelo no áudio para obter as previsões de classes
        scores, embeddings, spectrogram = model.predict(np.reshape(waveform_tensor.numpy(), (1, -1)), steps=1)

        # A média das pontuações ao longo do tempo fornece uma probabilidade de classe geral
        mean_scores = np.mean(scores, axis=0)
        
        # Pegar as 10 classes mais prováveis
        top_10_indices = np.argsort(mean_scores)[::-1][:10]
        
        print("Classes mais prováveis:")
        for i in top_10_indices:
            print(f"{class_names[i]}: {mean_scores[i]:.3f}")



    # Processar um arquivo de áudio
    if file_path.endswith(('.mp4', '.avi', '.mov')):  
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio_file:
                print("###########",file_path)
                video = mp.VideoFileClip(file_path)
                print("###########",temp_audio_file.name)
                video.audio.write_audiofile(temp_audio_file.name, codec='pcm_s16le', ffmpeg_params=['-ar', '16000'])
                file_path = temp_audio_file.name
                process_audio(file_path)
                

