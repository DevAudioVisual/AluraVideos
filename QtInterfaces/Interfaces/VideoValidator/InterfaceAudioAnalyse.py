from concurrent.futures import ProcessPoolExecutor
import csv
from PyQt6.QtWidgets import QWidget, QLabel, QSizePolicy, QAbstractItemView, QListWidget, QSlider, QVBoxLayout, QGridLayout,QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor
import Util.CustomWidgets as cw

class InterfaceAudio(QWidget):
    def __init__(self):
        super().__init__() 
        
        """CLASSES DISPONIVEIS"""
        self.campo_busca_tabela = cw.LineEdit(self)
        self.campo_busca_tabela.setPlaceholderText("Buscar...")         
        self.campo_busca_tabela.textChanged.connect(self.filtrar_tabela)
        
        tabela_html = "<span style='font-size: 14pt;'>Classes disponíveis</span><br><span style='font-size: 10pt; margin-top: 5px;'>Clique para ativar<br>shift+clique para desativar</span>"
        self.label_tabela = QLabel(tabela_html)
        self.label_tabela.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_tabela.setObjectName("medio")
        
        self.tabela_itens = TabelaItens(self)
        self.tabela_itens.horizontalHeader().setStretchLastSection(True)
        self.tabela_itens.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) 
        self.tabela_itens.itemClickedWithModifier.connect(self.adicionar_item_selecionado)
        self.tabela_itens.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabela_itens.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.buttonTransferirTodos = cw.PushButton("Transferir todos >>>")
        self.buttonTransferirTodos.clicked.connect(self.transferir_todos_itens)
        
        """CLASSES ATIVADAS"""
        self.campo_busca_lista = cw.LineEdit(self)
        self.campo_busca_lista.setPlaceholderText("Buscar...")         
        self.campo_busca_lista.textChanged.connect(self.filtrar_lista) 
        
        lista_html = "<span style='font-size: 14pt;'>Classes ativadas</span><br><b><span style='font-size: 10pt; margin-top: 5px;'>Clique para remover</span>"
        self.label_lista = QLabel(lista_html)
        self.label_lista.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_lista.setObjectName("medio")
        
        self.lista_selecionados = QListWidget(self)
        self.lista_selecionados.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) 
        self.lista_selecionados.itemClicked.connect(self.remover_item_selecionado) 
        
        self.button_limpar_lista = cw.PushButton("Limpar")
        self.button_limpar_lista.clicked.connect(lambda: self.lista_selecionados.clear())

        """CLASSES DESATIVADAS"""
        self.campo_busca_lista_desativada = cw.LineEdit(self)
        self.campo_busca_lista_desativada.setPlaceholderText("Buscar...")         
        self.campo_busca_lista_desativada.textChanged.connect(self.filtrar_lista_desativada)
        
        lista_desativada_html = "<span style='font-size: 14pt;'>Classes desativadas</span><br><b><span style='font-size: 10pt; margin-top: 5px;'>Clique para remover</span>"
        self.label_lista_desativada = QLabel(lista_desativada_html)
        self.label_lista_desativada.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_lista_desativada.setObjectName("medio")
        
        self.lista_desativada_selecionados = QListWidget(self)
        self.lista_desativada_selecionados.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) 
        self.lista_desativada_selecionados.itemClicked.connect(self.remover_item_selecionado) 
        
        self.button_limpar_lista_desativada = cw.PushButton("Limpar")
        self.button_limpar_lista_desativada.clicked.connect(lambda: self.lista_desativada_selecionados.clear())

        self.slider_limiar = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_limiar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.slider_limiar.setRange(0, 100)  # Define o intervalo de 0 a 100
        self.slider_limiar.setValue(80)  # Define o valor inicial como 0

        # Cria um QLabel para exibir o valor do slider
        self.slider_limiar_label = QLabel("Limiar: 80%", self)
        self.slider_limiar_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.slider_limiar_label.setContentsMargins(0,0,0,0)

        # Conecta o sinal valueChanged do slider ao método que atualiza o label
        self.slider_limiar.valueChanged.connect(self.atualizar_slider_limiar_label)  
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        layoutGrid = QGridLayout()
        layoutGrid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)                  
        
        layoutGrid.addWidget(self.label_tabela,0,0)
        layoutGrid.addWidget(self.campo_busca_tabela,1,0)
        layoutGrid.addWidget(self.tabela_itens,2,0)
        layoutGrid.addWidget(self.buttonTransferirTodos,3,0)
        
        layoutGrid.addWidget(self.label_lista,0,1)
        layoutGrid.addWidget(self.campo_busca_lista,1,1)
        layoutGrid.addWidget(self.lista_selecionados,2,1)
        layoutGrid.addWidget(self.button_limpar_lista,3,1)
        
        layoutGrid.addWidget(self.label_lista_desativada,0,2)
        layoutGrid.addWidget(self.campo_busca_lista_desativada,1,2)
        layoutGrid.addWidget(self.lista_desativada_selecionados,2,2)
        layoutGrid.addWidget(self.button_limpar_lista_desativada,3,2)

        layout.addLayout(layoutGrid)
        layout.addWidget(self.slider_limiar_label)
        layout.addWidget(self.slider_limiar)
        self.setLayout(layout)
        
        self.carregar_csv()
    def getslider_limiar(self):
        return self.slider_limiar
    def atualizar_slider_limiar_label(self, value):
        """Atualiza o label com o valor do slider."""
        self.slider_limiar_label.setText(f"Limiar: {value}%")
    def ordenar_itens(self):
        """Ordena os itens da lista e da tabela em ordem alfabética."""
        self.lista_selecionados.sortItems()
        self.tabela_itens.sortItems(2, order=Qt.SortOrder.AscendingOrder)
        
    def filtrar_lista_desativada(self, texto):
        """Filtra os itens da lista com base no texto fornecido."""
        for i in range(self.lista_desativada_selecionados.count()):
            item = self.lista_desativada_selecionados.item(i)
            if texto.lower() not in item.text().lower():
                self.lista_desativada_selecionados.setRowHidden(i, True)
            else:
                self.lista_desativada_selecionados.setRowHidden(i, False)        
        self.ordenar_itens()
        
    def filtrar_lista(self, texto):
        """Filtra os itens da lista com base no texto fornecido."""
        for i in range(self.lista_selecionados.count()):
            item = self.lista_selecionados.item(i)
            if texto.lower() not in item.text().lower():
                self.lista_selecionados.setRowHidden(i, True)
            else:
                self.lista_selecionados.setRowHidden(i, False)        
        self.ordenar_itens()
                
    def filtrar_tabela(self, texto):
        """Filtra a tabela e a lista com base no texto fornecido."""

        # Filtra a tabela
        for linha in range(self.tabela_itens.rowCount()):
            correspondencia = False
            for coluna in range(self.tabela_itens.columnCount()):
                item = self.tabela_itens.item(linha, coluna)
                if item and texto.lower() in item.text().lower():
                    correspondencia = True
                    break
            self.tabela_itens.setRowHidden(linha, not correspondencia)

        # Filtra a lista
        for i in range(self.lista_selecionados.count()):
            item = self.lista_selecionados.item(i)
            self.lista_selecionados.setRowHidden(i, texto.lower() not in item.text().lower())
        self.ordenar_itens()
        
    def transferir_todos_itens(self):
        """Transfere todos os itens da tabela para a lista."""
        for linha in range(self.tabela_itens.rowCount()):
            # Obtém o texto da terceira coluna (índice 2)
            item_texto = self.tabela_itens.item(linha, 2).text()  
            
            # Verifica se o item já existe na lista
            if not self.lista_selecionados.findItems(item_texto, Qt.MatchFlag.MatchExactly):
                self.lista_selecionados.addItem(item_texto)
        self.ordenar_itens()
     
    def adicionar_item_selecionado(self, item, event):
        linha = item.row()
        coluna3 = self.tabela_itens.item(linha, 2).text()

        if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:  # Verifica se Shift está pressionado
            if not self.lista_desativada_selecionados.findItems(coluna3, Qt.MatchFlag.MatchExactly):
                self.lista_desativada_selecionados.addItem(f"{coluna3}")
                # Remove da lista_selecionados se existir
                itens_correspondentes = self.lista_selecionados.findItems(coluna3, Qt.MatchFlag.MatchExactly)
                if itens_correspondentes:
                    for item_correspondente in itens_correspondentes:
                        self.lista_selecionados.takeItem(self.lista_selecionados.row(item_correspondente))
        else:
            if not self.lista_selecionados.findItems(coluna3, Qt.MatchFlag.MatchExactly):
                self.lista_selecionados.addItem(f"{coluna3}")
                # Remove da lista_desativada_selecionados se existir
                itens_correspondentes = self.lista_desativada_selecionados.findItems(coluna3, Qt.MatchFlag.MatchExactly)
                if itens_correspondentes:
                    for item_correspondente in itens_correspondentes:
                        self.lista_desativada_selecionados.takeItem(self.lista_desativada_selecionados.row(item_correspondente))
        self.ordenar_itens()
        
        
    def remover_item_selecionado(self, item):
        """Remove o item clicado da lista de selecionados."""
        self.lista_selecionados.takeItem(self.lista_selecionados.row(item))
        self.ordenar_itens()
             
    def carregar_csv(self):
        nome_arquivo = r"TensorModels\yamnet_class_map.csv"
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as arquivo_csv:
                leitor_csv = csv.reader(arquivo_csv)

                # Remove o cabeçalho
                next(leitor_csv)

                # Define o número de colunas (todas as colunas do arquivo)
                num_colunas = 3  # Corrigido: Agora lê todas as colunas
                self.tabela_itens.setColumnCount(num_colunas)

                # Insere as linhas, com todas as colunas
                for linha in leitor_csv:
                    linha_atual = self.tabela_itens.rowCount()
                    self.tabela_itens.insertRow(linha_atual)
                    for coluna, item in enumerate(linha):  # Insere todos os itens da linha
                        item_tabela = QTableWidgetItem(item)
                        self.tabela_itens.setItem(linha_atual, coluna, item_tabela)

                # Oculta as colunas 0 e 1 (depois de inserir os dados)
                self.tabela_itens.setColumnHidden(0, True)
                self.tabela_itens.setColumnHidden(1, True)

                # Remove o cabeçalho da tabela
                self.tabela_itens.horizontalHeader().setVisible(False)
            self.ordenar_itens()

        except Exception as e:
            print(f"Erro ao ler o arquivo CSV: {e}")
            
            
class TabelaItens(QTableWidget):
    itemClickedWithModifier = pyqtSignal(object, object)  # Sinal personalizado

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)  # Chama o método original
        if self.itemAt(event.pos()):  # Verifica se clicou em um item
            item = self.itemAt(event.pos())
            self.itemClickedWithModifier.emit(item, event)
            