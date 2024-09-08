import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
from Util import Util
from Models.LimparCache import Limpeza
from Models.ProcurarAssets import ImagensPixababy

class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1250x800")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        #self.root.bind("<Unmap>", self.on_minimize)

        self.isHided = False

        self.tray_icon = None
        self.tray_thread = threading.Thread(target=self.create_tray_icon, daemon=True)
        self.tray_thread.start()
        self.mini_window = None
        self.mini_window_visible = False        

    def on_closing(self):
      try:
          if self.isHided:
              if self.tray_icon:
                self.tray_icon.stop()
              self.root.destroy()
              return
          resposta = messagebox.askyesno(title="Rodar em segundo plano",message="Deseja rodar em segundo plano?") 
          if resposta == True:    
              messagebox.showinfo("Aviso","S_Videos rodando em segundo plano.\nAcesse pela bandeja de icones.")   
              self.hide_window()
              if self.tray_icon:
                self.tray_icon.visible = True
          else:        
            if self.tray_icon:
                self.tray_icon.stop()
            self.root.destroy()
      except Exception as e:
            print(f"Erro ao fechar") 

    def on_minimize(self, event):
        if self.root.state() == 'iconic':
            self.hide_window()

    def hide_window(self):
        self.isHided = True
        self.root.withdraw()

    def show_window(self, icon=None, item=None):
        self.root.deiconify()
        self.root.state('zoomed')
        self.isHided = False
        if self.tray_icon:
            self.tray_icon.visible = False
    def on_tray_icon_click(self, icon, item):
        self.show_window(icon, item)
        
    def create_tray_icon(self):
        image = Image.open(Util.pegarImagem("icon.ico"))
        menu = pystray.Menu(
            item('Mostrar', self.show_window),
            item('Limpar cache', Limpeza.iniciar_limpeza),
            item('Buscar imagens', ImagensPixababy.abrirInterface),
            #item('Mostrar mini janela', self.show_mini_window),
            #item('Esconder mini janela', self.hide_mini_window),
            item('Fechar', self.on_closing)
        )
        self.tray_icon = pystray.Icon("test_icon", image, "S_Videos", menu)

        # Configure o callback para o clique no ícone da bandeja
        self.tray_icon.run_detached()
        def on_click(icon, item):
            self.show_window(icon, item)

        self.tray_icon._run = self.tray_icon.run
        def new_run():
            self.tray_icon._run(on_click=on_click)
        self.tray_icon.run = new_run        

    def show_mini_window(self):
        if not self.mini_window_visible:
            self.mini_window = tk.Toplevel()
            self.mini_window.overrideredirect(True)  # Remove a moldura padrão da janela
            self.mini_window.geometry("200x100")
            self.mini_window.configure(background='white')

            # Obter a altura da barra de tarefas
            screen_height = self.root.winfo_screenheight()
            taskbar_height = screen_height - self.root.winfo_height()

            # Posicionar a janela no canto inferior direito, acima da barra de tarefas
            self.mini_window.geometry("+{}+{}".format(
                self.root.winfo_screenwidth() - self.mini_window.winfo_width(),
                screen_height - self.mini_window.winfo_height() - taskbar_height
            ))

            label = ttk.Label(self.mini_window, text="Mini Janela")
            label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            self.mini_window_visible = True

    def hide_mini_window(self):
        if self.mini_window_visible:
            self.mini_window.destroy()
            self.mini_window_visible = False
