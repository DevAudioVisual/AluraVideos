import os
import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QListWidget, QLineEdit, QHBoxLayout, QDateEdit, QListWidgetItem, QCheckBox
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QColor


class Interface(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lista de Tarefas")
        self.setGeometry(200, 200, 400, 300)

        # Nome do arquivo para salvar as tarefas
        self.file_name = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos","tarefas.json")

        # Layout principal
        layout = QVBoxLayout()

        # Campo para adicionar nova tarefa
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Digite sua tarefa...")

        # Campo para selecionar data
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())

        # Botão para adicionar tarefa
        self.add_button = QPushButton("Adicionar Tarefa")
        self.add_button.clicked.connect(self.add_task)

        # Lista de tarefas
        self.task_list = QListWidget()
        self.task_list.itemDoubleClicked.connect(self.edit_task)

        # Atalhos de teclado
        self.task_list.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.concluir_action = self.task_list.addAction("Concluir Tarefa")
        self.concluir_action.triggered.connect(self.remove_task)
        self.delete_action = self.task_list.addAction("Remover Tarefa")
        self.delete_action.triggered.connect(self.remove_task)

        # Botão para concluir tarefa
        self.complete_button = QPushButton("Concluir Tarefa")
        self.complete_button.clicked.connect(self.complete_task)

        # Layout para os campos de entrada
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.date_input)
        input_layout.addWidget(self.add_button)

        # Adicionando widgets ao layout principal
        layout.addLayout(input_layout)
        layout.addWidget(self.task_list)
        layout.addWidget(self.complete_button)

        # Armazenamento interno das tarefas como uma lista de tuplas (tarefa, data, status)
        self.tasks = []
        self.current_edit_index = None  # Para armazenar o índice da tarefa que está sendo editada

        # Carregar tarefas do arquivo ao iniciar o programa
        self.load_tasks_from_file()

        # Atualiza a exibição inicial
        self.sort_and_display_tasks()

        self.setLayout(layout)

        # Conectar tecla Delete para remover tarefa
        self.task_list.keyPressEvent = self.handle_keypress

    def handle_keypress(self, event):
        """Lida com eventos de tecla pressionada para remover tarefas."""
        if event.key() == Qt.Key.Key_Delete:
            self.remove_task()
        else:
            super().keyPressEvent(event)

    def add_task(self):
        """Adiciona uma nova tarefa à lista."""
        task_text = self.task_input.text()
        task_date = self.date_input.date()

        if task_text:
            if self.current_edit_index is not None:
                # Atualizar a tarefa existente
                self.tasks[self.current_edit_index] = (task_text, task_date, "Pendente")
                self.current_edit_index = None  # Resetar o índice após edição
                self.add_button.setText("Adicionar Tarefa")  # Voltar ao texto original
            else:
                # Adicionar a nova tarefa à lista
                self.tasks.append((task_text, task_date, "Pendente"))

            self.task_input.clear()
            self.sort_and_display_tasks()
            self.save_tasks_to_file()

    def edit_task(self, item):
        """Edita a tarefa selecionada ao dar um duplo clique."""
        selected_index = self.task_list.row(item)
        task_text, task_date, status = self.tasks[selected_index]

        # Preencher os campos com os dados da tarefa
        self.task_input.setText(task_text)
        self.date_input.setDate(task_date)

        # Armazenar o índice da tarefa que está sendo editada
        self.current_edit_index = selected_index
        self.add_button.setText("Atualizar Tarefa")  # Muda o texto para "Atual"

    def sort_and_display_tasks(self):
        """Ordena as tarefas por data e exibe com o status apropriado."""
        # Limpar a lista de tarefas na interface
        self.task_list.clear()

        # Data atual para comparação
        current_date = QDate.currentDate()

        # Separar as tarefas pendentes e concluídas
        pending_tasks = [task for task in self.tasks if task[2] != "Concluído"]
        completed_tasks = [task for task in self.tasks if task[2] == "Concluído"]

        # Ordenar as tarefas pendentes pela data
        pending_tasks.sort(key=lambda task: task[1])

        # Adicionar cada tarefa pendente à lista
        for task_text, task_date, status in pending_tasks:
            if task_date < current_date:
                display_status = "Atrasado"
                color = QColor("red")
            elif task_date == current_date:
                display_status = "Atual"
                color = QColor("green")
            else:
                display_status = "Futura"
                color = QColor("blue")

            task_display = f"{task_date.toString('dd/MM/yyyy')} ({display_status}): {task_text}"
            task_item = QListWidgetItem(task_display)

            # Definir a cor com base no status da data
            task_item.setForeground(color)

            # Adicionar uma caixa de seleção
            #check_box = QCheckBox()
            #check_box.stateChanged.connect(self.update_task_status)
            #self.task_list.addItem(task_item)
            #self.task_list.setItemWidget(task_item, check_box)

            # Armazenar o status da tarefa no QListWidgetItem
            task_item.setData(Qt.ItemDataRole.UserRole, status)

            # Adicionar o item à lista de tarefas
            self.task_list.addItem(task_item)

        # Adicionar cada tarefa concluída no final da lista
        for task_text, task_date, status in completed_tasks:
            task_display = f"{task_date.toString('dd/MM/yyyy')} (Concluído): {task_text}"
            task_item = QListWidgetItem(task_display)

            # Definir a cor para indicar que está concluída
            task_item.setForeground(QColor("gray"))

            # Adicionar uma caixa de seleção
            # check_box = QCheckBox()
            # check_box.setChecked(True)  # Marcar como concluído
            # self.task_list.addItem(task_item)
            # self.task_list.setItemWidget(task_item, check_box)

            # Armazenar o status da tarefa no QListWidgetItem
            task_item.setData(Qt.ItemDataRole.UserRole, status)

            # Adicionar o item à lista de tarefas
            self.task_list.addItem(task_item)

    def update_task_status(self):
        """Atualiza o status da tarefa com base na caixa de seleção."""
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            check_box = self.task_list.itemWidget(item)
            if check_box.isChecked():
                task_text, task_date, _ = self.tasks[i]
                self.tasks[i] = (task_text, task_date, "Concluído")
            else:
                task_text, task_date, _ = self.tasks[i]
                self.tasks[i] = (task_text, task_date, "Pendente")

        # Atualizar a exibição
        self.sort_and_display_tasks()
        # Salvar as mudanças no arquivo
        self.save_tasks_to_file()

    def complete_task(self):
        """Marca a tarefa selecionada como concluída e a move para o final da lista."""
        selected_item = self.task_list.currentItem()
        if selected_item:
            selected_index = self.task_list.row(selected_item)  
            # Alterar o status da tarefa para "Concluído"
            task_text, task_date, status = self.tasks[selected_index]
            self.tasks[selected_index] = (task_text, task_date, "Concluído")

            # Atualizar a exibição
            self.sort_and_display_tasks()
            # Salvar as mudanças no arquivo
            self.save_tasks_to_file()

    def remove_task(self):
        """Remove a tarefa selecionada da lista e do arquivo."""
        selected_item = self.task_list.currentItem()
        if selected_item:
            # Obter o índice da tarefa a partir do texto do item
            selected_index = self.task_list.row(selected_item)

            # Remover a tarefa da lista interna
            del self.tasks[selected_index]

            # Atualizar a exibição
            self.sort_and_display_tasks()

            # Salvar as mudanças no arquivo
            self.save_tasks_to_file()

    def save_tasks_to_file(self):
        """Salva as tarefas em um arquivo JSON."""
        task_data = [
            {"task": task_text, "date": task_date.toString("yyyy-MM-dd"), "status": status}
            for task_text, task_date, status in self.tasks
        ]
        with open(self.file_name, "w") as file:
            json.dump(task_data, file, indent=4)

    def load_tasks_from_file(self):
        """Carrega as tarefas do arquivo JSON ao iniciar o programa."""
        try:
            with open(self.file_name, "r") as file:
                task_data = json.load(file)
                for task in task_data:
                    task_text = task["task"]
                    task_date = QDate.fromString(task["date"], "yyyy-MM-dd")
                    status = task.get("status", "Pendente")
                    self.tasks.append((task_text, task_date, status))

                # Exibir as tarefas carregadas
                self.sort_and_display_tasks()
        except FileNotFoundError:
            pass