import os
import re
import time
import Util.CustomWidgets as cw
from Util import Util

def Renomear(pasta,entrada_videos,campo_formato,campo_id,campo_sufixo):
        erro = False
        for arquivo_original, entrada_nome in entrada_videos.items():
            novo_nome = entrada_nome.text()
            if novo_nome:
                nome_sem_extensao, extensao = os.path.splitext(arquivo_original)
                
                numero_aula_regex = r"(\d+\.\d+)"
                match = re.search(numero_aula_regex, nome_sem_extensao)
                if match:
                    numero_aula = match.group(1)
                else:
                    numero_aula = ""
                
                novo_nome_arquivo = (campo_formato
                                     .replace("{id}",campo_id)
                                     .replace("{aula}",numero_aula)
                                     .replace("{titulo}",novo_nome)
                                     .replace("-{sufixo}", f"-{campo_sufixo}" if campo_sufixo != "" else ""))
                print(novo_nome_arquivo)
                novo_nome_arquivo = Util.remover_extensao(novo_nome_arquivo)
                novo_nome_arquivo = str(novo_nome_arquivo) + str(extensao)
                print(novo_nome_arquivo)
                
                caminho_antigo = os.path.join(pasta, arquivo_original)
                caminho_novo = os.path.join(pasta, novo_nome_arquivo)
                
                MAX_TENTATIVAS = 2
                TEMPO_ESPERA = 1

                for tentativa in range(MAX_TENTATIVAS):
                    try:
                        os.rename(os.path.normpath(caminho_antigo), os.path.normpath(caminho_novo))
                        break  
                    except PermissionError as e:
                        if tentativa < MAX_TENTATIVAS - 1:
                            print(f"Tentativa {tentativa + 1} falhou. Aguardando {TEMPO_ESPERA} segundos...")
                            time.sleep(TEMPO_ESPERA)
                        else:
                            erro = True
                            Util.LogError("RenamerSheets",f"Erro: Não foi possível renomear o arquivo {caminho_antigo} após {MAX_TENTATIVAS} tentativas. {e}")
        if erro == False:
            print("Sucesso!")
            cw.MessageBox.information(None,"Sucesso","Arquivos renomeados com sucesso!")
        else:
            print("Erro")
            #Util.LogError("RenamerSheets",f"Erro ao renomear o arquivo {caminho_antigo}")