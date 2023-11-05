import jwt
from jwt import ExpiredSignatureError, DecodeError
from fastapi import HTTPException

# Configura la clave secreta para firmar el token
secret_key = "admin"
algorithm = "HS256"

def create_access_token(data: dict):
    token = jwt.encode(data, secret_key, algorithm=algorithm)
    return token

def decode_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except (ExpiredSignatureError, DecodeError):
        return None

def verify_token(token: str) -> bool:
    try:
        decoded_token = decode_token(token)
        return decode_token(token) is not None
    except HTTPException:
        return False
