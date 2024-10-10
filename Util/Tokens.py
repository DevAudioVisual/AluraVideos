import os
import yaml
from cryptography.fernet import Fernet
from Util import Util

class Credentials():
    def __init__(self):
        self.key = None
        self.dir = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos")
        self.file = os.path.join(self.dir,"tokens.yml")
    
    def getKeys(self):
      self.loadKey()
      try:
        dados_yaml = self.decript()
        credenciais = yaml.safe_load(dados_yaml)
        return credenciais
      except Exception as e:
        Util.LogError("Tokens","Arquivo tokens.yml não encontrado")
    
    def encript(self):
      self.generateKey()
      f = Fernet(self.key)
      
      with open(r"C:\Users\Samuel\Documents\AluraVideos\tokens_originais.yml", "r") as arquivo:
          dados_originais = yaml.safe_load(arquivo)
          
      dados_originais = yaml.dump(dados_originais).encode()
      dados_criptografados = f.encrypt(dados_originais)
      
      with open(self.file, "wb") as arquivo:
          arquivo.write(dados_criptografados)
    
    def decript(self):
      f = Fernet(self.key)
      with open(self.file, "rb") as arquivo:
          dados_criptografados = arquivo.read()
      dados_originais = f.decrypt(dados_criptografados)
      
      # Salva os dados criptografados
      with open(self.file, "wb") as arquivo:
          arquivo.write(dados_criptografados)
          
      return dados_originais.decode()
    
    def loadKey(self):
      try:
        self.key = open(os.path.join(self.dir,"key.key"), "rb").read()
      except Exception as e:
        Util.LogError("Tokens","Arquivo key.key não encontrado.")
      
    def generateKey(self):
      self.key = Fernet.generate_key()
      with open(os.path.join(self.dir,"key.key"), "wb") as arquivo_chave:
          arquivo_chave.write(self.key)
        

