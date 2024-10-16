import asyncio
import threading
import keyboard
import socketio
import websockets
from Config import LoadConfigs
from Util import Util
from PyQt6.QtCore import QThread, pyqtSignal
from WebSocket import WebSocket

class TeclasAtalho():
    def __init__(self):
        super().__init__()
        self.sio = socketio.Client()
    def registrarAtalhos(self):
        atalho = LoadConfigs.Config.getConfigData("ConfigAtalhos")
        if atalho["TeclasDeAtalho"] != True:
            return
        atalho = atalho.items()
        for atalhos, teclas in atalho:
            comando = None
            
            if atalhos == "Geral: Limpar Cache": comando = self.Mostrar
            if atalhos == "Geral: Mostrar": comando = self.Esconder
            if atalhos == "Geral: Esconder": comando = self.Fechar
            if atalhos == "Geral: Fechar": comando = self.Fechar
            
            if atalhos == "Premiere: Vinheta": comando = lambda: self.atalhoPremiere(atalhos)
            if atalhos == "Premiere: Transicao Curta": comando = lambda: self.atalhoPremiere(atalhos)
            if atalhos == "Premiere: Transicao Longa": comando = lambda: self.atalhoPremiere(atalhos)
            if atalhos == "Premiere: Lower Third": comando = lambda: self.atalhoPremiere(atalhos)
            if atalhos == "Premiere: Palavra Chave": comando = lambda: self.atalhoPremiere(atalhos)
            
            try:
                if comando is not None and teclas: 
                    keyboard.add_hotkey(teclas.lower(),comando)
                    print(f"Atalho: {atalhos} registrado com o comando: {teclas}")
                else: print(f"Atalho: {atalhos} não registrado")
            except Exception as e:
                Util.LogError("Atalho",f"Ocorreu um erro ao atribuir o atalho: {atalhos}")                       

    async def send_trigger_to_node(self, trigger):
        uri = "ws://localhost:8081"  # Endereço do servidor WebSocket

        try:
            async with websockets.connect(uri) as websocket:
                await websocket.send("executar_acao")
                print("Gatilho enviado ao Node.js!")
        except Exception as e:
            print(f"Erro ao enviar o gatilho: {e}")
        
    def atalhoPremiere(self, trigger):
        asyncio.run(self.send_trigger_to_node(trigger))
        
    def Mostrar(self):
        return
        InterfaceMain.Bandeja.show_window() 
    def Esconder(self):
        return
        InterfaceMain.Bandeja.on_closing()     
    def Fechar(self):
        return
        InterfaceMain.root.destroy()       
    def iniciarlimpeza(self):
        #print("Atalho iniciar limpeza")
        return
        thread = threading.Thread(target=Limpeza.iniciar_limpeza)
        thread.daemon = True
        thread.start()  

       
class WebSocketServer(QThread):
    trigger_received = pyqtSignal(str)

    async def handler(self, websocket, path):
        message = await websocket.recv()
        print(f"Mensagem recebida do cliente WebSocket: {message}")
        self.trigger_received.emit(message)  # Emite um sinal quando o trigger é recebido

    async def start_server(self):
        async with websockets.serve(self.handler, "localhost", 8081):
            await asyncio.Future()  # Mantém o servidor rodando

    def run(self):
        # Inicializa o loop do asyncio na thread separada
        print("######### Iniciando servidor WebSocket")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start_server())
