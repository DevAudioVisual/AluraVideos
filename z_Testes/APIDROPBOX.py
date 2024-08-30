from concurrent.futures import ThreadPoolExecutor
import dropbox
import time
import os
import threading

class DropboxDownloader:
    def __init__(self, token, num_threads=4):
        self.dbx = dropbox.Dropbox(token)
        self.bytes_baixados_total = 0
        self.start_time_pasta = 0
        self.tamanho_total_pasta = 0
        self.lock = threading.Lock()
        self.taxa_download_maxima = 0
        self.num_threads = num_threads

    def calcular_tamanho_pasta(self, caminho_dropbox):
        tamanho_total = 0
        result = self.dbx.files_list_folder(path=caminho_dropbox)
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                tamanho_total += entry.size
            elif isinstance(entry, dropbox.files.FolderMetadata):
                tamanho_total += self.calcular_tamanho_pasta(entry.path_lower)
        return tamanho_total

    def ajustar_chunk_size(self, velocidade_media, chunk_size):
        if velocidade_media < 5 * 1024 * 1024:  
            return max(chunk_size // 2, 256 * 1024)  
        elif velocidade_media > 10 * 1024 * 1024:  
            return min(chunk_size * 2, 16 * 1024 * 1024)
        return chunk_size

    def baixar_pasta(self, caminho_dropbox, caminho_local):
        os.makedirs(caminho_local, exist_ok=True)
        self.tamanho_total_pasta = self.calcular_tamanho_pasta(caminho_dropbox)
        self.bytes_baixados_total = 0
        self.start_time_pasta = time.time()

        result = self.dbx.files_list_folder(path=caminho_dropbox)
        fila_downloads = [entry for entry in result.entries if isinstance(entry, dropbox.files.FileMetadata)]

        def baixar_arquivo(arquivo):
            caminho_arquivo_dropbox = arquivo.path_lower
            caminho_arquivo_local = os.path.join(caminho_local, arquivo.name)

            chunk_size = 1024 * 1024
            bytes_downloaded = 0
            start_time_arquivo = time.time()
            amostras_velocidade = []

            try:
                md, res = self.dbx.files_download(path=caminho_arquivo_dropbox)
                with open(caminho_arquivo_local, 'wb') as f:
                    while True:
                        inicio_chunk = time.time()
                        tentativas = 0
                        while tentativas < 3: 
                            try:
                                chunk = res.raw.read(chunk_size)
                                break 
                            except Exception as e:
                                print(f"Erro ao ler chunk de {caminho_arquivo_local}: {e}. Tentando novamente...")
                                tentativas += 1
                                time.sleep(1) 

                        if not chunk:
                            break
                        f.write(chunk)
                        with self.lock:
                            self.bytes_baixados_total += len(chunk)
                            bytes_downloaded += len(chunk)

                        tempo_chunk = time.time() - inicio_chunk
                        velocidade_chunk = len(chunk) / tempo_chunk if tempo_chunk > 0 else 0

                        amostras_velocidade.append(velocidade_chunk)
                        if len(amostras_velocidade) > 5:
                            amostras_velocidade.pop(0)
                        velocidade_media = sum(amostras_velocidade) / len(amostras_velocidade)

                        chunk_size = self.ajustar_chunk_size(velocidade_media, chunk_size)

                        taxa_download_bytes_pasta = self.bytes_baixados_total / (time.time() - self.start_time_pasta)
                        taxa_download_mb_pasta = taxa_download_bytes_pasta / (1024 * 1024)
                        self.taxa_download_maxima = max(self.taxa_download_maxima, taxa_download_mb_pasta)

            except dropbox.exceptions.HttpError as err:
                print(f"\nErro ao baixar o arquivo {caminho_arquivo_local}: {err}")
            except Exception as e:
                print(f"\nErro inesperado ao baixar o arquivo {caminho_arquivo_local}: {e}")

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [executor.submit(baixar_arquivo, arquivo) for arquivo in fila_downloads]

            while any(future.running() for future in futures):
                time.sleep(1)
                percentual_completo_pasta = 100 * self.bytes_baixados_total / self.tamanho_total_pasta
                taxa_download_bytes_pasta = self.bytes_baixados_total / (time.time() - self.start_time_pasta)
                taxa_download_mb_pasta = taxa_download_bytes_pasta / (1024 * 1024)

                bytes_restantes = self.tamanho_total_pasta - self.bytes_baixados_total
                tempo_estimado = bytes_restantes / taxa_download_bytes_pasta if taxa_download_bytes_pasta > 0 else 0

                horas, resto = divmod(tempo_estimado, 3600)
                minutos, segundos = divmod(resto, 60)
                tempo_formatado = f"{int(horas):02d}:{int(minutos):02d}:{int(segundos):02d}"

                print(f"Baixando pasta - Progresso: {percentual_completo_pasta:.1f}% - Taxa de download: {taxa_download_mb_pasta:.2f} MB/s - Tempo estimado: {tempo_formatado}", end='\r')

            for future in futures:
                future.result()

        percentual_completo_pasta = 100 * self.bytes_baixados_total / self.tamanho_total_pasta
        taxa_download_bytes_pasta = self.bytes_baixados_total / (time.time() - self.start_time_pasta)
        taxa_download_mb_pasta = taxa_download_bytes_pasta / (1024 * 1024)

        print(f"\nPasta baixada com sucesso - Progresso: {percentual_completo_pasta:.1f}% - Taxa de download média: {taxa_download_mb_pasta:.2f} MB/s")
        print(f"Pico máximo de taxa de download: {self.taxa_download_maxima:.2f} MB/s")

# Exemplo de uso
token = ""
caminho_dropbox = "/9999 - Curso teste - Intrutor testando"
caminho_local = "arquivo_baixado.zip"
downloader = DropboxDownloader(token)
downloader.baixar_pasta(caminho_dropbox, caminho_local)
