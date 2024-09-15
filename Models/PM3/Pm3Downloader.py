import io
import threading
import time
import webbrowser
import requests
import re
import os
from Util import Styles
import Util.CustomWidgets as ctk
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk

class App():
    def __init__(self, root, filename, extract_folder_path, extract_folder_name,max_workers):
        self.filename = filename
        self.extract_folder_path = extract_folder_path
        self.extract_folder_name = extract_folder_name
        self.url = None
        self.root = root
        self.filename_element = None
        self.max_workers = max_workers
        
        # Criação dos elementos da janela principal
        self.main_frame2 = tk.Toplevel()
        self.main_frame2.configure(bg=Styles.cor_fundo,padx=50,pady=50)
        self.main_frame2.lift()
        self.main_frame2.attributes('-topmost', True)
        self.main_frame2.after_idle(self.main_frame2.attributes, '-topmost', False)
        
        self.main_frame = ctk.CustomFrame(self.main_frame2)
        self.main_frame.pack(fill="both", expand=True, anchor="center")

        self.canvas = tk.Canvas(self.main_frame,bg=Styles.cor_fundo,)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = ctk.CustomFrame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        self.inner_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        self.progress_frames = {}

    def startDownload(self):
        file_ids = self.extract_drive_links_and_ids()
        if not file_ids:
            print("Não foi possivel encontrar nenhum ID válido. Verifique se os links foram fornecidos corretamente.")
            return
        def downloads():
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self.download_file, file_id) for file_id in file_ids]
                for future in futures:
                    future.result()
        threading.Thread(target=downloads,daemon=True).start()
                
    def extract_drive_links_and_ids(self):
        links = re.findall(r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)/view', self.filename)
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

    def create_progress_window(self, filename):
        def create():
            frame = ctk.CustomFrame(self.inner_frame)
            frame.pack()

            name = ctk.CustomLabel(frame,text=filename,pack=True)
            name.pack()

            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(frame, variable=progress_var, maximum=100)
            progress_bar.pack()

            time_remaining_label = ctk.CustomLabel(frame,font=Styles.fonte_input, text="Tempo restante: Calculando...")
            time_remaining_label.pack()

            speed_label = ctk.CustomLabel(frame,font=Styles.fonte_input, text="Velocidade: Calculando...")
            speed_label.pack()

            self.progress_frames[filename] = {
                'frame': frame,
                'name': name,
                'progress_var': progress_var,
                'time_remaining_label': time_remaining_label.get(),
                'speed_label': speed_label.get(),
                'start_time': None
            }
        threading.Thread(target=create,daemon=True).start()

    def update_progress(self, filename, downloaded_size, total_size):
        frame_data = self.progress_frames[filename]
        progress_percent = (downloaded_size / total_size) * 100
        frame_data['progress_var'].set(progress_percent)

        if frame_data['start_time'] is None:
            frame_data['start_time'] = time.time()
        else:
            if progress_percent >= 99:
                frame_data['time_remaining_label'].configure(text=f"Concluído")
                frame_data['progress_var'].set(100)
                frame_data['speed_label'].pack_forget()
                frame_data['frame'].update()
                return
            elapsed_time = time.time() - frame_data['start_time']
            remaining_time = (elapsed_time / progress_percent) * (100 - progress_percent) if progress_percent > 0 else 0
            frame_data['time_remaining_label'].configure(text=f"Tempo restante: {time.strftime('%H:%M:%S', time.gmtime(remaining_time))}")

            speed = downloaded_size / elapsed_time
            frame_data['speed_label'].configure(text=f"Velocidade: {self.format_size(speed)}")

        frame_data['frame'].after(100, lambda: frame_data['frame'].update_idletasks()) 

    def mark_error(self, filename):
        frame_data = self.progress_frames[filename]
        frame_data['frame'].configure(bg='red')
    
    def download_file(self, file_id, chunk_size=8192):
        self.url = f'https://drive.usercontent.google.com/download?id={file_id}&export=download&authuser=0'
        download_link, filename = self.get_download_link_and_filename()
        if not download_link or not filename:
            print(f"Não foi possivel encontrar um download válido para o ID: {file_id}")
            self.mark_error(filename)
            return

        if download_link:
            folderpath = os.path.join(self.extract_folder_path, self.extract_folder_name)
            os.makedirs(folderpath, exist_ok=True)
            filepath = os.path.join(folderpath, filename)

            self.create_progress_window(filename)

            response = requests.get(download_link, stream=True, allow_redirects=True)
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            def update(): 
                self.update_progress(filename, downloaded_size, total_size)
                if downloaded_size >= total_size:
                    print(f"{filename} baixado com sucesso!")
                    return            
                self.root.after(300, update)
                
            update()
            
            with open(filepath, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    try:
                        size = file.write(data)
                        downloaded_size += size
                    except Exception as e:
                        print(f"Erro durante o download de {filename}: {e}")
                        self.mark_error(filename)
                        break
        else:
            self.mark_error(filename)
            print(f"Erro: Não foi possível encontrar o link de download para o arquivo com ID: {file_id}")
            
    def format_size(self, size):
        if size >= 1024**3:  # GB
            return f"{size / (1024**3):.2f} GB"
        elif size >= 1024**2:  # MB
            return f"{size / (1024**2):.2f} MB"
        elif size >= 1024:  # KB
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size:.2f} bytes"
            
