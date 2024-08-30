import customtkinter

# if Interface.var.get() == "on":
#     cor_fundo = "#393939"  
#     cor_texto = "white"  
#     cor_checkbox = "white"  
#     cor_barra = "green"
#     cor_ativo = "#0548E6"
#     fonte_texto = ("Helvetica", 12, "bold")
#     fonte_titulo = ("Helvetica", 20, "bold")
#     cor_botao = None
# else:
cor_fundo = "#030637"  
cor_texto = "white"  
cor_checkbox = "white"  
cor_barra = "green"
cor_ativo = "#4B70F5"
cor_botao = "#4C3BCF"
fonte_texto = ("Helvetica", 12, "bold")
fonte_titulo = ("Helvetica", 20, "bold")
fonte_input = ("Inter",14)



janela_cor_fundo = ""

def DefiniEstilo(ttk):
    # Fonte Futurista
    

    style = ttk.Style()
    style.theme_use('clam')  # Você pode escolher outro tema base, como 'default' ou 'alt'
    # Estilo para Checkbutton
    style.configure("TCheckbutton", background=cor_fundo, foreground=cor_checkbox, font=fonte_texto)
    style.map("TCheckbutton", foreground=[("active", cor_checkbox)], background=[("active", cor_ativo)])

    # Estilo para Label (texto)
    style.configure("TLabel", background=cor_fundo, foreground=cor_texto, font=fonte_texto)

    # Estilo para Button
    style.configure("TButton", foreground=cor_fundo, font=fonte_texto)
    style.map("TButton", foreground=[("active", cor_checkbox)], background=[("active", cor_ativo)])

    style.configure("Custom.TFrame", background=cor_fundo, foreground=cor_fundo)

   
    style.configure("CustomLabel.TLabel", foreground=cor_texto, background=cor_fundo, font=("Helvetica", "11"))


    style.configure("Horizontal.TProgressbar", background=cor_barra, troughcolor=cor_fundo)