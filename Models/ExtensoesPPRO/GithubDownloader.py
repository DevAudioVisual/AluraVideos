import base64
import requests
import shutil
import os
import zipfile
from PyQt6.QtWidgets import QMessageBox
import yaml
from packaging import version

class GithubUpdater:
    def __init__(self, versao_atual_ordinem, versao_atual_effector, versao_atual_notabillity):
        self.repositorios = {
            "Ordinem": {"url": "https://api.github.com/repos/DevAudioVisual/Ordinem/contents/version.yml", "versao": versao_atual_ordinem},
            "Effector": {"url": "https://api.github.com/repos/DevAudioVisual/Effector/contents/version.yml", "versao": versao_atual_effector},
            "Notability": {"url": "https://api.github.com/repos/DevAudioVisual/Notability/contents/version.yml", "versao": versao_atual_notabillity}
        }

    def verificar_atualizacoes(self):
        repositorios_desatualizados = {} # Dicionário para armazenar repositórios e suas versões
        for nome, dados in self.repositorios.items():
            url = dados["url"]
            versao_repositorio = dados["versao"]
            try:
                resposta = requests.get(url)
                resposta.raise_for_status()
                if resposta.status_code == 200:
                    conteudo_base64 = resposta.json()["content"]
                    conteudo = base64.b64decode(conteudo_base64).decode("utf-8")

                    # Carrega o YAML e processa a versão
                    dados_yaml = yaml.safe_load(conteudo)
                    versao_github = dados_yaml.lower()
                    versao_github = versao_github.replace("Version: ","")
                    versao_repositorio = str(versao_repositorio).replace("Version: ","")

                    if versao_github:
                        versao_github = version.parse(str(versao_github)) # Converte para string antes de analisar
                        versao_repositorio = version.parse(str(versao_repositorio)) # Converte para string antes de analisar

                        if versao_repositorio < versao_github:
                            repositorios_desatualizados[nome] = versao_github # Armazena a versão do GitHub
                else:
                    print(f"Erro ao acessar o arquivo {nome}: {resposta.status_code}")
            except Exception as e:
                print(f"Erro ao verificar {nome}: {e}")

        return repositorios_desatualizados # Retorna o dicionário


class GithubDownloader:
    def __init__(self, repo_owner, repo_name):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
    def VerificarExistente(self,download_path):
        pasta = self.encontrar_pasta_teste(download_path,self.repo_name)
        if pasta:
            try:
                pasta_path = os.path.join(download_path, pasta)
                shutil.rmtree(pasta_path)  # Usando shutil.rmtree para remover a pasta e seu conteúdo
                print(f"Pasta '{pasta}' removida com sucesso.")
                return True
            except PermissionError:
                QMessageBox.information(None,"Info","Ocorreu um erro no processo de instalação, permissão negada.")
                print(f"Erro: Não foi possível remover a pasta '{pasta}'. Permissão negada. Verifique se a pasta ou algum arquivo dentro dela está em uso.")
                return False
            except FileNotFoundError:
                QMessageBox.information(None,"Info","Ocorreu um erro no processo de instalação, pasta não encontrada.")
                print(f"Erro: Não foi possível remover a pasta '{pasta}'. Pasta não encontrada.")
                return False
            except Exception as e:
                QMessageBox.information(None,"Info","Ocorreu um erro inesperado no processo de instalação.")
                print(f"Erro inesperado ao remover a pasta '{pasta}': {e}")
                return False
        else:
            print(f"Nenhuma pasta encontrada começando com '{self.repo_name}'")
            return True
            
    def download_sourcecode(self, download_path):
        if not self.VerificarExistente(download_path):
            return
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()

            release_data = response.json()
            zipball_url = release_data["zipball_url"]

            zip_file_path = os.path.join(download_path, f"{self.repo_name}.zip")

            response = requests.get(zipball_url, stream=True)
            response.raise_for_status()

            with open(zip_file_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)

            print(f"Código-fonte baixado com sucesso para {zip_file_path}")

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(download_path)
            os.remove(zip_file_path)
            print(f"Arquivo {self.repo_name}.zip descompactado em {download_path}")
            
            nome = self.encontrar_pasta_teste(download_path,f"DevAudioVisual-{self.repo_name}")
            caminho_completo = os.path.join(download_path, nome)
            os.rename(caminho_completo, os.path.join(download_path, self.repo_name))
            
            QMessageBox.information(None,"Info",f"{self.repo_name} instalado com sucesso.")

        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar o código-fonte: {e}")
        except Exception as e:
            print(f"Erro ao descompactar ou renomear a pasta: {e}")
            
    def encontrar_pasta_teste(self, diretorio, pasta):
        for nome in os.listdir(diretorio):
          caminho_completo = os.path.join(diretorio, nome)
          if os.path.isdir(caminho_completo) and nome.startswith(pasta):
            return nome
        return None
