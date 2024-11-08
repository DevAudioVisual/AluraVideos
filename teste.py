import requests

response = requests.post("https://aluravideosapi.onrender.com/login",
                         json={
                             "username": "usuario_exemplo",
                             "password": "senha123"
                             },
                         timeout=15)

if response.status_code == 200:
    # Se a autenticação for bem-sucedida, obtem o token de acesso
    access_token = response.json().get("access_token")
    print("Autenticação bem-sucedida. Token de acesso:", access_token)
else:
    # Em caso de erro
    print("Falha na autenticação:", response.json().get("message"))
