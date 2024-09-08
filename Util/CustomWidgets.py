import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import Util.Styles as Styles
from PIL import Image
import Util.Util as Util
from CTkListbox import *
from ttkwidgets.autocomplete import AutocompleteEntryListbox


class CustomSegmentedButton(ttk.Frame):
    def __init__(self, master=None, values=[], segemented_button_var=None, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(style="Custom.TFrame")
        self.segemented_button = ctk.CTkSegmentedButton(master=master,
                                                        values=values,
                                                        variable=segemented_button_var,
                                                        bg_color=Styles.cor_fundo,
                                                        command=command,
                                                        dynamic_resizing=True,
                                                        font=Styles.fonte_input,
                                                        selected_color=Styles.cor_botao,
                                                        selected_hover_color=Styles.cor_ativo,
                                                        unselected_hover_color=Styles.cor_ativo,
                                                        text_color="white",
                                                        corner_radius=10)
        self.segemented_button.pack()

    def getSegmentedButton(self):
        return self.SegmentedButton


class CustomList(ttk.Frame):
    def __init__(self, master=None, height=50, width=50, completevalues=None, dica=None, pack=False, **kwargs):
        super().__init__(master, **kwargs)

        self.config(style="Custom.TFrame")
        self.listbox = AutocompleteEntryListbox(master,
                                                width=20 if width else None,
                                                height=height if height else None,
                                                completevalues=completevalues,
                                                autohidescrollbar=True,
                                                allow_other_values=False
                                                )
        self.listbox.listbox.config(background=Styles.cor_fundo,
                                    foreground="white",
                                    cursor="hand2",
                                    font=Styles.fonte_texto,
                                    )
        self.listbox.entry.config(font=Styles.fonte_input,
                                  )

        if dica:
            self.tooltip = CustomToolTip(self.listbox, dica)
        if pack:
            self.listbox.pack()
        else:
            self.listbox.grid()

    def getList(self):
        return self.listbox


class CustomToolTip(ctk.CTkToplevel):
    def __init__(self, widget, message):
        super().__init__(widget)
        self.overrideredirect(True)  # Sem bordas
        self.withdraw()  # Esconde inicialmente
        self.config(borderwidth=1)
        self.config(background=Styles.cor_botao)
        self.label = ctk.CTkLabel(self,
                                  text="  "+message,
                                  font=Styles.fonte_input,
                                  bg_color=Styles.cor_botao,
                                  fg_color=Styles.cor_botao,
                                  text_color="white",
                                  text_color_disabled="white"
                                  # image=CustomImage("help.ico",25,25),
                                  # compound="left",
                                  )
        self.label.pack(padx=5, pady=5)

        self.widget = widget
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event):
        x, y = self.widget.winfo_rootx(), self.widget.winfo_rooty()
        self.wm_geometry(f"+{x+25}+{y+25}")  # Posiciona próximo ao widget
        self.deiconify()

    def hide(self, event):
        self.withdraw()


class CustomComboBox(ttk.Frame):
    def __init__(self, master=None, Values=None, variable=None, dica=None, width=100, command=None, textLabel=None, pack=False, state="normal", **kwargs):
        super().__init__(master, **kwargs)

        self.config(style="Custom.TFrame")
        self.ComboBox = ctk.CTkComboBox(self,
                                        variable=variable,
                                        values=Values,
                                        font=Styles.fonte_texto,
                                        bg_color=Styles.cor_fundo,
                                        state=state,
                                        width=width,
                                        text_color=Styles.cor_texto,
                                        button_hover_color=Styles.cor_ativo,
                                        dropdown_hover_color=Styles.cor_ativo,
                                        text_color_disabled=Styles.cor_texto,
                                        command=command)
        if dica:
            self.tooltip = CustomToolTip(self.ComboBox, dica)
        if textLabel != None:
            self.Label = CustomLabel(self, text=textLabel)
            if pack:
                self.Label.pack(side="left", fill="x", expand=True, padx=10)
            else:
                self.Label.grid()
        if pack:
            self.ComboBox.pack(side="left")
        else:
            self.ComboBox.grid()

    def getCombo(self):
        return self.ComboBox


