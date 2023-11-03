from fastapi import APIRouter, HTTPException, Query, Form
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
    name: str
    dpi: str | None = None
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
        print("consultado")
        

@router.get("/usurio/", tags=["usuarios"])
async def obtener_usuarios(cod: int):
    try:
        db = Session()
        result = db.query.filter(UsuariosModel.code == cod).first()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
        print("consultado")
        
@router.post("/usuriocrear/", response_class=Usuarios, tags=["usuarios"])
async def crear(data: Usuarios):
    try:
        db = Session()
        #verificar si ya existe una cosulta
        verificar = db.query(UsuariosModel).filter(
            UsuariosModel.code == data.code,
            UsuariosModel.name == data.name,
            UsuariosModel.dpi == data.dpi,
            UsuariosModel.email == data.email
        ).first()
        
        if verificar: 
            return JSONResponse(status_code=400, content={"message": "ya existe usuario"})
            
        resgistro = UsuariosModel(**data.dict())
        db.add(resgistro)
        db.commit()  
         
        return JSONResponse(status_code=201, content={"message": "Se ha creado usuario"})
    except SQLAlchemyError as error:
         return {"message": f"error al crear consulta: {error}"}
    finally:
        cursor.close()
        
#Put conectado a SQL
@router.put("/editarusuario/{id}", tags=["usuarios"])
async def actualizar( user: Usuarios, cod: int):
    try:
        db = Session()
        result = db.query(UsuariosModel).filter(UsuariosModel.code == cod).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        result.id = user.id
        result.code = user.code
        result.name = user.code
        result.dpi = user.dpi
        result.email = user.email
        result.password = user.password
        result.rol = user.rol
        
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Actualización Realizada"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally: 
            print(f" ACTUALIZADO")
            
            

#Delete conectado a SQL
@router.delete("/usuario/{cod}", tags=["usuarios"])
async def eliminar(cod: int):
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
            print(f" ELIMINADO realizado")
