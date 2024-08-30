import tkinter as tk
import Modelos.Interface.Interface as Interface
from Util import Util
import Util.Styles as Styles 
import Util.CustomWidgets as CustomWidgets
from PIL import Image, ImageTk


def interfaceAjuda():
        JanelaAjuda = tk.Toplevel(Interface.root)
        JanelaAjuda.title("Se apaixonou?")
        JanelaAjuda.configure(bg=Styles.cor_fundo,padx=50,pady=50)
        img = Image.open(Util.pegarImagem("icon.ico"))
        photo = ImageTk.PhotoImage(img)
        JanelaAjuda.iconphoto(True, photo)
        
        # Adiciona widgets na janela toplevel
        Imagem = CustomWidgets.CustomImage("VaiSeApaixonar.png",500,500)
        CustomWidgets.CustomLabel(master=JanelaAjuda, text=None,pack=True,image=Imagem).pack(pady=20)        
        CustomWidgets.CustomButton(master=JanelaAjuda,text="Fechar",command=JanelaAjuda.destroy).pack(pady=10)