import threading
import keyboard
from Config import LoadConfigs
from Util import Util
from WebSocket import WebSocket

class TeclasAtalho():
    def __init__(self):
        super().__init__()
        
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

    
        
    def atalhoPremiere(self,atalho):
        global server
        WebSocket.server.sendMessageToAll(atalho)
        
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



            
            