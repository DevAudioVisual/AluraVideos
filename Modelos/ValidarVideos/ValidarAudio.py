import librosa
import numpy as np
import moviepy.editor as mp
import tempfile
import os
import soundfile as sf

def calcular_volume_medio(audio_file, output_voice_file=None, output_noise_file=None):
    y, sr = librosa.load(audio_file)

    frame_length = int(sr * 0.025)  # 25 ms de frame
    hop_length = int(sr * 0.01)    # 10 ms de hop
    energy = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)

    # Converte a energia para dB
    energy_db = librosa.power_to_db(energy.squeeze())

    # Estima o limiar de voz vs. ruído
    threshold = np.percentile(energy_db, 75)  # Ajustável

    # Separa os frames de voz e ruído
    # Certifique-se de que o número de frames em energy_db corresponda ao número de frames em y
    n_frames = 1 + len(y) // hop_length 
    voice_frames = np.zeros(n_frames, dtype=bool)
    voice_frames[:len(energy_db)] = energy_db > threshold
    noise_frames = np.logical_not(voice_frames)

    # Calcula o volume médio da voz e do ruído
    avg_voice_volume = np.mean(energy_db[voice_frames[:len(energy_db)]]) # Indexar apenas até o tamanho de energy_db
    avg_noise_level = np.mean(energy_db[noise_frames[:len(energy_db)]]) # Indexar apenas até o tamanho de energy_db

    # Reamostra os frames de voz e ruído para corresponder ao tamanho de y
    voice_frames_resampled = np.repeat(voice_frames, hop_length)[:len(y)]
    noise_frames_resampled = np.repeat(noise_frames, hop_length)[:len(y)]

    # Salva os frames de voz e ruído em arquivos separados, se especificado
    if output_voice_file:
        sf.write(output_voice_file, y[voice_frames_resampled], sr)
    if output_noise_file:
        sf.write(output_noise_file, y[noise_frames_resampled], sr)

    return avg_voice_volume, avg_noise_level

def calcular_volume_medio_video(video_file, output_voice_file=None, output_noise_file=None):

    video = mp.VideoFileClip(video_file)
    audio = video.audio

    # Cria um arquivo temporário para o áudio
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        audio.write_audiofile(temp_audio_file.name)

    # Calcula o volume médio e salva os arquivos, se especificado
    avg_voice_volume, avg_noise_level = calcular_volume_medio(
        temp_audio_file.name, output_voice_file, output_noise_file
    )

    # Exclui o arquivo temporário
    temp_audio_file.close()
    os.unlink(temp_audio_file.name)

    return avg_voice_volume, avg_noise_level

