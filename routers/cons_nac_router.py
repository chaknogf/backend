from fastapi import APIRouter, HTTPException, Query, Form
from pydantic import BaseModel
from typing import List
from datetime import date, datetime, time
from database.database import engine, Session, Base
from database import database
from models.cons_nac import Cons_NacModel
from models.paciente import PacienteModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import lazyload

router = APIRouter()
db = database.get_database_connection()
cursor = db.cursor()
now = datetime.now()
año = now.year

class ConsNac(BaseModel):
    id: int 
    fecha: date
    cor: int | None = None
    año: int | None = None 
    doc: str | None = None 
    fecha_parto: date | None = None
    madre: str | None = None
    dpi: int | None = None
    passport: str | None = None
    libro: int | None = None
    folio: int | None = None
    partida: int | None = None
    muni: int | None = None
    edad: int | None = None
    vecindad: int | None = None
    sexo_rn: str | None = None
    lb: int | None = None
    onz: int | None = None
    hora: time | None = None
    medico: int | None = None
    colegiado: int | None = None
    dpi_medico: int | None = None
    hijos: int | None = None
    vivos: int | None = None
    muertos: int | None = None
    tipo_parto: int | None = None
    clase_parto: int | None = None
    certifica: int | None = None
    
    
    #gets
    
@router.get("/consnac/", tags=["Constancias de Nacimiento"])
async def ver_todas():
    try:
        with Session() as db:
            result = (
                db.query(Cons_NacModel)
                .order_by(desc(Cons_NacModel.id))
                .limit(10000)
                .options(lazyload('*'))
                .all()
            )
            if not result:
                return JSONResponse(status_code=404, content=jsonable_encoder([]))
            return result
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")
    
@router.get("/constancia_nac_id/", tags=["Constancias de Nacimiento"])
async def ver_una_id(id:int):
    try:
        db = Session()
        result = db.query(Cons_NacModel).filter(Cons_NacModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        
        consulta = result
        
        created_at = consulta.created_at
        updated_at = consulta.updated_at
        
        created_at_str = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else None
        updated_at_str = updated_at.strftime("%Y-%m-%d %H:%M:%S") if updated_at else None

        # Agregar created_at y updated_at al diccionario de resultados
        consulta_dict = consulta.__dict__
        
        consulta_dict["created_at"] = created_at_str
        consulta_dict["updated_at"] = updated_at_str
        
        return JSONResponse(status_code=200, content=jsonable_encoder(consulta_dict))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")
    finally:
        db.close()

@router.get("/constancia_nac_cor/", tags=["Constancias de Nacimiento"])
async def ver_una_cor(cor:str):
    try:
        db = Session()
        result = db.query(Cons_NacModel).filter(Cons_NacModel.cor == cor).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        
        consulta = result
        
        created_at = consulta.created_at
        updated_at = consulta.updated_at
        
        created_at_str = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else None
        updated_at_str = updated_at.strftime("%Y-%m-%d %H:%M:%S") if updated_at else None

        # Agregar created_at y updated_at al diccionario de resultados
        consulta_dict = consulta.__dict__
        
        consulta_dict["created_at"] = created_at_str
        consulta_dict["updated_at"] = updated_at_str
        
        return JSONResponse(status_code=200, content=jsonable_encoder(consulta_dict))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")
    finally:
        db.close()
        
#post

@router.post("/crear_cons_nac/", tags=["Constancias de Nacimiento"])
async def crear_cor(data: ConsNac):
    try:
        db = Session()
        
        consulta_verificacion = db.query(Cons_NacModel).filter(
            Cons_NacModel.madre == data.madre,
            Cons_NacModel.fecha_parto == data.fecha_parto,
            Cons_NacModel.tipo_parto == 1
        ).first()
        
        if consulta_verificacion:
            return JSONResponse(status_code=400, content={"message": "ya existe constancia para paciente"})
        registro = Cons_NacModel()
    
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")
    finally:
        db.close()
        
#put

@router.put("/cons_nac/{id}", tags=["Constancias de Nacimiento"])
async def actualizar(data: ConsNac, id: int):
    try:
        db = Session()
        result = db.query(Cons_NacModel).filter(Cons_NacModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        result.fecha = data.fecha
        result.cor = data.cor
        result.año = data.año 
        result.doc = data.doc
        result.fecha_parto = data.fecha_parto
        result.madre = data.madre
        result.dpi = data.dpi
        result.passport = data.passport
        result.libro = data.libro
        result.folio = data.folio
        result.partida = data.partida
        result.muni = data.muni
        result.edad = data.edad
        result.vecindad = data.vecindad
        result.sexo_rn = data.sexo_rn
        result.lb = data.lb
        result.onz = data.onz
        result.hora = data.hora
        result.medico = data.medico
        result.colegiado = data.colegiado
        result.dpi_medico = data.dpi_medico
        result.hijos = data.hijos
        result.vivos = data.vivos
        result.muertos = data.muertos
        result.tipo_parto = data.tipo_parto
        result.clase_parto = data.clase_parto
        result.certifica = data.certifica
            
    
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Actualización Realizada"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally: 
            print(f" ACTUALIZADO")
            
#delete

@router.delete("/cons_nac", tags=["Constancias de Nacimiento"])
async def eliminar(id: int):
    try:
        db = Session()
        result = db.query(Cons_NacModel).filter(Cons_NacModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No enontrado"})
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Eliminado con exito"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally:
            print(f" ELIMINADO realizado")