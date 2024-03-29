from fastapi import APIRouter, HTTPException, Depends, Form, Query, Request
from pydantic import BaseModel
from typing import List
from datetime import date, datetime, time
from auth import decode_token
from database.database import engine, Session, Base
from database import database
from models.cie10 import Cie10Model
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter()
db = database.get_database_connection()
cursor = db.cursor()
now = datetime.now()

class Cie10(BaseModel):
    id: int
    cod: str | None = None
    grupo: str | None = None
    dx: str | None = None
    abreviatura: str | None = None
    especialidad: int | None | None
    
    
# Función de dependencia para obtener roles desde el token
async def get_roles(token: dict = Depends(decode_token)):
    return token.get("roles", {})
    
# get conectado a SQL

@router.get("/cie10/", tags=["Cie10"])
async def obtener_dxs(roles: dict = Depends(get_roles)):
    try:
        # # Verifica que el usuario tenga permisos para el método GET
        # if roles.get("read_only", False):
        #     raise HTTPException(status_code=403, detail="Acceso no autorizado (solo lectura)")
    
        db = Session()
        result = db.query(Cie10Model).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
      cursor.close()
        

@router.get("/diagnostico/", tags=["Cie10"])
async def obtener_dx(id: int):
    try:
        db = Session()
        result = db.query(Cie10Model).filter(Cie10Model.id == id).first()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
        cursor.close()
        
@router.post("/cie10/",  tags=["Cie10"])
async def crear(cie10: Cie10):
    try:
        db = Session()
        # Verificar si ya existe un usuario
        verificar = db.query(Cie10Model).filter(
            Cie10Model.cod == cie10.cod,
            Cie10Model.dx == cie10.dx,
            Cie10Model.abreviatura == cie10.abreviatura,
        ).first()

        if verificar:
            return JSONResponse(status_code=400, content={"message": "ya existe cie10"})

        registro = Cie10Model(**cie10.dict())
        db.add(registro)
        db.commit()
        cursor.close()
        return JSONResponse(status_code=201, content={"message": "Se ha creado cie10"})
    except SQLAlchemyError as error:
        return {"message": f"error al crear usuario: {error}"}
    

#Put conectado a SQL
@router.put("/editarcie10/{id}", tags=["Cie10"])
async def actualizar( cie10: Cie10, id: int):
    try:
        db = Session()
        result = db.query(Cie10Model).filter(Cie10Model.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        
        result.cod= cie10.cod
        result.grupo = cie10.grupo
        result.dx = cie10.dx
        result.especialidad = cie10.especialidad
        result.abreviatura = cie10.abreviatura
        
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Actualización Realizada"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally: 
            cursor.close()
            
            

#Delete conectado a SQL
@router.delete("/eliminarcie10/{id}", tags=["Cie10"])
async def eliminar(id: int):
    try:
        db = Session()
        result = db.query(Cie10Model).filter(Cie10Model.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Eliminado con exito"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally:
           cursor.close()
 
@router.get("/filtrarcie10/", tags=["Cie10"])
async def filtro(
    cod: str = Query(None, description="Codigo de cie-10"),
    grupo: str = Query(None, description="Grupo"),
    dx: str = Query(None, description="Diagnostico"),
    abreviatura: str = Query(None, description="Abreviatura"),
    especialidad: int = Query(None, description="especialidad")
   ):
    try:
        
        db = Session()
        query = db.query(Cie10Model)

            
        if cod:
            query = query.filter(Cie10Model.cod.ilike(f"%{cod}%"))

        if grupo is not None:
            query = query.filter(Cie10Model.grupo == grupo)

        if dx:
            query = query.filter(Cie10Model.dx.ilike(f"%{dx}%"))

        if abreviatura:
            query = query.filter(Cie10Model.abreviatura.ilike(f"%{abreviatura}%"))

        if especialidad is not None:
            query = query.filter(Cie10Model.especialidad == especialidad)

        
        result = query.all()
        return result
    except Exception as e:
        return {"error": str(e)}  