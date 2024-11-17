import json
import os
import jwt
import requests
import yaml
from cryptography.fernet import Fernet
from Util import Util

GITHUB = None
VIMEO = None
AWS_S3 = None

def LoadKeys():
  global GITHUB,VIMEO,PIXABAY,AWS_S3
 #credentials = Credentials()
  try:
    key = "O+k9G/kMiXqcm+FRKGvAWQ=="
    dir = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos")
    tokens = os.path.join(dir,"credentials.json") 
    with open(tokens, 'r') as f:
        encoded_jwt = f.read()  # Lê o token do arquivo
        decoded_jwt = jwt.decode(encoded_jwt, key, algorithms=['HS256'])
    response = requests.post("https://samuka.pythonanywhere.com/login",
                         json=decoded_jwt,
                         timeout=60)
    GITHUB = response.json().get("GITHUB")#credentials.getKeys()["GITHUB"]
    VIMEO = ""#credentials.getKeys()["VIMEO"]
    AWS_S3 = response.json().get("S3")#credentials.getKeys()["S3"]
    return True
  except Exception as e:
    return False
    
  

class Credentialss():
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
        print(e)
        Util.LogError("Tokens","Arquivo tokens.yml não encontrado",dialog=False)
        raise e
    
    def encript(self):
      self.generateKey()
      f = Fernet(self.key)
      
      with open(r"z_KeyEToken\tokens_originais.yml", "r") as arquivo:
          dados_originais = yaml.safe_load(arquivo)
          
      dados_originais = yaml.dump(dados_originais).encode()
      dados_criptografados = f.encrypt(dados_originais)
      
      with open(self.file, "wb") as arquivo:
          arquivo.write(dados_criptografados)
      print("Dados criptografados")
    
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
        print(e)
        Util.LogError("Tokens","Arquivo key.key não encontrado.",dialog=False)
      
    def generateKey(self):
      print("Gerando keys")
      self.key = Fernet.generate_key()
      with open(os.path.join(self.dir,"key.key"), "wb") as arquivo_chave:
          arquivo_chave.write(self.key)