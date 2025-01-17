import requests

from Models.VideoUploader import UploaderTokenManager

def get_showcases(title):
  url = "https://video-uploader.alura.com.br/api/showcase/list"

  headers = {
      "X-API-TOKEN": UploaderTokenManager.token()
  }
  params = {
    "title": title
  }

  try:
    response = requests.get(url, headers=headers,params=params)
    response.raise_for_status()
    return response.json()
  except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
    return None
  except requests.exceptions.JSONDecodeError as e:
    print(f"Erro ao decodificar JSON: {e}")
    return None