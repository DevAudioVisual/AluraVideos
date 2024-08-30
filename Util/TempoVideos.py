import Util.Util as Util
import subprocess
import os

def obter_duracao_video(caminho_video):
    """Obtém a duração de um vídeo em segundos usando ffprobe."""
    comando = [
        f"{Util.pegarFFPROBRE()}", 
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", 
        caminho_video
    ]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    if resultado.returncode == 0:
        return float(resultado.stdout)
    else:
        raise ValueError(f"Erro ao obter duração do vídeo: {resultado.stderr}")

def calcular_duracao_total(caminho_pasta):
    """Calcula a duração total dos vídeos em uma pasta e imprime em horas, minutos e segundos."""
    duracao_total = 0
    for arquivo in os.listdir(caminho_pasta):
        caminho_completo = os.path.join(caminho_pasta, arquivo)
        if os.path.isfile(caminho_completo) and arquivo.endswith((".mp4", ".avi", ".mkv",".mov")):
            try:
                duracao_video = obter_duracao_video(caminho_completo)
                duracao_total += duracao_video
            except ValueError as e:
                print(f"Erro ao processar {arquivo}: {e}")

    # Converter para horas, minutos e segundos
    horas = int(duracao_total // 3600)
    minutos = int((duracao_total % 3600) // 60)
    segundos = int(duracao_total % 60)

    return(f"{horas} horas, {minutos} minutos e  {segundos} segundos.")