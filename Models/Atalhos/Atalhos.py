import threading
import keyboard
import Main
from Models.LimparCache import Limpeza
from Util import Util

class TeclasAtalho():
    def __init__(self):
        super().__init__()
        self.ConfigAtalhos = Main.Config
        
    def registrarAtalhos(self):
        for atalhos, teclas in self.ConfigAtalhos.getConfigData("ConfigAtalhos").items():
            comando = None
            if atalhos == "Mostrar": comando = self.Mostrar
            if atalhos == "Esconder": comando = self.Esconder
            if atalhos == "Fechar": comando = self.Fechar
            if atalhos == "BuscarImagens": comando = self.BuscarImagens
            if atalhos == "IniciarLimpeza": comando = self.iniciarlimpeza

            
            
            try:
                if comando is not None and teclas: 
                    keyboard.add_hotkey(teclas.lower(),comando)
                    #print(f"Atalho: {atalhos} registrado com o comando: {teclas}")
                else: print(f"Atalho: {atalhos} não registrado")
            except Exception as e:
                Util.LogError("Atalho",f"Ocorreu um erro ao atribuir o atalho: {atalhos}")            

    
        
        
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



            
            