from fastapi import APIRouter, HTTPException, Depends, Form, Query
from pydantic import BaseModel
from typing import List
from datetime import date, datetime, time
from database.database import engine, Session, Base
from database import database
from models.procedimientos import ProceMedicosModel, CodigosProceModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from datetime import datetime


router = APIRouter()
db = database.get_database_connection()
cursor = db.cursor()

class ProceMedicos(BaseModel):
    id: int
    fecha: str | None = None
    servicio: int | None = None
    sexo: str | None = None
    abreviatura: str | None = None
    procedimiento: str | None = None
    especialidad: int | None = None
    cantidad: int | None = None
    medico: int | None = None
    created_by: str | None = None
    
class CodigosProces(BaseModel):
    id: int
    abreviatura: str
    procedimiento: str
    
@router.get("/promedic", tags=["Procedimientos Medicos"])
async def obtener_procedimientos():
    try:
        db = Session()
        result = db.query(ProceMedicosModel).limit(1000).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
      cursor.close()
      
@router.get("/abreviaturas", tags=["Codigos Procedimientos"])
async def obtener_abreviaturas():
    try:
        db = Session()
        result = db.query(CodigosProceModel).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
      cursor.close()
      
      
@router.get("/procedimiento/",tags=["Procedimientos Medicos"])
async def obtener_proce(id: int):
    try:
        db = Session()
        result = db.query(ProceMedicosModel).filter(ProceMedicosModel.id == id).first()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
        cursor.close()
        
@router.get("/abreviaturaid/",tags=["Codigos Procedimientos"])
async def obtener_abre_id(id: int):
    try:
        db = Session()
        result = db.query(CodigosProceModel).filter(CodigosProceModel.id == id).first()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
        cursor.close()
        
@router.get("/abreviatura/",tags=["Codigos Procedimientos"])
async def obtener_abre(abreviatura: str):
    try:
        db = Session()
        result = db.query(CodigosProceModel).filter(CodigosProceModel.abreviatura == abreviatura).first()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
        cursor.close()
        
@router.post("/procedimiento_registrado", tags=["Procedimientos Medicos"])
async def crear(proce: ProceMedicos):
    try:
        db = Session()
        verificar = db.query(ProceMedicosModel).filter(
            ProceMedicosModel.fecha == proce.fecha,
            ProceMedicosModel.especialidad == proce.especialidad,
            ProceMedicosModel.procedimiento == proce.procedimiento,
            ProceMedicosModel.servicio == proce.servicio
        ).first()
         
        if verificar:
            return JSONResponse(status_code=400, content={"message": "ya existe"})
        
        registro = ProceMedicosModel(**proce.dict())
        db.add(registro)
        db.commit()
        cursor.close()
        return JSONResponse(status_code=201, content={"message": "Se ha registrado"})
    except SQLAlchemyError as error:
        return {"message": f"error al crear usuario: {error}"}
    
@router.post("/nueva_abreviatura", tags=["Codigos Procedimientos"])
async def crear_abreviatura(codigo: CodigosProces):
    try:
        db = Session()
        verificar = db.query(CodigosProceModel).filter(
            CodigosProceModel.abreviatura == codigo.abreviatura,
            CodigosProceModel.procedimiento == codigo.procedimiento,
        ).first()
        
        if verificar:
            return JSONResponse(status_code=400, content={"message": "ya existe"})
        
        registro = CodigosProceModel(**codigo.dict())
        db.add(registro)
        db.commit()
        cursor.close()
        return JSONResponse(status_code=201, content={"message": "Se ha creado cie10"})
    except SQLAlchemyError as error:
        return {"message": f"error al crear usuario: {error}"}
    
        
@router.put("/procedimiento_editado", tags=["Procedimientos Medicos"])
async def editar(proce: ProceMedicos, id: int):
    try:
        db = Session()
        result = db.query(ProceMedicosModel).filter(ProceMedicosModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "no encontrado"})
        
        result.fecha = proce.fecha
        result.servicio = proce.servicio
        result.sexo = proce.sexo
        result.abreviatura = proce.abreviatura
        result.procedimiento = proce.procedimiento
        result.medico = proce.medico
        result.cantidad = proce.cantidad
        
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Actualizado con exito"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally: 
        cursor.close()
            
@router.put("/abreviatura_editada", tags=["Codigos Procedimientos"])
async def editar_abreviatura(proce: CodigosProces, id: int):
    try:
        db = Session()
        result = db.query(CodigosProceModel).filter(CodigosProceModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "no encontrado"})
        
        result.abreviatura = proce.abreviatura
        result.procedimiento = proce.procedimiento
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Actualizado con exito"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally: 
        cursor.close()
            
@router.delete("/procedimiento_eliminado/{id}", tags=["Procedimientos Medicos"])
async def eliminar(id: int):
    try:
        db = Session()
        result = db.query(ProceMedicosModel).filter(ProceMedicosModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Eliminado con exito"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally:
           cursor.close()

@router.delete("/abreviatura_eliminada/{id}", tags=["Codigos Procedimientos"])
async def eliminar_abreviatura(id: int):
    try:
        db = Session()
        result = db.query(CodigosProceModel).filter(CodigosProceModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Eliminado con exito"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally:
           cursor.close()
           
@router.get("/filtrar_procedimientos/", tags=["Procedimientos Medicos"])
async def filtro(
    id: str = Query(None, description="id"),
    fecha: str = Query(None, description="Fecha"),
    servicio: str = Query(None, description="Servicio"),
    sexo: str = Query(None, description="Sexo"),
    abreviatura: str = Query(None, description="Abreviatura"),
    especialidad: int = Query(None, description="especialidad"),
    medico: int = Query(None, description="Medico"),
    procedimiento: int = Query(None, description="Procedimiento")
   ):
    try:
        
        db = Session()
        query = db.query(ProceMedicosModel)

        if id:
            query = query.filter(ProceMedicosModel.id == id)
            
        if fecha:
            query = query.filter(ProceMedicosModel.fecha == fecha)

        if servicio is not None:
            query = query.filter(ProceMedicosModel.servicio == servicio)

        if sexo:
            query = query.filter(ProceMedicosModel.sexo == sexo)

        if abreviatura:
            query = query.filter(ProceMedicosModel.abreviatura.ilike(f"%{abreviatura}%"))

        if especialidad is not None:
            query = query.filter(ProceMedicosModel.especialidad == especialidad)
        
        if medico is not None:
            query = query.filter(ProceMedicosModel.medico == medico)
            
        if procedimiento is not None:
            query = query.filter(ProceMedicosModel.procedimiento.ilike(f"%{procedimiento}%"))

        
        result = query.limit(1000).all()
        return result
    except Exception as e:
        return {"error": str(e)}  
    
@router.get("/filtrar_abreviaturas/", tags=["Codigos Procedimientos"])
async def filtro_abreviatura(
    id: int = Query(None, description="ID"),
    abreviatura: str = Query(None, description="Abreviatura"),
    procedimiento: str = Query(None, description="Procedimiento")
   ):
    try:
        db = Session()
        query = db.query(ProceMedicosModel)

        if id:
            query = query.filter(ProceMedicosModel.id == id)
            
        if abreviatura:
            query = query.filter(ProceMedicosModel.abreviatura.ilike(f"%{abreviatura}%"))
            
        if procedimiento is not None:
            query = query.filter(ProceMedicosModel.procedimiento.ilike(f"%{procedimiento}%"))
            
        result = query.all()
        return result
    except Exception as e:
        return {"error": str(e)}
    
    
