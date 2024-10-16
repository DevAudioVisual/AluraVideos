"""
import asyncio
import threading
import keyboard
import socketio
import websockets
from Config import LoadConfigs
from Util import Util

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


    
"""