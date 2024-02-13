from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import BaseModel
from typing import List
from datetime import date, datetime, time
from database.database import engine, Session, Base
from database import database
from models.usuarios import UsuariosModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()
db = database.get_database_connection()
cursor = db.cursor()
now = datetime.now()

class Usuarios(BaseModel):
    id: int
    code: int 
    username: str
    name: str
    dpi: int | None = None
    email: str | None = None
    password: str | None = None
    rol: int
    
    
# get conectado a SQL

@router.get("/usurios/", tags=["usuarios"])
async def obtener_usuarios():
    try:
        db = Session()
        result = db.query(UsuariosModel).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
      cursor.close()
        

@router.get("/usuario/", tags=["usuarios"])
async def obtener_usuario(id: int):
    try:
        db = Session()
        result = db.query(UsuariosModel).filter(UsuariosModel.id == id).first()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
        cursor.close()
        
@router.get("/usuriocod/", tags=["usuarios"])
async def obtener_usuario_cod(cod: int):
    try:
        db = Session()
        result = db.query(UsuariosModel).filter(UsuariosModel.code == cod).first()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
        cursor.close()
        
@router.get("/username/", tags=["usuarios"])
async def obtener_usuarios(user: str):
    try:
        db = Session()
        result = db.query(UsuariosModel).filter(UsuariosModel.username == user).first()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
        cursor.close()
        
@router.post("/user/",  tags=["usuarios"])
async def crear_user(user: Usuarios):
    try:
        db = Session()
        # Verificar si ya existe un usuario
        verificar = db.query(UsuariosModel).filter(
            UsuariosModel.code == user.code,
            UsuariosModel.username == user.username,
            UsuariosModel.name == user.name,
            UsuariosModel.dpi == user.dpi,
            UsuariosModel.email == user.email
        ).first()

        if verificar:
            return JSONResponse(status_code=400, content={"message": "ya existe el usuario"})

        registro = UsuariosModel(**user.dict())
        db.add(registro)
        db.commit()
        cursor.close()
        return JSONResponse(status_code=201, content={"message": "Se ha creado el usuario"})
    except SQLAlchemyError as error:
        return {"message": f"error al crear usuario: {error}"}
    

#Put conectado a SQL
@router.put("/editarusuario/{id}", tags=["usuarios"])
async def actualizar( user: Usuarios, id: int):
    try:
        db = Session()
        result = db.query(UsuariosModel).filter(UsuariosModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        result.id = user.id
        result.code = user.code
        result.username = user.username
        result.name = user.name
        result.dpi = user.dpi
        result.email = user.email
        result.password = user.password
        result.rol = user.rol
        
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Actualización Realizada"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally: 
            cursor.close()
            
@router.put("/updateuser/", tags=["usuarios"])
async def actualizar( user: Usuarios, username: str):
    try:
        db = Session()
        result = db.query(UsuariosModel).filter(UsuariosModel.username == username).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        result.name = user.name
        result.dpi = user.dpi
        result.email = user.email
        result.password = user.password
        
        
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Actualización Realizada"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally: 
            cursor.close()
            
            

#Delete conectado a SQL
@router.delete("/usuario/{id}", tags=["usuarios"])
async def eliminar(id: int):
    try:
        db = Session()
        result = db.query(UsuariosModel).filter(UsuariosModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Eliminado con exito"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally:
           cursor.close()
