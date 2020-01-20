import jwt
import base64

msg = {
    'header': '',
    'payload': {'school':'udacity'},
    'secret': 'learning'
}

encoded_jwt = jwt.encode(msg['payload'], key=msg['secret'], algorithm="HS256")
print(encoded_jwt)

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXJrIjoiYmF0dGVyeSBwYXJrIn0.bQEjsBRGfhKKEFtGhh83sTsMSXgSstFA_P8g2qV5Sns"
dec = base64.b64decode(str(token.split(".")[1]+"=="))
#payload = jwt.decode(token, 'learning', verify=True)

print(dec)
