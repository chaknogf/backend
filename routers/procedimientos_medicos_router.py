from fastapi import APIRouter, HTTPException, Depends, Form, Query
from pydantic import BaseModel
from typing import List
from datetime import date, datetime, time
from database.database import engine, Session, Base
from database import database
from models.procedimientos import ProceMedicosModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter()
db = database.get_database_connection()
cursor = db.cursor()

class ProceMedicos(BaseModel):
    id: int
    fecha: str | None = None
    servicio: int | None = None
    sexo: str | None = None
    abreviatura: str | None = None
    especialidad: int | None = None
    cantidad: int | None = None
    medico: int | None = None
    created_by: str | None = None
    
@router.get("/promedic", tags=["Procedimientos Medicos"])
async def obtener_procedimientos():
    try:
        db = Session()
        result = db.query(ProceMedicosModel).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
      cursor.close()
      
      
@router.get("/procedimiento/",tags=["Procedimientos Medicos"])
async def obtener_proce():
    try:
        db = Session()
        result = db.query(ProceMedicosModel).filter(ProceMedicosModel.id == id).first()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
        cursor.close()