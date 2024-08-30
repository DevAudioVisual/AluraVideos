import re
import tkinter as tk
from tkinter import filedialog
import pyautogui
import cv2
import numpy as np
import tempfile
import os
from PIL import Image, ImageTk
import time
from Util import CustomWidgets

class ScreenshotApp:
    def __init__(self, master):
        self.master = master
        master.title("Selecionador de ROI")

        self.canvas = tk.Canvas(master, width=1280, height=720)
        self.canvas.pack()

        self.frameBotoes = CustomWidgets.CustomFrame(self.master)
        self.frameBotoes.pack()
        
        self.btn_capturar = CustomWidgets.CustomButton(self.frameBotoes, text="Capturar Tela", command=self.capturar_tela)
        self.btn_capturar.pack(side="left",padx=10,pady=10)

        b3 = CustomWidgets.CustomButton(self.frameBotoes, text="Salvar", command=self.salvar_roi_diretorio, state=tk.DISABLED)
        self.btn_salvar_diretorio = b3.getButton()
        b3.pack(side="left",padx=10,pady=10)
        
        b2 = CustomWidgets.CustomButton(self.frameBotoes, text="Enviar ao Gemini", command=self.salvar_roi, state=tk.DISABLED)
        self.btn_salvar = b2.getButton()
        b2.pack(side="left",padx=10,pady=10)


        self.img = None
        self.roi = None
        self.roi_coords = None

        self.zoom_factor = 1.0
        self.image_x = 0
        self.image_y = 0
        self.last_update_time = 0

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Control-B1-Motion>", self.move_image)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<Button-3>", self.reset_roi)

    def capturar_tela(self):
        self.master.withdraw()  # Minimiza a janela
        self.master.focus_force()
        self.master.after(200, self.capturar_apos_restauracao) 

    def restaurar_e_capturar(self):
        self.btn_salvar.configure(state=tk.NORMAL)
        self.btn_salvar_diretorio.configure(state=tk.NORMAL)
        self.master.deiconify()  # Restaura a janela

    def capturar_apos_restauracao(self):
        self.screenshot = pyautogui.screenshot()
        self.img = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_RGB2BGR)
        self.exibir_imagem()
        self.btn_salvar.configure(state=tk.DISABLED)
        self.btn_salvar_diretorio.configure(state=tk.DISABLED)
        self.master.after(50, self.restaurar_e_capturar)

    def exibir_imagem(self):
        if self.img is not None:
            img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)

            new_width = int(img_pil.width * self.zoom_factor)
            new_height = int(img_pil.height * self.zoom_factor)
            img_pil = img_pil.resize((new_width, new_height), Image.BICUBIC)

            self.photo = ImageTk.PhotoImage(img_pil)

            if hasattr(self, 'image_id'):
                self.canvas.delete(self.image_id)

            self.image_id = self.canvas.create_image(self.image_x, self.image_y, anchor=tk.NW, image=self.photo)

    def on_button_press(self, event):
        if hasattr(self, 'rect'):
            self.canvas.delete(self.rect)

        if event.state & 0x0004:  # Verifica se a tecla Ctrl está pressionada
            self.prev_x = event.x
            self.prev_y = event.y
        else:
            self.start_x = event.x
            self.start_y = event.y
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        if hasattr(self, 'rect'):
            self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        if not (event.state & 0x0004):  # Verifica se a tecla Ctrl NÃO está pressionada
            self.end_x = event.x
            self.end_y = event.y

            # Verifica se a seleção da ROI está dentro dos limites da imagem
            if 0 <= self.start_x <= self.canvas.winfo_width() and \
               0 <= self.start_y <= self.canvas.winfo_height() and \
               0 <= self.end_x <= self.canvas.winfo_width() and \
               0 <= self.end_y <= self.canvas.winfo_height():

                self.roi_coords = (self.start_x, self.start_y, self.end_x, self.end_y)

                # Calcula as coordenadas da ROI na imagem original (sem zoom)
                x1, y1, x2, y2 = self.roi_coords
                x1_original = int((x1 - self.image_x) / self.zoom_factor)
                y1_original = int((y1 - self.image_y) / self.zoom_factor)
                x2_original = int((x2 - self.image_x) / self.zoom_factor)
                y2_original = int((y2 - self.image_y) / self.zoom_factor)
                self.original_roi_coords = (x1_original, y1_original, x2_original, y2_original)

    def salvar_roi(self):
        if self.roi_coords:
            # Calcula as coordenadas da ROI na imagem original (sem zoom)
            x1, y1, x2, y2 = self.roi_coords
            x1_original = int((x1 - self.image_x) / self.zoom_factor)
            y1_original = int((y1 - self.image_y) / self.zoom_factor)
            x2_original = int((x2 - self.image_x) / self.zoom_factor)
            y2_original = int((y2 - self.image_y) / self.zoom_factor)

            imagem_a_salvar = self.img[y1_original:y2_original, x1_original:x2_original]
        else:
            imagem_a_salvar = self.img  # Salva a imagem completa se não houver ROI

        with tempfile.TemporaryDirectory() as temp_dir:
            caminho_imagem = os.path.join(temp_dir, 'roi.png')
            cv2.imwrite(caminho_imagem, imagem_a_salvar)
            print(f"Imagem salva em: {caminho_imagem}")

    def salvar_roi_diretorio(self):
        if self.roi_coords:
            # Calcula as coordenadas da ROI na imagem original (sem zoom)
            x1, y1, x2, y2 = self.roi_coords
            x1_original = int((x1 - self.image_x) / self.zoom_factor)
            y1_original = int((y1 - self.image_y) / self.zoom_factor)
            x2_original = int((x2 - self.image_x) / self.zoom_factor)
            y2_original = int((y2 - self.image_y) / self.zoom_factor)

            imagem_a_salvar = self.img[y1_original:y2_original, x1_original:x2_original]
        else:
            imagem_a_salvar = self.img  # Salva a imagem completa se não houver ROI

        diretorio = filedialog.askdirectory()
        if diretorio:
            novo_nome_roi = self.gerar_nome_arquivo_roi(diretorio)
            caminho_imagem = os.path.join(diretorio, novo_nome_roi)
            cv2.imwrite(caminho_imagem, imagem_a_salvar)
            print(f"Imagem salva em: {caminho_imagem}")
    def gerar_nome_arquivo_roi(self,dir):
        arquivos_existentes = os.listdir(dir)
        arquivos_roi = [arquivo for arquivo in arquivos_existentes if arquivo.startswith("roi") and arquivo.endswith(".png")]

        numeros_roi = []
        for arquivo in arquivos_roi:
            match = re.search(r"SV_Screenshot_(\d+)\.png", arquivo)
            if match:
                numeros_roi.append(int(match.group(1)))

        proximo_numero = 1
        if numeros_roi:
            proximo_numero = max(numeros_roi) + 1

        novo_nome = f"SV_Screenshot_{proximo_numero}.png"
        return novo_nome
    def exibir_imagem_processada(self, img_processada):
        img_rgb = cv2.cvtColor(img_processada, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        self.photo = ImageTk.PhotoImage(img_pil)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def reset_roi(self, event):
        if hasattr(self, 'rect'):
            self.canvas.delete(self.rect)
            del self.rect
        self.roi_coords = None
        self.btn_salvar.config(state=tk.DISABLED)
        self.btn_salvar_diretorio.config(state=tk.DISABLED)
        self.zoom_factor = 1.0
        self.image_x = 0
        self.image_y = 0
        self.exibir_imagem()        
    def move_image(self, event):
        if self.img is not None:
            delta_x = event.x - self.prev_x
            delta_y = event.y - self.prev_y
            self.canvas.move(self.image_id, delta_x, delta_y)
            self.image_x += delta_x
            self.image_y += delta_y
            self.prev_x = event.x
            self.prev_y = event.y

            # Atualiza a imagem após um pequeno atraso
            current_time = time.time()
            if current_time - self.last_update_time > 0.05:
                self.exibir_imagem()
                self.last_update_time = current_time

    def zoom(self, event):
        if self.img is not None:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            old_zoom_factor = self.zoom_factor
            if event.delta > 0:
                self.zoom_factor *= 1.5  # Aumenta o fator de zoom para um efeito mais perceptível
            else:
                self.zoom_factor *= 0.8

            scale_factor = self.zoom_factor / old_zoom_factor
            self.image_x = x - (x - self.image_x) * scale_factor
            self.image_y = y - (y - self.image_y) * scale_factor
            self.exibir_imagem()

root = tk.Tk()
app = ScreenshotApp(root)
root.mainloop()