import threading
import tkinter as tk
from tkinter import ttk
import Models.LimparCache.Limpeza as LimparCache
import Util.Styles as Styles
import Main
import Util.CustomWidgets as CustomWidgets


def interfaceLimparCache(tabview):
    linha = 0

    frame = CustomWidgets.CustomFrame(tabview.tab("Limpar Cache"))
    frame.pack(pady=5)

    tabview.tab("Limpar Cache").rowconfigure(0, weight=1)
    tabview.tab("Limpar Cache").rowconfigure(1, weight=1)
    tabview.tab("Limpar Cache").rowconfigure(2, weight=1)
    tabview.tab("Limpar Cache").rowconfigure(3, weight=1)
    tabview.tab("Limpar Cache").columnconfigure(0, weight=1)
    tabview.tab("Limpar Cache").columnconfigure(1, weight=0)

    CustomWidgets.CustomLabel(frame, text="Pastas para limpar:",
                              dica="Selecione quais pastas deseja limpar.", font=Styles.fonte_titulo, pack=True).pack(pady=10)
    linha += 1

    def update_selected_keys(key):
        if checkbox_vars[key].get():
            selected_keys.add(key)
        else:
            selected_keys.discard(key)

        print("Chaves selecionadas:", selected_keys)

    global selected_keys
    global checkbox_vars
    checkbox_vars = {}
    selected_keys = set()
    Pastas = Main.Config.getDataFrame("ConfigCache")
    for key, criar in Pastas['Pastas'].iloc[0].items():
        check_var = tk.BooleanVar(value=criar)
        checkbox_vars[key] = check_var
        if (criar == True):
            selected_keys.add(key)
        if (key == "PorcentoTemp"):
            keyFilter = "%temp%"
        else:
            keyFilter = key

        CustomWidgets.CustomCheckBox(frame, text=keyFilter, variable=check_var,
                                     command=lambda k=key: update_selected_keys(k), pack=True).pack(pady=5, anchor="w")

        linha += 1

    global progress_bar
    progress_bar = ttk.Progressbar(
        frame, orient="horizontal", length=400, mode="determinate", style="Horizontal.TProgressbar")
    progress_bar.pack(pady=20)
    linha += 1

    def iniciarlimpeza():
        thread = threading.Thread(target=LimparCache.iniciar_limpeza)
        thread.daemon = True
        thread.start()
    CustomWidgets.CustomButton(frame, text="Limpar", dica="Clique para iniciar o processo de limpeza.",
                               width=400, command=iniciarlimpeza, pack=True).pack()

    return frame
