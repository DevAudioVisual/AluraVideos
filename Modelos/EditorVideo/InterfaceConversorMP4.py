import customtkinter as ctk
from Modelos.EditorVideo import ConversorVideos
from Util import Styles, CustomWidgets

def interfaceConversorMP4(tabview):
    global input_dir_var,input_dir_var2
    global output_dir_var
    input_dir_var = []
    input_dir_var2 = ctk.StringVar()
    output_dir_var = ctk.StringVar()

    tab = tabview.tab("Video")
    framePrincipal = CustomWidgets.CustomScroolabeFrame(tab)
    
    frameDiretorios = CustomWidgets.CustomFrame2(framePrincipal)
    frameVideos = CustomWidgets.CustomFrame2(framePrincipal)
    frame = CustomWidgets.CustomFrame2(framePrincipal)
    
    frameDiretorios.pack(padx=10,pady=10)
    frameVideos.pack(padx=10,pady=10)
    frame.pack(padx=10,pady=10)


    

    CustomWidgets.CustomLabel(frameDiretorios, text="Arquivos de entrada:",font=Styles.fonte_titulo).pack(fill="both")

    

    frameEntrada = CustomWidgets.CustomFrame(frameDiretorios)
    frameEntrada.pack(pady=10,fill="both")

    CustomWidgets.CustomEntry(frameEntrada, textvariable=input_dir_var2,width=500).pack(side="left")

    CustomWidgets.CustomButton(frameEntrada, text="Buscar",dica="Busque pelos arquivos que deseja converter.",Image=CustomWidgets.CustomImage("folder.png",20,20),command=ConversorVideos.select_input_directory).pack(padx=10,side="right")

    

    CustomWidgets.CustomLabel(frameDiretorios, text="Diretório de saída:",font=Styles.fonte_titulo).pack(fill="both")
    
    frameSaida = CustomWidgets.CustomFrame(frameDiretorios)
    frameSaida.pack(pady=10,fill="both")
    
    CustomWidgets.CustomEntry(frameSaida, textvariable=output_dir_var,width=500).pack(side="left")

    CustomWidgets.CustomButton(frameSaida, text="Buscar",dica="Busque pelo diretório onde deseja que a conversão seja colocada.",Image=CustomWidgets.CustomImage("folder.png",20,20),command=ConversorVideos.select_output_directory).pack(padx=10,side="right")

    frameConverterDePara = CustomWidgets.CustomFrame(frameVideos)
    frameConverterDePara.pack(pady=10,fill="both")

    CustomWidgets.CustomLabel(frameConverterDePara,dica="Qual o formato de origem?", text="Converter de:").pack(side="left",fill="both",expand=True)

    global opcoesFormatosConverterDeVar
    global opcoesFormatosConverterParaVar
    opcoesFormatos = [".mov",".mp4",".mkv"]
    opcoesFormatosConverterDeVar = ctk.StringVar(value=".mov")  # Valor padrão
    CustomWidgets.CustomComboBox(frameConverterDePara,variable=opcoesFormatosConverterDeVar,Values=opcoesFormatos).pack(padx=10,side="left",fill="both",expand=True)
    
    
    CustomWidgets.CustomLabel(frameConverterDePara,dica="Qual o formato desejado?", text="Converter para:").pack(side="left")
    opcoesFormatosConverterParaVar = ctk.StringVar(value=".mp4")  # Valor padrão
    CustomWidgets.CustomComboBox(frameConverterDePara,variable=opcoesFormatosConverterParaVar,Values=opcoesFormatos).pack(padx=10,side="left",fill="both",expand=True)

    

    frameResolucao = CustomWidgets.CustomFrame(frameVideos)
    frameResolucao.pack(pady=10,fill="both")

    CustomWidgets.CustomLabel(frameResolucao,dica="Qual a resolução do vídeo?", text="Resolução").pack(side="left")

    global ResolucaooVar
    Resolucaoopcoes = ["4k", "2k", "1080P", "720P", "480P", "360P", "144P"]
    ResolucaooVar = ctk.StringVar(value="1080P")  # Valor padrão
    CustomWidgets.CustomComboBox(frameResolucao,variable=ResolucaooVar,Values=Resolucaoopcoes).pack(side="left",padx=10)
 

    global UltraWideoVar
    UltraWideoVar = ctk.IntVar()
    CustomWidgets.CustomCheckBox(frameResolucao,text="Ultrawide?",dica="Deseja a proporção ultrawide?\n(Padrão cursos Alura)",variable=UltraWideoVar).pack(side="left")

    

    frameCRF = CustomWidgets.CustomFrame(frameVideos)
    frameCRF.pack(pady=10,fill="both")

    CustomWidgets.CustomLabel(frameCRF,dica="Qual o CRF do vídeo desejado?\nCRF = Qualidade de compressão, quanto menor melhor a qualidade,\nMas também um arquivo mais pesado.", text="CRF do vídeo").pack(side="left",fill="both")

    global SliderCRF
    SliderCRF = CustomWidgets.CustomSlider(frameCRF,from_=1, to=30, start=23,sufixo="CRF's")
    SliderCRF.pack(side="left",fill="both")

    

    frameFPS = CustomWidgets.CustomFrame(frameVideos)
    frameFPS.pack(pady=10,fill="both")

    CustomWidgets.CustomLabel(frameFPS,dica="Qual o FPS desejado para o vídeo?", text="FPS do Vídeo").pack(side="left")
    global SliderFPS
    SliderFPS = CustomWidgets.CustomSlider(frameFPS,from_=20, to=60, start=24,sufixo="FPS")
    SliderFPS.pack(side="left")

    

    frameCompressao = CustomWidgets.CustomFrame(frameVideos)
    frameCompressao.pack(pady=10,fill="both")

    CustomWidgets.CustomLabel(frameCompressao,dica="Qual o preset de compressão usar?\nQuanto mais lento, menor o arquivo de vídeo e maior a qualidade.", text="Preset de compressão").pack(side="left")

    # compressaoopcoes = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"]
        
    global compressaoVar
    compressaoopcoes = ["fast", "medium", "slow"]
    compressaoVar = ctk.StringVar(value="medium")  # Valor padrão
    CustomWidgets.CustomComboBox(frameCompressao,variable=compressaoVar,Values=compressaoopcoes).pack(side="left",padx=10)

    

    frameDecodificador = CustomWidgets.CustomFrame(frameVideos)
    frameDecodificador.pack(pady=10,fill="both")

    CustomWidgets.CustomLabel(frameDecodificador,dica="Qual decodificador usar?\nNVIDIA (CUDA) = Usar sua placa de vídeo, uma conversão mais rápida.\nCPU = Usar seu processador, uma conversão mais lenta com um leve ganho de qualidade.\nDica: Usar CPU apenas para conteúdos com uma qualidade de gravação excepcional.", text="Decodificador").pack(side="left")

    global decodificadorVar
    decodificadoropcoes = ["CPU","NVIDIA (CUDA)"]
    decodificadorVar = ctk.StringVar(value="NVIDIA (CUDA)")  # Valor padrão
    CustomWidgets.CustomComboBox(frameDecodificador,variable=decodificadorVar,Values=decodificadoropcoes).pack(side="left",padx=10)
    
    


    #decodificadorVar,video_fps,video_crf,preset_compressao,ResolucaooVar,formatoDe,formatoPara
    def converter():   
        c = ConversorVideos.Converter(
                                input_dir=input_dir_var,
                                output_dir=output_dir_var.get(),
                                decodificadorVar=decodificadorVar.get(),
                                video_fps=SliderFPS.get_slider_value(),
                                video_crf=SliderCRF.get_slider_value(),
                                preset_compressao=compressaoVar.get(),
                                ResolucaooVar=ResolucaooVar.get(),
                                formatoDe=opcoesFormatosConverterDeVar.get(),
                                formatoPara=opcoesFormatosConverterParaVar.get()
                                )
        c.startCoversao()
    CustomWidgets.CustomButton(frame,text="Converter",dica="Clique para iniciar a conversão.",width=150,command=converter).pack(side="left")
    CustomWidgets.CustomButton(frame,text="Assistir",dica="Em breve.",width=150).pack(side="left",padx=10)
    CustomWidgets.CustomCheckBox(frame,text="Trazer audio do editor de audio",dica="Em breve.").pack(side="left")
    
    return framePrincipal
    