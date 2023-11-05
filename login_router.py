from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from auth import create_access_token
from sqlalchemy.orm import Session
from database import database
from models.usuarios import UsuariosModel

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str
    
    
def get_db_session() -> Session:
    db = database.get_database_session()
    try:
        yield db
    finally:
        db.close()
    


@router.post("/login", tags=["login"])
async def login(form_data: LoginRequest, db: Session = Depends(get_db_session)):
    usuario = db.query(UsuariosModel).filter(UsuariosModel.email == form_data.email).first()
    if usuario is None:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Verificar la contraseña (debes usar una función de hash segura en lugar de esta comparación directa)
    if usuario.password != form_data.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Las credenciales son válidas, generamos el token JWT
    access_token = create_access_token(data={"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}
