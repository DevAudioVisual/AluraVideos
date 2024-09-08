import threading
import time
from tkinter import messagebox
import webbrowser
import shutil
import os
from Modelos.Interface import Interface
from Modelos.CriarProjeto import Descompactador, BaixarDoDrop, InterfaceCriarProjeto
from Util import TempoVideos,Util



def download_completo(arquivo, tamanho_esperado=None):
    """Verifica se o download do arquivo está completo."""
    tamanho_anterior = 0
    tempo_ultima_alteracao = time.time()

    while True:
        try:
            tamanho_atual = os.path.getsize(arquivo)
        except FileNotFoundError:
            # O arquivo ainda não existe, o download provavelmente não começou
            time.sleep(1)
            continue

        if tamanho_esperado and tamanho_atual >= tamanho_esperado:
            return True  # Download completo se atingiu o tamanho esperado

        if tamanho_atual == tamanho_anterior:
            if time.time() - tempo_ultima_alteracao > 5:  # 5 segundos sem alteração
                return True  # Download completo se o tamanho não muda por 5 segundos
        else:
            tempo_ultima_alteracao = time.time()

        tamanho_anterior = tamanho_atual
        time.sleep(1)

def descompactar(arquivo_zip, diretorio_saida):
    """Descompacta o arquivo, mas só se ele estiver 100% baixado."""

    max_tentativas = 5
    tentativa = 0

    while tentativa < max_tentativas:
        try:
            if not download_completo(arquivo_zip):
                raise Exception("Arquivo ainda não baixado completamente.")

            print("Descompactando...")

            janela, barra_progresso = Descompactador.criar_barra_progresso(
                Interface.root, "Descompactando, aguarde..."
            )

            tamanho_total = os.path.getsize(arquivo_zip)

            # Thread para a extração
            global thread_extracao
            thread_extracao = threading.Thread(
                target=Descompactador.converter_zip_rar,
                args=(
                    arquivo_zip,
                    diretorio_saida,
                    barra_progresso,
                    janela,
                    Descompactador.evento_termino,
                ),
            )
            thread_extracao.daemon = True
            thread_extracao.start()

            # Thread para a barra de progresso
            global thread_barra
            thread_barra = threading.Thread(
                target=Descompactador.atualizar_barra,
                args=(
                    barra_progresso,
                    tamanho_total,
                    diretorio_saida,
                    janela,
                    Descompactador.evento_termino,
                ),
            )
            thread_barra.daemon = True
            thread_barra.start()

            return  # Sai da função se a descompactação for bem-sucedida

        except Exception as e:
            print(f"Erro na descompactação (tentativa {tentativa + 1}): {e}")        
            tentativa += 1
            time.sleep(5)

    # Se todas as tentativas falharem, cancela a ação
    print("Falha na descompactação após várias tentativas. Cancelando a ação.")
    Util.LogError("Descompactar",f"Falha na descompactação após várias tentativas. Cancelando a ação.",True)
    Descompactador.evento_termino.set()
    janela.destroy()
    
