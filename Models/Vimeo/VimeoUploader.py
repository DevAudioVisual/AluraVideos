import vimeo
import os

class VimeoUploader():
    def __init__(self):
        self.token = "f28eaf747f1e8f3ce2e2bcf289fd8cae"
        self.key = "5881a0108288c8e0fa45418cc0c40538bf6c9d5e"
        self.secret = "wNmMmQv9NXNVAui/EPIZU90bjDv8ZxvWHljwq+UA887/6jDzOalFhSB1C0nrX2Q83xvTxnRU3x2VWnb0uHZuhIjcIvke7t4qmEvkhhHFlmPbV+EiKY3H+x6DLPYgb2qE"
        self.client = vimeo.VimeoClient(self.token,self.key,self.secret)
          
    # Função para criar uma Showcase (álbum) sem parâmetros de privacidade
    def criar_showcase(self, nome_showcase):
        showcase_data = {
            'name': nome_showcase,
            'description': 'Esta é uma showcase criada via AluraVideos'
        }

        response = self.client.post('/me/albums', data=showcase_data)
        
        if response.status_code == 201:
            print(f"Showcase '{nome_showcase}' criada com sucesso!")
            return response.json().get('uri')  # Retorna o URI da showcase
        else:
            print("Erro ao criar a Showcase:", response.json())
            return None

    # Função para subir múltiplos vídeos para o Vimeo e adicionar à Showcase
    def subir_videos_para_showcase(self,caminhos_videos, showcase_uri):    
        for video_path in caminhos_videos:
            if os.path.exists(video_path):          
                print(f"Iniciando upload de: {os.path.basename(video_path)}")
                self.video_response = self.client.upload(video_path, data={'name': os.path.basename(video_path)})
                if isinstance(self.video_response, str):  # Verifica se o retorno é uma string (URI do vídeo)
                    self.video_uri = self.video_response
                    print(f"Vídeo '{os.path.basename(video_path)}' enviado com sucesso!")

                    # Mudar a privacidade do vídeo para público
                    #self.client.patch(self.video_uri, data={'privacy': {'view': 'anybody'}})
                    #print(f"Privacidade do vídeo '{os.path.basename(video_path)}' alterada para 'público'.")

                    # Adicionar o vídeo à showcase
                    showcase_add_response = self.client.put(f'{showcase_uri}{self.video_uri}')
                    if showcase_add_response.status_code == 204:
                        print(f"Vídeo '{os.path.basename(video_path)}' adicionado à showcase!\nId do vídeo:{self.video_uri}")
                    else:
                        print(f"Erro ao adicionar o vídeo à showcase: {showcase_add_response.status_code}")
                else:
                    print(f"Erro ao enviar o vídeo: {video_path}")
            else:
                print(f"Arquivo não encontrado: {video_path}")




