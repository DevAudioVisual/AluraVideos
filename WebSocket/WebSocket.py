from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtNetwork import QTcpServer, QTcpSocket

class WebSocketServerss(QThread):
    message_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.server = QTcpServer()
        self.server.newConnection.connect(self.on_new_connection)

    def on_new_connection(self):
        client_socket = self.server.nextPendingConnection()
        client_socket.readyRead.connect(lambda: self.on_data_received(client_socket))
        client_socket.disconnected.connect(lambda: self.on_client_disconnected(client_socket))

    def on_data_received(self, client_socket: QTcpSocket):
        data = client_socket.readAll().data().decode("utf-8")
        print(f"Mensagem recebida: {data}")
        self.message_received.emit(data)  # Emite o sinal quando uma mensagem é recebida

    def on_client_disconnected(self, client_socket: QTcpSocket):
        print("Cliente desconectado")
        client_socket.deleteLater()

    def run(self):
        if not self.server.listen(port=8081):  # Porta onde o servidor estará ouvindo
            print("Erro ao iniciar o servidor:", self.server.errorString())
        else:
            print("Servidor WebSocket iniciado na porta 8081")