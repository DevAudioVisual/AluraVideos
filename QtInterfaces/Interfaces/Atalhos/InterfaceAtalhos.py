from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QSizePolicy
)

from Config import LoadConfigs
class KeyLineEdit(QLineEdit):
    def __init__(self, linha, parent=None):
        super().__init__(parent)
        self.linha = linha
        self.setReadOnly(True)

    def keyPressEvent(self, event):
        keys = []
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            keys.append("Ctrl")
        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            keys.append("Shift")
        if event.modifiers() & Qt.KeyboardModifier.AltModifier:
            keys.append("Alt")

        key_name = QApplication.translate(
            "QWidget",
            QKeySequence(event.key()).toString(
                QKeySequence.SequenceFormat.NativeText
            ),
        )
        if key_name:
            keys.append(key_name)

        self.setText("+".join(keys))


class Interface(QWidget):
    def __init__(self):
        super().__init__()

        funcoes = LoadConfigs.Config.getConfigData("ConfigAtalhos")

        self.setWindowTitle("Mapeamento de Funções e Teclas")
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.layout.setContentsMargins(10, 20, 10, 10)

        self.tabela = QTableWidget(len(funcoes), 2)
        self.tabela.setHorizontalHeaderLabels(["Função", "Teclas"])

        #for i, funcao in enumerate(sorted(funcoes)):
        for i, funcao in enumerate(funcoes):
          tecla = funcoes[funcao]
          item_funcao = QTableWidgetItem(funcao)
          self.tabela.setItem(i, 0, item_funcao)

          line_edit = KeyLineEdit(i)  # Usar a subclasse KeyLineEdit
          line_edit.setText(f"{tecla}")
          self.tabela.setCellWidget(i, 1, line_edit)

        self.tabela.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tabela.resizeColumnsToContents()  # Ajusta o tamanho das colunas
        self.tabela.resizeRowsToContents()

        self.layout.addWidget(self.tabela)
        self.setLayout(self.layout)