from fastapi import Request, HTTPException
from jwt import decode, exceptions
from starlette.status import HTTP_403_FORBIDDEN

SECRET = "admin"  # Reemplaza con tu clave secreta JWT

def jwt_middleware(request: Request):
    token = request.headers.get("Authorization")
    if token:
        try:
            payload = decode(token, SECRET, algorithms=["HS256"])
            return payload
        except exceptions.ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Token de acceso expirado"
            )
        except exceptions.DecodeError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Token de acceso inválido"
            )
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Token de acceso no proporcionado"
        )
