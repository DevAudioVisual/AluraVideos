import sys
import threading
import requests
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QListWidget, QPushButton, QLabel, QHBoxLayout, QListWidgetItem, QMessageBox, QComboBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QByteArray, QBuffer, QIODevice, QThread, pyqtSignal, QRunnable, QThreadPool
from functools import lru_cache

from Util import Util

image_cache = {}
threadpool = QThreadPool()
threadpool.setMaxThreadCount(10)
thumbnail_semaphore = threading.Semaphore(10)


@lru_cache(maxsize=128)
def fetch_image_data(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    return response.content, response.headers.get('Content-Type')


class ImageDownloader(QRunnable):
    def __init__(self, url, asset_widget, is_preview=False):
        super().__init__()
        self.url = url
        self.asset_widget = asset_widget
        self.is_preview = is_preview

    def run(self):
        with thumbnail_semaphore:
            try:
                data, content_type = fetch_image_data(self.url)
                image = QImage.fromData(data)

                if not image.isNull():
                    if not self.is_preview or not content_type.startswith("image/png"):
                        byte_array = QByteArray()
                        buffer = QBuffer(byte_array)
                        buffer.open(QIODevice.WriteOnly)
                        image.save(buffer, "PNG")
                        image.loadFromData(byte_array)

                    pixmap = QPixmap.fromImage(image)

                    if self.is_preview:
                        # Redimensionar apenas a miniatura
                        pixmap = pixmap.scaled(
                            self.asset_widget.image_label.size(), Qt.KeepAspectRatio)

                    self.asset_widget.image_label.setPixmap(pixmap)

                    if hasattr(self.asset_widget, 'loading_label'):
                        self.asset_widget.loading_label.hide()

            except Exception as e:
                Util.LogError("ImagensPixaBaby",
                              f"Erro ao baixar ou exibir imagem: {e}", False)

        # # Indicador de carregamento
        # self.loading_label = QLabel()
        # movie = QMovie("loading.gif")  # Substitua pelo caminho da sua animação de carregamento
        # self.loading_label.setMovie(movie)
        # movie.start()
        # layout.addWidget(self.loading_label)


class AssetItem(QWidget):
    def __init__(self, url, title):
        super().__init__()
        layout = QHBoxLayout()

        # Imagem de pré-visualização
        self.image_label = QLabel()
        self.image_label.setFixedSize(100, 75)
        layout.addWidget(self.image_label)

        # Informações do asset
        info_layout = QVBoxLayout()
        self.title_label = QLabel(title)
        info_layout.addWidget(self.title_label)
        layout.addLayout(info_layout)

        self.setLayout(layout)

        self.url = url  # Usar a URL largeImageURL para a imagem em alta resolução
        self.image_label.setPixmap(QPixmap())  # Placeholder vazio

    def set_image(self, pixmap):
        self.image_label.setPixmap(pixmap.scaled(
            self.image_label.size(), Qt.KeepAspectRatio))

    def set_image_from_data(self, image_data):
        try:
            image = QImage.fromData(image_data)
            pixmap = QPixmap.fromImage(image).scaled(
                self.image_label.size(), Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
        except Exception as e:
            Util.LogError("ImagensPixaBaby",
                          f"Erro ao carregar imagem do cache: {e}", False)


class AssetDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Buscador de imagens")

        layout = QVBoxLayout()

        # Campo de busca e botão de pesquisa
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("O que você deseja buscar?")
        search_layout.addWidget(self.search_bar)
        self.setFixedSize(800, 600)

        self.tipoImagem = QComboBox()
        self.tipoImagem.addItem("Imagens")
        self.tipoImagem.addItem("Vetores")
        self.texto_selecionado = "Imagens"

        def on_combobox_changed(index):
            self.texto_selecionado = self.tipoImagem.itemText(
                index)  # Obter o texto pelo índice

        self.tipoImagem.currentIndexChanged.connect(on_combobox_changed)
        search_layout.addWidget(self.tipoImagem)

        self.Ordem = QComboBox()
        self.Ordem.addItem("popular")
        self.Ordem.addItem("latest")
        self.texto_selecionado_Ordem = "popular"

        def on_combobox_changed_ordem(index):
            self.texto_selecionado_Ordem = self.Ordem.itemText(
                index)  # Obter o texto pelo índice

        self.Ordem.currentIndexChanged.connect(on_combobox_changed_ordem)
        search_layout.addWidget(self.Ordem)

        self.search_button = QPushButton("Pesquisar")
        self.search_button.setCursor(Qt.PointingHandCursor)
        self.search_button.clicked.connect(self.search_assets)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Lista de resultados
        self.asset_list = QListWidget()
        layout.addWidget(self.asset_list)

        # Botão de download
        self.download_button = QPushButton("Baixar")
        self.download_button.setCursor(Qt.PointingHandCursor)
        self.download_button.clicked.connect(self.download_asset)
        layout.addWidget(self.download_button)

        # Botões de paginação
        pagination_layout = QHBoxLayout()
        self.previous_button = QPushButton("Página anterior")
        self.previous_button.setCursor(Qt.PointingHandCursor)
        self.previous_button.setEnabled(False)
        self.previous_button.clicked.connect(self.previous_page)
        pagination_layout.addWidget(self.previous_button)

        self.next_button = QPushButton("Próxima página")
        self.next_button.setCursor(Qt.PointingHandCursor)
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)
        layout.addLayout(pagination_layout)

        self.setStyleSheet("""                           
        QPushButton {
            background-color: #4C3BCF; /* Cor de fundo (azul) */
            color: white; /* Cor do texto (branco) */
            font-family: Helvetica; /* Fonte */
            font-size: 12px; /* Tamanho da fonte */
            border-radius: 5px; /* Bordas arredondadas */
            padding: 10px 20px; /* Espaçamento interno */
        }

        QPushButton:hover {
            background-color: #4B70F5; /* Cor ao passar o mouse (azul mais escuro) */
        }
        
        QComboBox {
            background-color: #4C3BCF; /* Cor de fundo (azul) */
            color: white; /* Cor do texto (branco) */
            font-family: Helvetica; /* Fonte */
            font-size: 12px; /* Tamanho da fonte */
            border-radius: 5px; /* Bordas arredondadas */
            padding: 8px 13px; /* Espaçamento interno */
        }

        QComboBox:hover {
            background-color: #4B70F5; /* Cor ao passar o mouse (azul mais escuro) */
        }
        """)

        self.setLayout(layout)

        self.page = 1
        self.per_page = 30
        self.total_hits = 0
        self.thread = None

        self.image_cache = {}
        self.threadpool = QThreadPool()
        self.search_assets()

    def search_assets(self, _=None):
        if not self.texto_selecionado:
            self.texto_selecionado = "Imagens"
        if self.thread is not None and self.thread.isRunning():
            self.thread.terminate()

        query = self.search_bar.text()
        self.thread = SearchThread(
            query, self.page, self.per_page, self.texto_selecionado, self.texto_selecionado_Ordem)
        self.thread.result_ready.connect(self.update_asset_list)
        self.thread.error_occurred.connect(self.handle_api_error)
        self.thread.start()

    def update_asset_list(self, hits, total_hits):
        self.total_hits = total_hits
        self.asset_list.clear()
        for hit in hits:
            item = QListWidgetItem(self.asset_list)
            # Usa largeImageURL para a imagem completa
            asset_widget = AssetItem(hit["largeImageURL"], hit["tags"])
            item.setSizeHint(asset_widget.sizeHint())
            self.asset_list.addItem(item)
            self.asset_list.setItemWidget(item, asset_widget)

            downloader = ImageDownloader(
                hit["previewURL"], asset_widget, is_preview=True)
            self.threadpool.start(downloader)

        # Atualizar estado dos botões de paginação
        self.previous_button.setEnabled(self.page > 1)
        self.next_button.setEnabled(
            self.page * self.per_page < self.total_hits)

    def handle_api_error(self, error_message):
        Util.LogError("ImagensPixaBaby",
                      f"Erro na API do Pixabay: {error_message}")

    def next_page(self):
        if self.page * self.per_page < self.total_hits:
            self.page += 1
            self.search_assets(self.search_bar.text())

    def previous_page(self):
        if self.page > 1:
            self.page -= 1
            self.search_assets(self.search_bar.text())

    def download_asset(self):
        selected_item = self.asset_list.currentItem()
        if selected_item:
            asset_widget = self.asset_list.itemWidget(selected_item)
            url = asset_widget.url

            # Extrair a extensão do arquivo da URL
            file_extension = os.path.splitext(url)[-1]

            # Nome base do arquivo (sem extensão)
            base_filename = "S_Videos_Assets"  # Substitua por seu nome desejado

            # Caminho para a área de trabalho (Windows)
            desktop_path = os.path.join(os.path.join(
                os.environ['USERPROFILE']), 'Desktop')

            # Contador para verificar se o arquivo já existe
            count = 1
            while True:
                filename = f"{base_filename}{count}{file_extension}"
                filepath = os.path.join(desktop_path, filename)

                # Verificar se o arquivo já existe
                if not os.path.exists(filepath):
                    break
                count += 1

            try:
                response = requests.get(url)
                response.raise_for_status()

                with open(filepath, 'wb') as f:
                    f.write(response.content)

                print(f"Imagem baixada com sucesso em: {filepath}")
                QMessageBox.information(
                    self, "Download Concluído", f"Imagem baixada com sucesso em:\n {filepath}")
            except requests.exceptions.RequestException as e:
                Util.LogError("ImagensPixaBaby",
                              f"Erro ao baixar a imagem: {e}")


class SearchThread(QThread):
    result_ready = pyqtSignal(list, int)
    error_occurred = pyqtSignal(str)

    def __init__(self, query, page, per_page, tipo, ordem):
        super().__init__()
        self.query = query
        self.page = page
        self.per_page = per_page
        self.tipo = tipo
        self.ordem = ordem

    def run(self):
        api_key = "26537515-16c067bfaadb70328236cbcad"
        if self.tipo == "Vetores":
            url = f"https://pixabay.com/api/?key={api_key}&q={self.query}&image_type=vector&order={
                self.ordem}&page={self.page}&per_page={self.per_page}"
        else:
            url = f"https://pixabay.com/api/?key={api_key}&q={self.query}&image_type=photo&order={
                self.ordem}&page={self.page}&per_page={self.per_page}"
        response = requests.get(url)

        if response.status_code != 200:
            self.error_occurred.emit(response.json()['error'])
            return

        data = response.json()
        hits = data.get("hits", [])  # Obter os hits com segurança
        total_hits = data.get("totalHits", 0)
        self.result_ready.emit(hits, total_hits)


def abrirInterface():
    """Abre a interface AssetDownloader em uma thread separada."""
    def run_app():
        app = QApplication(sys.argv)
        window = AssetDownloader()
        window.show()
        # Importante: Remover 'sys.exit(app.exec_())' para que o Tkinter não feche
        app.exec_()
    run_app()
    # thread = threading.Thread(target=run_app)
    # thread.daemon = True
    # thread.start()