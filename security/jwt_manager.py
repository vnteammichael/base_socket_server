import jwt
from utils.config import config

def generate_token(payload):
    secret_key = config.get('secret_key')
    return jwt.encode(payload, secret_key, algorithm="HS256")

def verify_token(token):
    secret_key = config.get('secret_key')
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
