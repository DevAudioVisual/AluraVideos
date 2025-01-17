import requests

from Models.VideoUploader import UploaderTokenManager

def create_showcase(showcase):
    url = "https://video-uploader.alura.com.br/api/showcase/create"
    # Define o body da requisição
    headers = {
        "X-API-TOKEN": UploaderTokenManager.token()
    }
    params = {
        "title": showcase
    }

    # Faz a requisição POST
    response = requests.post(url, headers=headers,json=params)

    # Retorna a resposta
    return response
