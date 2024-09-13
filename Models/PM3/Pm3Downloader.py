import io
import webbrowser
import requests
import re
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from bs4 import BeautifulSoup

class App():
    def __init__(self, filename, extract_folder_path, extract_folder_name):
        self.filename = filename
        self.extract_folder_path = extract_folder_path
        self.extract_folder_name = extract_folder_name
        self.url = None
        self.filename_element = None
    def startDownload(self):
        file_ids = self.extract_drive_links_and_ids()
        if not file_ids:
            print("Não foi possivel encontrar nenhum ID válido. Verifique se os links foram fornecidos corretamente.")
            return

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.download_file, file_id) for file_id in file_ids]
            for future in futures:
                future.result()
                
    def extract_drive_links_and_ids(self):
        with open(self.filename, 'r') as file:
            content = file.read()
            links = re.findall(r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)/view', content)
        return links

    def get_download_link_and_filename(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        span_element = soup.find('span')

        if span_element: 
            a_tag = span_element.find('a')
            if a_tag: 
                self.filename_element = a_tag.text.strip() 
            else:
                print("Tag <a> não encontrada dentro do <span>")
        else:
            print("Elemento <span> não encontrado, abrindo URL")
            webbrowser.open(self.url)
        if self.filename_element:
            filename = self.filename_element
        else:
            filename = "arquivo_sem_nome"

        download_form = soup.find('form', id='download-form')
        if download_form:
            action_url = download_form['action']
            query_params = []
            for input_field in download_form.find_all('input', {'type': 'hidden'}):
                query_params.append(f"{input_field['name']}={input_field['value']}")
            query_string = '&'.join(query_params)
            download_link = f"{action_url}?{query_string}"
            return download_link, filename
        else:
            print("Formulário de download não encontrado, abrindo URL")
            webbrowser.open(self.url)
            return None, None


    def download_file(self, file_id,chunk_size=8192):
        self.url = f'https://drive.usercontent.google.com/download?id={file_id}&export=download&authuser=0'
        download_link, filename = self.get_download_link_and_filename()
        if not download_link or not filename:
            print(f"Não foi possivel encontrar um download válido para o ID: {file_id}")
            return

        if download_link:
            folderpath = os.path.join(self.extract_folder_path,self.extract_folder_name)
            os.makedirs(folderpath, exist_ok=True)
            filepath = os.path.join(folderpath,filename)

            response = requests.get(download_link, stream=True, allow_redirects=True)
            total_size = int(response.headers.get('content-length', 0))
            with open(filepath, 'wb') as file, tqdm(
                desc=filename,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(chunk_size=chunk_size):
                    size = file.write(data)
                    bar.update(size) 
        else:
            print(f"Erro: Não foi possível encontrar o link de download para o arquivo com ID: {file_id}")
            
            
teste = App(filename=r"C:\Users\Samuel\Desktop\links.txt",
            extract_folder_path=r"C:\Users\Samuel\Desktop",
            extract_folder_name="97 - SQL para manipulação e análise de dados [PM3]")
teste.startDownload()
