from fastapi import APIRouter, HTTPException, Depends, Form, Query
from pydantic import BaseModel
from typing import List
from datetime import date, datetime, time
from database.database import engine, Session, Base
from database import database
from models.medicos import MedicosModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()
db = database.get_database_connection()
cursor = db.cursor()
now = datetime.now()

class Medicos(BaseModel):
    id: int
    colegiado: int | None = None
    name: str | None = None
    dpi: int | None = None
    especialidad: int | None = None
    pasaporte: str | None = None
    
    
# get conectado a SQL

@router.get("/medicos/", tags=["medicos"])
async def obtener_medicos():
    try:
        db = Session()
        result = db.query(MedicosModel).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
      cursor.close()
        

@router.get("/medico/", tags=["medicos"])
async def obtener_medico(id: int):
    try:
        db = Session()
        result = db.query(MedicosModel).filter(MedicosModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
        cursor.close()
        
@router.get("/colegiado/", tags=["medicos"])
async def obtener_colegiado(col: int):
    try:
        db = Session()
        result = db.query(MedicosModel).filter(MedicosModel.colegiado == col).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
        cursor.close()
        
@router.post("/medico/",  tags=["medicos"])
async def crear_medico(medico: Medicos):
    try:
        db = Session()
        # Verificar si ya existe un usuario
        verificar = db.query(MedicosModel).filter(
            MedicosModel.colegiado == medico.colegiado,
            MedicosModel.name == medico.name,
            MedicosModel.dpi == medico.dpi,
        ).first()

        if verificar:
            return JSONResponse(status_code=400, content={"message": "ya existe medico"})

        registro = MedicosModel(**medico.dict())
        db.add(registro)
        db.commit()
        cursor.close()
        return JSONResponse(status_code=201, content={"message": "Se ha creado medico"})
    except SQLAlchemyError as error:
        return {"message": f"error al crear usuario: {error}"}
    

#Put conectado a SQL
@router.put("/editarmedico/{id}", tags=["medicos"])
async def actualizar( medico: Medicos, id: int):
    try:
        db = Session()
        result = db.query(MedicosModel).filter(MedicosModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        result.id = medico.id
        result.colegiado = medico.colegiado
        result.name = medico.name
        result.dpi = medico.dpi
        result.especialidad = medico.especialidad
        result.pasaporte = medico.pasaporte
        
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Actualización Realizada"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally: 
            cursor.close()
            
            

#Delete conectado a SQL
@router.delete("/eliminarmedico/{id}", tags=["medicos"])
async def eliminar(id: int):
    try:
        db = Session()
        result = db.query(MedicosModel).filter(MedicosModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Eliminado con exito"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally:
           cursor.close()


@router.get("/filtrarmedico/", tags=["medicos"])
async def filtro(
    name: str = Query(None, description="Nombre de Medico"),
    colegiado: str = Query(None, description="colegia"),
    dpi: str = Query(None, description="Diagnostico"),
    especialidad: int = Query(None, description="especialidad")
   ):
    try:
        
        db = Session()
        query = db.query(MedicosModel)

            
        if name:
            query = query.filter(MedicosModel.name.ilike(f"%{name}%"))

        if colegiado is not None:
            query = query.filter(MedicosModel.colegiado == colegiado)

        if dpi:
            query = query.filter(MedicosModel.dpi.ilike(f"%{dpi}%"))

        if especialidad is not None:
            query = query.filter(MedicosModel.especialidad == especialidad)

        
        result = query.all()
        return result
    except Exception as e:
        return {"error": str(e)}  