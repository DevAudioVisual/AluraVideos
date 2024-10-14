# Copyright 2019 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Inference demo for YAMNet."""
from __future__ import division, print_function

from concurrent.futures import ProcessPoolExecutor
import json
import math
import multiprocessing
import multiprocessing
import os
import sys
import tempfile

import numpy as np
import resampy
import soundfile as sf
import tensorflow as tf
import moviepy.editor as mp
import params as yamnet_params
import yamnet as yamnet_model

global anomalias
anomalias = {}

params = yamnet_params.Params()
yamnet = yamnet_model.yamnet_frames_model(params)
yamnet.load_weights(r'C:\Users\Samuel\Documents\GitHub\AluraValidator\models\research\audioset\yamnet\yamnet.h5')
yamnet_classes = yamnet_model.class_names(r'C:\Users\Samuel\Documents\GitHub\AluraValidator\models\research\audioset\yamnet\yamnet_class_map.csv')
def main(file_path):
  if file_path.endswith(('.mp4', '.avi', '.mov')):  
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio_file:
        video = mp.VideoFileClip(file_path)
        video.audio.write_audiofile(temp_audio_file.name, codec='pcm_s16le', ffmpeg_params=['-ar', '16000'])
        file_path = temp_audio_file.name

  

  # Decode the WAV file.
  wav_data, sr = sf.read(file_path, dtype=np.int16)
  waveform = wav_data / 32768.0  # Convert to [-1.0, +1.0]
  waveform = waveform.astype('float32')

  # Convert to mono and the sample rate expected by YAMNet.
  if len(waveform.shape) > 1:
    waveform = np.mean(waveform, axis=1)
  if sr != params.sample_rate:
    waveform = resampy.resample(waveform, sr, params.sample_rate)

  # Predict YAMNet classes.
  scores, embeddings, spectrogram = yamnet(waveform)
  # Scores is a matrix of (time_frames, num_classes) classifier scores.
  # Average them along time to get an overall classifier output for the clip.
  time_per_frame = params.patch_hop_seconds 
  prediction = np.mean(scores, axis=0)
  # Report the highest-scoring classes and their scores.
  for i, score in enumerate(scores):
    top_class_index = np.argmax(score)
    top_class_name = yamnet_classes[top_class_index]
    top_class_score = score[top_class_index]

    recusar = ["Silence"]
    
    if top_class_score > 0.1 and top_class_name not in recusar:
      
      arquivo_base = os.path.basename(file_path)
      
      global anomalias
      if arquivo_base not in anomalias:
        anomalias[arquivo_base] = []
      anomalias[arquivo_base].append({"anomalia": top_class_name, "tempo": timecode})
      print(anomalias)
      
      # Calcular o timecode em minutos:segundos
      timecode_seconds = i * time_per_frame
      minutes = int(timecode_seconds // 60)
      seconds = int(timecode_seconds % 60)
      timecode = f"{minutes:02d}:{seconds:02d}"

      print(f"{arquivo_base} Anomalia detectada em {timecode}: {top_class_name} ({top_class_score:.3f})")
    
  """
  top5_i = np.argsort(prediction)[::-1][:10]
  print(file_path, ':\n' +
        '\n'.join('  {:12s}: {:.3f}'.format(yamnet_classes[i], prediction[i])
                  for i in top5_i))
  """


if __name__ == '__main__':
  max_threads = math.ceil(multiprocessing.cpu_count() / 2)
  videos = [
            r"C:\Users\Samuel\Documents\GitHub\AluraValidator\video1.mov",
            r"C:\Users\Samuel\Documents\GitHub\AluraValidator\video2.mov",
            ]
  tarefas = 0
  with ProcessPoolExecutor(max_workers=max_threads) as executor:
    for video in videos:
      executor.submit(main,video)
      tarefas +=1
    executor.shutdown(wait=True)
  def finaly():
    global anomalias
    with open("anomalias.json", "w") as f:
          json.dump(anomalias, f, indent=4)
    print("##################################")
    print("##################################")
    print("Todas as tarefas foram concluídas!",tarefas)
    print("##################################")
    print("##################################")
  finaly()

  #main(r"C:\Users\Samuel\Documents\GitHub\AluraValidator\video1.mov")
