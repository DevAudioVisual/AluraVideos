import os
import jwt
import requests

GITHUB = None
AWS_S3 = None

def LoadKeys():
  global GITHUB,PIXABAY,AWS_S3
  try:
    key = "O+k9G/kMiXqcm+FRKGvAWQ=="
    dir = os.path.join(os.path.expanduser("~"), "Documents", "AluraVideos")
    tokens = os.path.join(dir,"credentials.json") 
    with open(tokens, 'r') as f:
        encoded_jwt = f.read()  # Lê o token do arquivo
        decoded_jwt = jwt.decode(encoded_jwt, key, algorithms=['HS256'])
    import Main
    decoded_jwt["version"] = f"{Main.version}"
    response = requests.post("https://samuka.pythonanywhere.com/login",
                         json=decoded_jwt,
                         timeout=60)
    JWT_TOKEN = response.json().get("JWT_TOKEN")
    JWT_DECODER = "b'hXP5vrphNUNwEHDmfV8E1vxlQ28jLZfEpR_BN5SxqUASDDzdassd133x@5!23$%¨SAD2o='"
    
    KEYS = jwt.decode(JWT_TOKEN,JWT_DECODER,algorithms=['HS256'])
    GITHUB = KEYS["GITHUB"]
    AWS_S3 = KEYS["AWS_S3"]
    return True
  except Exception as e:
    return False

# payload = {
#     "GITHUB": "",
#     "AWS_S3": ""
#     }
#key = "b'hXP5vrphNUNwEHDmfV8E1vxlQ28jLZfEpR_BN5SxqUASDDzdassd133x@5!23$%¨SAD2o='"
#print(jwt.encode(payload=payload,key=key,algorithm="HS256"))

#print(jwt.decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJHSVRIVUIiOiJnaHBfa0NFS0E2U003enFwZmY4dzR0SlBYVWxaVlpRYXBCMVN4cEJoIiwiQVdTX1MzIjoiOHM1JUhIc2RvIUp3Y20xX1UzMTVnQGxhbFlDMkV1U2o0QGowaHo5NG42NWp3JDZjNmUtNjc4N2gzZGEzNTgifQ.OvpZ1f7JyJ1kqlAczI4njAb9WWoH9orZ32updVnXwV4",key,algorithms=['HS256']))

#Credentials().encript()
#print(Fernet.generate_key())