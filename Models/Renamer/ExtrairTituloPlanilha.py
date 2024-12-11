import re
from bs4 import BeautifulSoup
import requests

from Util import Util

def extrair_titulo_planilha(url_planilha):
        try:
            # Faz a requisição à página da planilha
            response = requests.get(url_planilha)
            response.raise_for_status()  # Lança uma exceção se houver erro na requisição

            # Analisa o HTML da página
            soup = BeautifulSoup(response.content, 'html.parser')

            # Tenta encontrar o título na estrutura HTML (pode precisar ajustar isso)
            titulo_elemento = soup.find('title')
            if titulo_elemento:
                titulo = titulo_elemento.text.strip()
                # Remove o sufixo "- Google Sheets" se existir
                titulo = titulo.replace(" - Google Sheets", "")
                padrao = r"^\d{4}"  # Expressão regular para encontrar 4 dígitos no início da string
                correspondencia = re.match(padrao, titulo)
                return correspondencia.group(0)
            else:
                return None  # Retorna None se não encontrar o título

        except requests.exceptions.RequestException as e:
            Util.LogError("RenamerSheets",f"Erro ao acessar a página: {e}")
            return None