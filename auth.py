import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError  # Ajuste en la importación
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
        return decoded_token is not None  # Corregido para devolver True si el token es válido
    except jwt.ExpiredSignatureError:  # Corregido para usar el nombre completo del error
        return False
