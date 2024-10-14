import os
import shutil
import sys
import webbrowser
from PyQt6.QtWidgets import QListWidget, QWidget, QVBoxLayout,QPushButton, QLabel, QFileDialog, QSizePolicy
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl,Qt,QCoreApplication,QProcess

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(10, 10, 10, 10)
        
        h1 = QLabel(f"{os.getlogin()}, seja bem vindo(a) ao AluraVideos!")
        h1.setObjectName("grande")
        h1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layoutPrincipal = QVBoxLayout()
        layoutPrincipal.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layoutPrincipal.addWidget(h1)
        
        self.dir = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos")
        tokens = os.path.join(self.dir,"tokens.yml")
        key = os.path.join(self.dir,"key.key")
        
        arquivos_inexistentes = []
        arquivos = [tokens, key]
        for arquivo in arquivos:
            if not os.path.exists(arquivo):
                arquivos_inexistentes.append(arquivo)
        
        if arquivos_inexistentes:
            h2 = QLabel(f"<font color='red'>Você não está autenticado!</font>")
            h2.setObjectName("grande")
            h2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
            self.nome_arquivos = []
            for a in arquivos_inexistentes:
                self.nome_arquivos.append(os.path.basename(a))
            h3 = QLabel(f"Por favor, busque pelos arquivos de autenticação para acessar completamente a ferramenta.\n\nArquivo(s) de autenticação restante(s): {self.nome_arquivos}")
            h3.setWordWrap(True)
            h3.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
            h3.setObjectName("medio")
            
            botao_buscar = QPushButton("Buscar")
            botao_buscar.clicked.connect(self.buscarEregistrar)
            
            layoutPrincipal.addWidget(h2)
            layoutPrincipal.addWidget(h3)
            layoutPrincipal.addWidget(botao_buscar)
        else:  
            label_desc = QLabel("AluraVideos é um software desenvolvido por Samuel Mariano para o time de AudioVisual da Alura Online. Cujo seu principal objetivo é otimizar e automatizar processos do dia-dia.")
            label_desc.setWordWrap(True)
            label_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_desc.setObjectName("medio-normal")
            
            label_ajuda = QLabel("Precisa de ajuda? Acesse a nossa documentação oficial e obtenha algumas dicas! xD")
            label_ajuda.setWordWrap(True)
            label_ajuda.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_ajuda.setObjectName("medio")
            
            button_ajuda = QPushButton("Acessar documentação")
            button_ajuda.clicked.connect(lambda: webbrowser.open("https://www.notion.so/grupoalura/AluraVideos-8589d6eab57744b7a9ccf4080c0b6bca?pvs=25"))
            
            layoutPrincipal.addWidget(label_desc)
            layoutPrincipal.addWidget(label_ajuda)
            layoutPrincipal.addWidget(button_ajuda)
            #layoutPrincipal.addWidget(VimeoPlayer())
        
        self.setLayout(layoutPrincipal)
    def buscarEregistrar(self):
        filenames, _ = QFileDialog.getOpenFileNames(
                self,
                "Selecione os arquivos",
                "",
                "Arquivos Key e YML (*.key *.yml)"  # Filtro modificado
            )
        if filenames:
            pasta_destino = self.dir

            for filename in filenames:
                try:
                    shutil.copy2(filename, pasta_destino)
                    os.remove(filename)
                    print(f"Arquivo {filename} movido com sucesso!")
                    QCoreApplication.quit()
                    QProcess.startDetached(sys.executable, sys.argv)
                    
                except Exception as e:
                    print(f"Erro ao mover o arquivo {filename}: {e}")

class VimeoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl(f"https://player.vimeo.com/video/1018726974")) 

        with open(r"Assets\styles\style_vimeo_player.css", "r") as f:
             stylesheet = f.read()
        self.setStyleSheet(stylesheet)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        label_video = QLabel("Apresentação e tutorial de uso:")
        label_video.setObjectName("medio")
        label_video.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_video)
        layout.addWidget(self.web_view)
        
        self.chapters_list = QListWidget()
        self.chapters_list.setFlow(QListWidget.Flow.LeftToRight)  # Define o fluxo para horizontal
        self.chapters_list.setMaximumHeight(60)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.chapters_list.setSizePolicy(sizePolicy)
        self.chapters_list.addItem("Apresentação (00:00:00)")
        self.chapters_list.addItem("Criar Projeto (00:00:10)")
        #self.chapters_list.addItem("S3 (00:05:00)")
        #self.chapters_list.addItem("Imagens Pixabay (00:10:00)")
        #self.chapters_list.addItem("Limpar Cache (00:10:00)")
        #self.chapters_list.addItem("Renamer (00:10:00)")
        layout.addWidget(self.chapters_list)

        self.chapters_list.itemClicked.connect(self.set_chapter)
  
        self.setLayout(layout)
        
        self.web_view.loadFinished.connect(self.on_load_finished)
    def on_load_finished(self, ok):
        if ok:
            js_code = """
                const script = document.createElement('script');
                script.src = 'https://player.vimeo.com/api/player.js';
                document.head.appendChild(script);

                script.onload = function() {
                    const iframe = document.querySelector('iframe');
                    const player = new Vimeo.Player(iframe);
                    window.setVimeoTime = function(seconds) {
                        player.setCurrentTime(seconds).then(function(seconds) {
                            // segundos = o tempo real para o qual o player buscou
                        }).catch(function(error) {
                            switch (error.name) {
                                case 'RangeError':
                                    // o tempo era menor que 0 ou maior que a duração do vídeo
                                    break;
                                default:
                                    // algum outro erro ocorreu
                                    break;
                            }
                        });
                    }
                };
            """
            self.web_view.page().runJavaScript(js_code)
              
    def set_chapter(self, item):
        time_str = item.text().split("(")[-1].split(")")[0]
        hours, minutes, seconds = map(int, time_str.split(":"))
        total_seconds = hours * 3600 + minutes * 60 + seconds

        # Chama a função JavaScript para definir o tempo
        js_code = f"window.setVimeoTime({total_seconds});"
        self.web_view.page().runJavaScript(js_code)