class CustomEntry(ttk.Frame):
    def __init__(self, master=None, textvariable="", border_width=1, border_color="gray", width=0, dica=None, state=None, corner_radius=10, font=Styles.fonte_input, bg_color=Styles.cor_fundo, fg_color="white", text_color="black", pack=False, **kwargs):
        super().__init__(master, **kwargs)

        self.config(style="Custom.TFrame")
        self.Entry = ctk.CTkEntry(self, textvariable=textvariable,
                                  bg_color=Styles.cor_fundo,
                                  fg_color=fg_color,
                                  text_color=text_color,
                                  corner_radius=corner_radius,
                                  width=width,
                                  font=font,
                                  state=state,
                                  border_color=border_color,
                                  border_width=border_width
                                  )
        if dica:
            self.tooltip = CustomToolTip(self.Entry, dica)
        if pack:
            self.Entry.pack(fill="x")
        else:
            self.Entry.grid(sticky="ew")

    def get(self):
        return self.Entry.get()

    def getEntry(self):
        return self.Entry


def CustomImage(Imagem, sizeX, sizeY):
    Imagem = ctk.CTkImage(dark_image=Image.open(Util.pegarImagem(Imagem)),
                          light_image=Image.open(Util.pegarImagem(Imagem)),
                          size=(sizeX, sizeY))
    return Imagem


def CustomTabview(frame):
    return ctk.CTkTabview(frame, bg_color=Styles.cor_fundo,
                          fg_color=Styles.cor_fundo,
                          corner_radius=50,
                          height=1,
                          width=1,
                          anchor="n",
                          segmented_button_fg_color=Styles.cor_fundo,
                          segmented_button_selected_color=Styles.cor_ativo,
                          segmented_button_selected_hover_color=Styles.cor_ativo,
                          segmented_button_unselected_hover_color=Styles.cor_ativo,
                          state="normal")


def CustomScroolabeFrame(frame):

    frame = ctk.CTkScrollableFrame(frame,
                                   bg_color=Styles.cor_fundo,
                                   fg_color=Styles.cor_fundo,
                                   scrollbar_button_color=Styles.cor_botao,
                                   scrollbar_button_hover_color=Styles.cor_ativo,
                                   width=5000,
                                   height=5000,)

    return frame


def CustomFrame(frame):
    return ctk.CTkFrame(frame, bg_color=Styles.cor_fundo, fg_color=Styles.cor_fundo)


def CustomFrameBorda(frame, borderw):
    borda = ctk.CTkFrame(
        frame,
        bg_color=Styles.cor_fundo,
        fg_color=Styles.cor_fundo,
        border_width=borderw,
        border_color="white",
        corner_radius=5,
    )

    return borda


def CustomFrame2(frame):
    frame = ttk.Frame(frame, style="Custom.TFrame")
    return frame


class CustomLabel(ttk.Frame):
    def __init__(self, master=None, text="", font=Styles.fonte_texto, bg_color=Styles.cor_fundo, dica=None, image=None, pack=False, **kwargs):
        super().__init__(master, **kwargs)

        self.config(style="Custom.TFrame")
        self.Label = ctk.CTkLabel(self, text=text,
                                  bg_color=bg_color,
                                  font=font,
                                  image=image,
                                  text_color=Styles.cor_texto,
                                  text_color_disabled=Styles.cor_texto,
                                  fg_color=bg_color)

        if dica:
            self.tooltip = CustomToolTip(self.Label, dica)

        if pack:
            self.Label.pack()
        else:
            self.Label.grid()


class CustomButton(ttk.Frame):
    def __init__(self, master=None, text="", textvariable="", command=None, Image=None, width=100, dica=None, pack=False, background=None, state=tk.NORMAL, **kwargs):
        super().__init__(master, **kwargs)

        self.config(style="Custom.TFrame")
        self.Button = ctk.CTkButton(self,
                                    text=text if text else None,
                                    textvariable=textvariable if textvariable else None,
                                    hover_color=Styles.cor_ativo,
                                    bg_color=Styles.cor_fundo if not background else background,
                                    font=Styles.fonte_texto,
                                    image=Image,
                                    width=width,
                                    text_color=Styles.cor_texto,
                                    text_color_disabled=Styles.cor_texto,
                                    state=state,
                                    fg_color=Styles.cor_botao,
                                    command=command)
        if dica:
            self.tooltip = CustomToolTip(self.Button, dica)
        if pack:
            self.Button.pack()
        else:
            self.Button.grid()

    def getButton(self):
        return self.Button


