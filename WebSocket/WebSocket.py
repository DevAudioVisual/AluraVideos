from PyQt6.QtWebSockets import QWebSocketServer,QWebSocket
from PyQt6.QtNetwork import QHostAddress
from PyQt6.QtCore import QThread
import asyncio
import keyboard
import websockets

async def enviar_mensagem(uri, mensagem):
  """Conecta a um servidor WebSocket, envia uma mensagem e fecha a conexão."""
  async with websockets.connect(uri) as websocket:
    await websocket.send(mensagem)
    print(f"Mensagem enviada: {mensagem}")

    # Opcional: Aguardar uma resposta do servidor
    resposta = await websocket.recv()
    print(f"Resposta recebida: {resposta}")

def startServer():
    websocket_server = WebSocketServer()
    websocket_server.start()
    keyboard.add_hotkey('ctrl+alt+shift+x', lambda: asyncio.run(enviar_mensagem("ws://localhost:8765", "executar_funcao_js")))


class WebSocketServer(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)

    async def handler(self, websocket, path):
        async for message in websocket:
            print(f"Mensagem recebida: {message}")
            await websocket.send(f"Você enviou: {message}")

    def run(self):
        async def main():
            async with websockets.serve(self.handler, "localhost", 8765):
                await asyncio.Future()  # executa para sempre

        asyncio.run(main())