from tkinter import messagebox
import cv2
import os
import tempfile
import subprocess
from concurrent.futures import ThreadPoolExecutor
import time

from Util import Util

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class VideoAnalyse():
  def __init__(self, analise_videos = "", checkFPS = True, checkEnquadramento = True):
    self.video_side = None
    self.ref_video = analise_videos[0]
    self.analise_videos = analise_videos
    self.checkFPS = checkFPS
    self.checkEnquadramento = checkEnquadramento
    
  def extract_frames(self,video_path, temp_dir, side='both'):
      """Extrai frames de um vídeo, considerando o lado especificado se for ultrawide."""
      if side not in ['left', 'right', 'both']:
          raise ValueError("O lado deve ser 'left', 'right' ou 'both'.")

      # Obter as dimensões do vídeo
      cap = cv2.VideoCapture(video_path)
      if not cap.isOpened():
          Util.LogError("ValidarVideos",f"Erro ao abrir o vídeo.")
          return
      width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
      height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
      cap.release()

      # Definir a parte do vídeo a ser extraída
      if side == 'left':
          crop_area = f"crop=w={width//2}:h={height}:x=0:y=0"
      elif side == 'right':
          crop_area = f"crop=w={width//2}:h={height}:x={width//2}:y=0"
      else:  # 'both'
          crop_area = None
      command = [f'{Util.pegarFFMPEG()}', '-hwaccel', 'cuda', '-threads', '0', '-i', rf"{video_path}"]
      if crop_area:
          command.extend(['-vf', crop_area])
      command.extend(['-vf', 'fps=1', os.path.join(temp_dir, 'frame_%04d.png')])

      print(f"Extracting frames from {video_path}...", end='\r')
      try:
          subprocess.call(command)
      except subprocess.CalledProcessError as e:
          Util.LogError("ValidarVideos",f"Erro ao executar o FFmpeg: {e}")
          return
      total_frames = len([f for f in os.listdir(temp_dir) if f.endswith('.png')])
      print(f"Frames extracted from {video_path} successfully! ({total_frames} frames)")

  def select_roi(self,frame):
      """Permite ao usuário selecionar uma ROI no frame."""
      # Desenhar uma linha no centro do frame
      height, width, _ = frame.shape
      center_x = width // 2
      center_y = height // 2
      cv2.line(frame, (center_x, 0), (center_x, height), (0, 255, 0), 1)
      cv2.line(frame, (0, center_y), (width, center_y), (0, 255, 0), 1)

      # Mostrar o frame com a linha no centro
      cv2.imshow("Selecione o ROI", frame)
      cv2.waitKey(1)

      # Selecionar a ROI
      roi = cv2.selectROI("Selecione o ROI", frame, fromCenter=False, showCrosshair=True)
      cv2.destroyWindow("Selecione o ROI")
      return roi

  def detect_face_center(self,frame):
      """Detecta o centro aproximado do rosto no frame e retorna suas coordenadas."""
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

      if len(faces) > 0:
          largest_face = max(faces, key=lambda x: x[2] * x[3])
          fx, fy, fw, fh = largest_face
          center = (fx + fw // 2, fy + fh // 2)
          return center
      else:
          return None

  def track_instructor(self,frames_dir, crop_x=0, crop_y=0):
      """Detecta o centro aproximado do rosto em cada frame da câmera, considerando o crop."""
      centers = []
      frame_files = sorted([f for f in os.listdir(frames_dir) if f.startswith('frame_') and f.endswith('.png')])
      total_frames = len(frame_files)
      print(f"Detecting faces in {total_frames} frames...", end='\r')

      for i, frame_file in enumerate(frame_files):
          frame = cv2.imread(os.path.join(frames_dir, frame_file))

          if frame is None:
              Util.LogError("ValidarVideos",f"Não foi possivel ler o frame {frame_file}. pulando para o próximo", False)
              #print(f"Error: Could not read frame {frame_file}. Skipping this frame...", end='\r')
              centers.append(None)
              continue 

          # Aplicar crop se necessário
          if crop_x > 0 or crop_y > 0:
              frame = frame[crop_y:, crop_x:]

          center = self.detect_face_center(frame)
          centers.append(center)

          progress = (i + 1) / total_frames * 100
          print(f"Detecting faces in {total_frames} frames... {progress:.2f}% ({i + 1}/{total_frames} frames processed)", end='\r')

      print()
      return centers

  def analyze_centralization(self,ref_centers, analise_centers, roi, video_path, log_file):
      """Analyzes if the face center is within the ROI and returns if there are anomalies."""
      x, y, w, h = roi
      ref_centers = [c for c in ref_centers if c is not None]
      if not ref_centers:
          Util.LogError("ValidarVideos",f"Não foi possível encontrar um rosto do vídeo de referência.")
          #print("Erro: Nenhum rosto detectado no vídeo de referência. Verifique a qualidade do vídeo ou ajuste os parâmetros de detecção.")
          return True

      anomaly_detected = False
      video_name = os.path.basename(video_path)
      video_name_no_ext = os.path.splitext(video_name)[0]

      # Define anomaly_messages here
      anomaly_messages = [] 
      for i, analise_center in enumerate(analise_centers):
          if analise_center is None:
              continue  # Ignore frames without face detection
          else:
              # Check if the face center is within the ROI
              cx, cy = analise_center
              if not (x <= cx <= x + w and y <= cy <= y + h):
                  timecode = f"{i // 60:02d}:{i % 60:02d}"
                  anomaly_message = f"   - Instrutor fora do enquadramento, no tempo: {timecode}"
                  anomaly_messages.append(anomaly_message)
                  anomaly_detected = True

      return anomaly_detected, anomaly_messages  

  def process_video(self,video_path, ref_centers, roi, temp_dir, crop_x=0, crop_y=0, log_file='log.txt'):
      print(f"Processing video {video_path}...", end='\r')
      if self.checkEnquadramento: 
        #self.extract_frames(video_path, temp_dir, side=self.video_side)
        analise_centers = self.track_instructor(temp_dir, crop_x=crop_x, crop_y=crop_y)

      # Analisar se há anomalias no enquadramento

      # Escrever resultados no log, combining audio and video
      with open(log_file, "a", encoding="utf-8") as f:
          f.write(f"\n{'*'*20} Vídeo: {os.path.basename(video_path)} {'*'*20}\n")
          
          if self.checkFPS:
            variacoes = self.verificar_variacao_frames(video_path, self.ref_video)
            f.write(f"Análise do framerate:\n")
            if variacoes:
              for variacao in variacoes:
                f.write(f"   - Variação detectada em {variacao['timecode']}, duração de {variacao['frames']} frames, FPS calculado: {variacao['fps_calculado']:.2f}\n")
            else:
              f.write(f"   - Nenhuma variação detectada.\n") 
          
          if self.checkEnquadramento:
            anomaly_detected, anomaly_messages = self.analyze_centralization(ref_centers, analise_centers, roi, video_path, log_file) # Receive anomaly_messages
            f.write(f"Análise de Enquadramento:\n")
            if anomaly_detected:
                f.write(f"   - Anomalias detectadas:\n")
                for msg in anomaly_messages:
                    f.write(msg + '\n')
            else:
                f.write(f"   - Nenhuma anomalia detectada.\n")


  def process_videos_in_parallel(self, videos, ref_centers, roi, crop_x=0, crop_y=0):
      start_time = time.time()

      log_file = os.path.join(os.path.dirname(videos[0]), 'log.txt')
      with open(log_file, "w", encoding="utf-8") as f:
          f.write(f"{'='*40}\n")
          f.write(f"Relatório de Análise de Vídeos\n")
          f.write(f"{'='*40}\n")
      num_threads = os.cpu_count()
      with ThreadPoolExecutor(max_workers=num_threads) as executor:
          futures = [executor.submit(self.process_video, video_path, ref_centers, roi, tempfile.mkdtemp(), crop_x, crop_y, log_file) for video_path in videos]
          for future in futures:
              future.result()  # Esperar até que todos os vídeos sejam processados

      end_time = time.time()
      total_time = end_time - start_time
      with open(log_file, "a", encoding="utf-8") as f:
          f.write(f"\n{'='*40}\n")
          f.write(f"Tempo total de processamento: {total_time:.2f} segundos\n")
          f.write(f"{'='*40}\n")
          
  def verificar_variacao_frames(self,video_path, video_referencia_path):
    cap_referencia = cv2.VideoCapture(video_referencia_path)
    fps_referencia = cap_referencia.get(cv2.CAP_PROP_FPS)
    cap_referencia.release()

    cap = cv2.VideoCapture(video_path)

    variacoes = []
    prev_frame_time = 0
    frames_variacao = 0
    fps_calculado_variacao = 0
    timecode_inicio_variacao = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Fim do vídeo

        current_frame_time = cap.get(cv2.CAP_PROP_POS_MSEC)
        if prev_frame_time > 0:
            calculated_fps = 1000 / (current_frame_time - prev_frame_time)
            if abs(calculated_fps - fps_referencia) > 1:  # Tolerância de 1 FPS
                if frames_variacao == 0:
                    # Início de uma nova variação
                    timecode_inicio_variacao = f"{int(current_frame_time / 3600000):02d}:{int(current_frame_time / 60000) % 60:02d}:{int(current_frame_time / 1000) % 60:02d}.{int(current_frame_time % 1000):03d}"
                    fps_calculado_variacao = calculated_fps
                frames_variacao += 1
            else:
                if frames_variacao > 0:
                    # Fim de uma variação, adiciona à lista
                    variacoes.append({
                        'timecode': timecode_inicio_variacao,
                        'frames': frames_variacao,
                        'fps_calculado': fps_calculado_variacao
                    })
                    frames_variacao = 0

        prev_frame_time = current_frame_time

    cap.release()
    return variacoes
      
  def Validar(self):
    with tempfile.TemporaryDirectory() as ref_temp_dir:

        ref_video_path = self.ref_video
        ref_first_frame_path = os.path.join(ref_temp_dir, 'frame_0001.png')

        cap = cv2.VideoCapture(ref_video_path)
        if not cap.isOpened():
            print("Erro ao abrir o vídeo.")
            exit(1)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

        if width > 1920:  # Largura comum para ultrawide
            self.video_side = input("O instrutor está no lado 'left' ou 'right' do vídeo? ").strip().lower()
        else:
            self.video_side = 'both'

        self.extract_frames(ref_video_path, ref_temp_dir, side=self.video_side)

        ref_first_frame = cv2.imread(ref_first_frame_path)
        if ref_first_frame is None:
            Util.LogError("ValidarVideos",f"Erro: Não foi possível ler o frame {ref_first_frame_path}. Verifique se o vídeo de referência é válido e se o FFmpeg extraiu os frames corretamente.", False)
            exit(1)

        # Se o vídeo for ultrawide, ajustar a parte do frame para mostrar apenas a metade selecionada
        crop_x = 0
        crop_y = 0
        if self.video_side in ['left', 'right']:
            # Definir o crop inicial para o frame
            if self.video_side == 'left':
                ref_first_frame = ref_first_frame[:, :width // 2]
                crop_x = 0
            else:  # 'right'
                ref_first_frame = ref_first_frame[:, width // 2:]
                crop_x = width // 2

        # Selecionar a ROI no frame de referência
        roi = self.select_roi(ref_first_frame)
        if roi == (0, 0, 0, 0):
            Util.LogError("ValidarVideos","Erro: ROI inválida. Certifique-se de selecionar uma região válida.")
            exit(1)

        # Rastrear o instrutor no vídeo de referência
        ref_centers = self.track_instructor(ref_temp_dir, crop_x, crop_y)

        # Processar vídeos em paralelo
        analise_videos = self.analise_videos
        self.process_videos_in_parallel(analise_videos, ref_centers, roi, crop_x, crop_y)
        messagebox.showinfo("Aviso","Validação concluida,\nArquivo de logs gerado")



