import requests
import yaml
from packaging import version
from Util import Tokens

class GithubUpdater:
    def __init__(self, versao_atual_ordinem, versao_atual_effector, versao_atual_notabillity):
        def _query(repo):
            return f"""
                query {{
                    repository(owner: "DevAudioVisual", name: "{repo}") {{
                        object(expression: "master:version.yml") {{
                            ... on Blob {{
                                text
                            }}
                        }}
                    }}
                }}
            """
        self.repositorios = {

            "Ordinem": {"query": _query("Ordinem"), "versao": versao_atual_ordinem},
            
            "Effector": {"query": _query("Effector"), "versao": versao_atual_effector},
            
            "Notability": {"query": _query("Notability"), "versao": versao_atual_notabillity}
        }
        global GITHUB
        token = Tokens.GITHUB
        self.headers = {"Authorization": f"Bearer {token}"}
        
        self.url = "https://api.github.com/graphql"

    def verificar_atualizacoes(self):
        repositorios_desatualizados = {} # Dicionário para armazenar repositórios e suas versões
        for nome, dados in self.repositorios.items():
            query = dados["query"]
            versao_repositorio = dados["versao"]
            try:
                resposta = requests.post(self.url, headers=self.headers, json={"query": query})
                resposta.raise_for_status()
                if resposta.status_code == 200:
                    data = resposta.json()
                    version_yml_content = data['data']['repository']['object']['text']

                    # Carrega o YAML e processa a versão
                    dados_yaml = yaml.safe_load(version_yml_content)
                    dados_yaml = dados_yaml.get("Version")
                    versao_github = str(dados_yaml).lower()
                    versao_github = str(versao_github).replace("version: ","")
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