class CustomCheckBox(ttk.Frame):
    def __init__(self, master=None, text="", variable=None, command=None, dica=None, pack=False, **kwargs):
        super().__init__(master, **kwargs)

        self.config(style="Custom.TFrame")
        self.checkbox = ctk.CTkCheckBox(self, text=text, variable=variable,
                                        bg_color=Styles.cor_fundo,
                                        hover_color=Styles.cor_ativo,
                                        fg_color="green",
                                        command=command,
                                        text_color=Styles.cor_texto,
                                        text_color_disabled=Styles.cor_texto,
                                        font=Styles.fonte_texto)
        if dica:
            self.tooltip = CustomToolTip(self.checkbox, dica)
        if pack:
            self.checkbox.pack()
        else:
            self.checkbox.grid()


class CustomSlider(ttk.Frame):
    def __init__(self, master=None, from_=0, to=100, start=0, sufixo="", dica=None, **kwargs):
        super().__init__(master, **kwargs)

        self.sufixo = sufixo

        self.config(style="Custom.TFrame")  # Aplica o estilo ao Frame
        self.label_var = ctk.StringVar()  # Variável para armazenar o valor do label

        self.label = ttk.Label(
            self, textvariable=self.label_var, style="CustomLabel.TLabel")
        self.label.pack(pady=5)  # Coloca o label acima do slider

        self.scale = ctk.CTkSlider(self, from_=from_, to=to, width=200,
                                   button_hover_color=Styles.cor_ativo,
                                   bg_color=Styles.cor_fundo,
                                   fg_color=Styles.cor_checkbox,
                                   progress_color=Styles.cor_ativo,
                                   button_color=Styles.cor_botao,
                                   button_length=10, corner_radius=10,
                                   command=self.update_label)
        self.scale.set(start)  # Define o valor inicial
        self.scale.pack(fill=tk.X, padx=10, pady=5)

        if dica:
            self.tooltip = CustomToolTip(self.scale, dica)

        # Inicializa o valor do label com o valor inicial do slider
        self.label_var.set(str(start)+" "+self.sufixo)

        self.slider_value = start  # Variável externa para armazenar o valor do slider

    def update_label(self, value):
        self.label_var.set(str(int(float(value)))+" "+self.sufixo)
        # Atualiza a variável externa com o valor do slider
        self.slider_value = int(float(value))
        # print(self.slider_value)

    def get_slider_value(self):
        return int(self.slider_value)


class CustomSliderFloat(ttk.Frame):
    def __init__(self, master=None, from_=0, to=100, start=0, sufixo="", dica=None, **kwargs):
        super().__init__(master, **kwargs)

        self.sufixo = sufixo

        self.config(style="Custom.TFrame")  # Aplica o estilo ao Frame
        self.label_var = ctk.StringVar()  # Variável para armazenar o valor do label

        self.label = ttk.Label(
            self, textvariable=self.label_var, style="CustomLabel.TLabel")
        self.label.pack(pady=5)  # Coloca o label acima do slider

        self.scale = ctk.CTkSlider(self, from_=from_, to=to, width=200,
                                   button_hover_color=Styles.cor_ativo,
                                   bg_color=Styles.cor_fundo,
                                   fg_color=Styles.cor_checkbox,
                                   progress_color=Styles.cor_ativo,
                                   button_color=Styles.cor_botao,
                                   button_length=10, corner_radius=10,
                                   command=self.update_label)
        self.scale.set(start)  # Define o valor inicial
        self.scale.pack(fill=tk.X, padx=10, pady=5)

        if dica:
            self.tooltip = CustomToolTip(self.scale, dica)

        # Inicializa o valor do label com o valor inicial do slider
        self.label_var.set(f"{start:.2f} {self.sufixo}")

        self.slider_value = start  # Variável externa para armazenar o valor do slider

    def update_label(self, value):
        # Formata o valor para duas casas decimais
        formatted_value = f"{float(value):.2f}"
        self.label_var.set(f"{formatted_value} {self.sufixo}")
        # Atualiza a variável externa com o valor do slider
        self.slider_value = float(value)

    def get_slider_value(self):
        return self.slider_value