def criar_pastas():
    if not InterfaceCriarProjeto.CriarEm.get(): 
        Util.logWarning(None,"Diretório de criação inválido.",False)
        return
        
    PastasCriadas = []
    ArquivoVideos = InterfaceCriarProjeto.ArquivoVideos.get()
    nome_projeto = InterfaceCriarProjeto.nome_projeto_var.get()
    CriarProjetos = True #InterfaceCriarProjeto.criar_arquivos.get()
    CriarSubPastas = True #InterfaceCriarProjeto.criar_pastas.get()
    subpastas_selecionadas = [subpasta for subpasta, var in InterfaceCriarProjeto.subpasta_vars.items() if var.get()]
    Premire = False
    After = False
    destinoPremiere = ""
    destinoAfter = ""
    destinoVideos = ""
    global thread_barra,thread_extracao,thread_baixando
    thread_barra = None;
    thread_extracao = None;
    thread_baixando = None;
    if nome_projeto:
        caminho_pasta_principal = os.path.join(InterfaceCriarProjeto.CriarEm.get(), nome_projeto)
        os.makedirs(caminho_pasta_principal, exist_ok=True)
        print(f"Pasta '{nome_projeto}' criada com sucesso!")
        if CriarSubPastas:
            for subpasta in subpastas_selecionadas:
                caminho_subpasta = os.path.join(caminho_pasta_principal, subpasta)
                os.makedirs(caminho_subpasta, exist_ok=True)
                PastasCriadas.append(subpasta)
                print(f"Subpasta '{subpasta}' criada com sucesso!")
                if subpasta == "01_Bruto":
                    caminho_nova_pasta = caminho_subpasta
                    destinoVideos = caminho_nova_pasta
                if subpasta == "05_AfterEfects": 
                    After = True 
                    caminho_nova_pasta = caminho_subpasta
                    destinoAfter = caminho_nova_pasta
                elif subpasta == "04_Premiere":
                    Premire = True
                    caminho_nova_pasta = caminho_subpasta
                    destinoPremiere = caminho_nova_pasta
        Tempo = None;            
        if ArquivoVideos:
            Tempo = 100
            arquivo_zip = InterfaceCriarProjeto.filepath           
            #arquivo_zip = BaixarDoDrop.url_pasta
            diretorio_saida = destinoVideos
            if Util.is_url(arquivo_zip):
                thread_baixando = threading.Thread(target=BaixarDoDrop.baixar_pasta_dropbox, args=(Interface.root,arquivo_zip,diretorio_saida))
                thread_baixando.daemon = True
                thread_baixando.start()               
            else: descompactar(arquivo_zip,diretorio_saida)              
            
               
        if CriarProjetos:
            criar_Arquivos(destinoPremiere,destinoAfter,Premire,After,nome_projeto)        
            
        def verificar_termino_download():
            if BaixarDoDrop.foi_baixado == True:
                print("############ INICIANDO DESCOMPACTAÇAO")
                arquivo_zip = BaixarDoDrop.caminho_completo_tratado
                Interface.root.after(5000, lambda: descompactar(arquivo_zip,diretorio_saida))           
                Interface.root.after_cancel(verificar_termino_download)
            else: Interface.root.after(1000, verificar_termino_download)       
               
        def verificar_termino():
            if thread_extracao:
                if not thread_extracao.is_alive() and Descompactador.evento_termino.isSet():
                    Tempo = TempoVideos.calcular_duracao_total(destinoVideos)
                    if Tempo: 
                        messagebox.showinfo("Aviso", Mensagem+" \n"+f"Você tem {Tempo} de bruto para edição.")
                        abriroufechar()
                    Interface.root.after_cancel(verificar_termino)
                else:
                    Interface.root.after(1000, verificar_termino)  # Verifica novamente em 100ms
    verificar_termino()
    verificar_termino_download()
    Mensagem = "Projeto: "+nome_projeto+" criado com sucesso!"
    def abriroufechar():    
        if InterfaceCriarProjeto.abrir_premiere.get():
            if Premire:
                webbrowser.open(os.path.join(destinoPremiere, nome_projeto+".prproj"))
        if InterfaceCriarProjeto.abrir_pasta.get():
            Interface.root.after(1000, lambda: webbrowser.open(caminho_pasta_principal)) 
        if InterfaceCriarProjeto.fechar_ao_criar.get():
            Interface.root.after(1000, Interface.root.destroy) 
    if not Tempo: 
        abriroufechar()
        messagebox.showinfo("Aviso", Mensagem)

    

                            
def criar_Arquivos(destino_premiere,destino_after,premiere, after, projeto):
    origem_premiere = Util.pegarTemplate("template.prproj")
    origem_after = Util.pegarTemplate("AE_template.aep")
    
    
    if premiere == True:
        try:
            shutil.copy2(origem_premiere, destino_premiere)
            nome_original = os.path.basename(origem_premiere)
            caminho_novo_arquivo = os.path.join(destino_premiere, nome_original)
            os.rename(caminho_novo_arquivo, os.path.join(destino_premiere, projeto+".prproj"))
            Util.logInfo(None,f"Arquivo e metadados copiados de '{origem_premiere}' para '{destino_premiere}' com sucesso!",False)
                    
        except FileNotFoundError:
            Util.LogError("CriarProjeto",f"Arquivo de origem '{origem_premiere}' não encontrado.")
        except PermissionError:
            Util.LogError("CriarProjeto",f"Permissão negada para copiar para '{destino_premiere}'.")
        except Exception as e:
            Util.LogError("CriarProjeto",f"Erro ao copiar o arquivo: {e}")
    if after == True:
        try:
            shutil.copy2(origem_after, destino_after)
            nome_original = os.path.basename(origem_after)
            caminho_novo_arquivo = os.path.join(destino_after, nome_original)
            os.rename(caminho_novo_arquivo, os.path.join(destino_after, projeto+".aep"))
            print(f"Arquivo e metadados copiados de '{origem_after}' para '{destino_after}' com sucesso!")
        except FileNotFoundError:
            Util.LogError("CriarProjeto",f"Arquivo de origem '{origem_premiere}' não encontrado.")
        except PermissionError:
            Util.LogError("CriarProjeto",f"Permissão negada para copiar para '{destino_premiere}'.")
        except Exception as e:
            Util.LogError("CriarProjeto",f"Erro ao copiar o arquivo: {e}")    
    
            