import time
import webbrowser
import shutil
import os
from Models.CriarProjeto import Descompactador, DropDownloader
from Interfaces.ProjectCreator import InterfaceProjectCreator
from Util import TempoVideos, Util
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QTimer,QCoreApplication
    
class ProjectCreator():
    def __init__(self, ArquivoVideos, nome_projeto_var, subpasta_vars, CriarEm,abrir_pasta,fechar_ao_criar,abrir_premiere, main_window, stackedwidget):
        self.PastasCriadas = []
        self.stackedwidget = stackedwidget
        self.abrir_pasta = abrir_pasta
        self.abrir_premiere = abrir_premiere
        self.fechar_ao_criar = fechar_ao_criar
        self.ArquivoVideos = ArquivoVideos #CriarProjetoInterface.ArquivoVideos.get()
        self.nome_projeto = nome_projeto_var.text() #CriarProjetoInterface.nome_projeto_var.get()
        self.CriarEm = CriarEm
        self.subpasta_vars = subpasta_vars
        self.subpastas_selecionadas = [subpasta for subpasta, var in self.subpasta_vars.items() if var.isChecked()]
        self.Premire = False
        self.After = False
        self.destinoPremiere = ""
        self.destinoAfter = ""
        self.destinoVideos = ""
        self.Tempo = None;       
        self.Downloader = None    
        self.Descompactador = None
        
        self.main_window = main_window
        
        self.Mensagem = "Projeto: "+self.nome_projeto+" criado com sucesso!"
        self.Interface = InterfaceProjectCreator.Interface()
        
    def create(self):
        if not self.CriarEm.text(): 
            Util.logWarning(None,"Diretório de criação inválido.",True)
            return
        if not self.ArquivoVideos.text(): 
            Util.logWarning(None,"Arquivo de vídeos não fornecido.",True)
            return
        
        if self.nome_projeto:
            self.caminho_pasta_principal = os.path.join(self.CriarEm.text(), self.nome_projeto)
            os.makedirs(self.caminho_pasta_principal, exist_ok=True)
            print(f"Pasta '{self.nome_projeto}' criada com sucesso!")
            for subpasta in self.subpastas_selecionadas:
                self.caminho_subpasta = os.path.join(self.caminho_pasta_principal, subpasta)
                os.makedirs(self.caminho_subpasta, exist_ok=True)
                self.PastasCriadas.append(subpasta)
                print(f"Subpasta '{subpasta}' criada com sucesso!")
                if subpasta == "01_Bruto":
                    self.caminho_nova_pasta = self.caminho_subpasta
                    self.destinoVideos = self.caminho_nova_pasta
                if subpasta == "05_AfterEfects": 
                    self.After = True 
                    self.caminho_nova_pasta = self.caminho_subpasta
                    self.destinoAfter = self.caminho_nova_pasta
                elif subpasta == "04_Premiere":
                    self.Premire = True
                    self.caminho_nova_pasta = self.caminho_subpasta
                    self.destinoPremiere = self.caminho_nova_pasta
             
            self.Descompactador = Descompactador.Descompact(projeto=self.nome_projeto)
             
            def verificar_termino_download():
                if self.Downloader and self.Downloader.downloaded == True:
                        print("############ INICIANDO DESCOMPACTAÇAO")
                        self.arquivo_zip = self.Downloader.zip_file
                        QTimer.singleShot(3000, lambda: self.Descompactador.start(arquivo_entrada=self.arquivo_zip,diretorio_saida=self.diretorio_saida, stackedwidget=self.stackedwidget))
                else: 
                    QTimer.singleShot(1000, verificar_termino_download)
                    #InterfaceMain.root.after(1000, verificar_termino_download)       
                
            def verificar_termino():
                if self.Descompactador.descompacted == True:
                    self.Tempo = TempoVideos.calcular_duracao_total(self.destinoVideos)
                    QMessageBox.information(None, "Aviso", self.Mensagem+" \n"+f"Você tem {self.Tempo} de bruto para edição.")
                    #messagebox.showinfo("Aviso", self.Mensagem+" \n"+f"Você tem {self.Tempo} de bruto para edição.")
                    self.abriroufechar()
                else:
                    QTimer.singleShot(1000, verificar_termino)
                    #InterfaceMain.root.after(1000, verificar_termino)  # Verifica novamente em 100ms
            if self.ArquivoVideos:
                self.arquivo_zip = self.ArquivoVideos.text()          
                self.diretorio_saida = self.destinoVideos
                if Util.is_url(self.arquivo_zip):
                    self.Downloader = DropDownloader.DownloadDropApp(url=self.arquivo_zip, extract_folder_path=self.diretorio_saida,stackedwidget=self.stackedwidget,projeto=self.nome_projeto)
                    self.Downloader.startDownload() 
                    #url = self.arquivo_zip
                    #self.Downloader = DropDownloader.DownloadWidget(url,self.diretorio_saida)
                    #self.stackedwidget.addWidget(self.progressdialog)
                    #self.stackedwidget.setCurrentWidget(self.progressdialog)
                    verificar_termino_download()
                    verificar_termino()
                else: 
                    self.Descompactador.start(arquivo_entrada=self.arquivo_zip,diretorio_saida=self.diretorio_saida,stackedwidget=self.stackedwidget)   
                    verificar_termino()     

            self.criar_Arquivos(self.destinoPremiere,self.destinoAfter,self.Premire,self.After,self.nome_projeto)   
                
    def abriroufechar(self):    
        if self.abrir_premiere == True:
            webbrowser.open(os.path.join(self.destinoPremiere, self.nome_projeto+".prproj"))
        if self.abrir_pasta  == True:
            webbrowser.open(self.caminho_pasta_principal)
        if self.fechar_ao_criar  == True:
            QCoreApplication.instance().quit()
    def download_completo(self,arquivo, tamanho_esperado=None):
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
                            
    def criar_Arquivos(self,destino_premiere,destino_after,premiere, after, projeto):
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
    
            