import requests
import os
from tqdm import tqdm

class App():
    def __init__(self, filename, extract_folder_path, extract_folder_name):
        self.filename = filename
        self.extract_folder_path = extract_folder_path
        self.extract_folder_name = extract_folder_name
        self.url = None
        self.filename_element = None
    def startDownload(self):
        self.download_file()
        # with ThreadPoolExecutor() as executor:
        #     futures = [executor.submit(self.download_file, file_id) for file_id in file_ids]
        #     for future in futures:
        #         future.result()


    def download_file(self,chunk_size=8192):
        self.url = f'https://www.dropbox.com/scl/fo/x3pobwptwyjc83aoxqkw3/AGIfXRqGcVjFJOSAOp1u1Dw?rlkey=za0ssx4hqi2tby6xdxh7b7og3&st=2bpi9h7a&dl=1'
        filename = "arquivo_videos.zip"
        if not self.url or not filename:
            print(f"Não foi possivel encontrar um download válido para o ID:")
            return

        if self.url:
            folderpath = os.path.join(self.extract_folder_path,self.extract_folder_name)
            os.makedirs(folderpath, exist_ok=True)
            filepath = os.path.join(folderpath,filename)

            response = requests.get(self.url, stream=True, allow_redirects=True)
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
            print(f"Erro: Não foi possível encontrar o link de download para o arquivo com ID:")
            
            
teste = App(filename=r"C:\Users\Samuel\Desktop\links.txt",
            extract_folder_path=r"C:\Users\Samuel\Desktop",
            extract_folder_name="DropTeste")
teste.startDownload()
