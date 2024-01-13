from fastapi import APIRouter, HTTPException, Query, Form
from pydantic import BaseModel
from typing import List
from datetime import date, datetime, time, timedelta
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
año_actual = now.year


def correlativo_unico():
    try:
        with Session() as db:
            # Obtén la fecha actual
            fecha_actual = datetime.now()
            # Obtén el año actual
            año_actual = fecha_actual.year
            # Calcula la fecha de ayer
            ayer = (fecha_actual - timedelta(days=1)).year

            cor_nuevo = None

            # Verifica si el año ha cambiado y reinicia el contador
            if año_actual != ayer:
                cor_nuevo = 1  # Reinicia a 0001
            elif cor_nuevo is None:
                cor_nuevo = 1
            else:
                # Continuar el correlativo
                cor_nuevo = db.execute(select(func.max(Cons_NacModel.cor))).scalar() or 0
                cor_nuevo += 1  # Incrementa el correlativo

            # Formatea el correlativo con 4 dígitos
            correlativo_formateado = str(cor_nuevo).zfill(5)

            return {"cor": correlativo_formateado, "año": año_actual}
    except SQLAlchemyError as error:
        # Maneja la excepción de manera adecuada, podrías imprimir el error o realizar alguna acción específica
        print(f"Error al consultar: {error}")
        return {"error": "Error al consultar la base de datos"}
    finally:
        cursor.close()
        
        
class ConsNac(BaseModel):
    id: int 
    fecha: date
    cor: int | None = None
    ao: int | None = None 
    doc: str | None = None 
    fecha_parto: date | None = None
    madre: str | None = None
    dpi: int | None = None
    passport: str | None = None
    libro: int | None = None
    folio: int | None = None
    partida: int | None = None
    depto: int | None = None
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
    create_by: str | None = None
    
    
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
        
        documento = Cons_NacModel(**data.dict())
        db.add(documento)
        db.commit()
        correlativo_unico()
        return JSONResponse(status_code=201, content={"message": "Registrado con exito"})
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
        result.ao = data.ao 
        result.doc = data.doc
        result.fecha_parto = data.fecha_parto
        result.madre = data.madre
        result.dpi = data.dpi
        result.passport = data.passport
        result.libro = data.libro
        result.folio = data.folio
        result.partida = data.partida
        result.depto = data.depto
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
 
#correlativo nuevo           
@router.get("/cor_nuevo", tags=["Constancias de Nacimiento"])
async def correlativos():   
    result = correlativo_unico()
    return result


@router.get("/filtrarConstanciaN/", tags=["Constancias de Nacimiento"])
async def filtro(
    fecha: str = Query(None, description="Fecha de constancia"),
    cor: str = Query(None, description="correlativo"),
    fecha_parto: str = Query(None, description="Fecha de parto"),
    madre: str = Query(None, description="Nombre de la madre"),
    medico: int = Query(None, description="Medico"),
    certifica: int = Query(None, description="Certifica"),
    tipo_parto: int = Query(None, description="Tipo de parto"),
    clase_parto: int = Query(None, description="Clase de parto"),
    lb: int = Query(None, description="Libras"),
    onz: int = Query(None, description="onzas")
    
):
    try:
        db = Session()
        query = db.query(Cons_NacModel)
        
        if fecha is not None:
            query = query.filter(Cons_NacModel.fecha == fecha)
        if  cor:
            query = query.filter(Cons_NacModel.cor.ilike(f"%{cor}%"))
        if fecha_parto is not None:
            query = query.filter(Cons_NacModel.fecha_parto == fecha_parto)
        if madre:
            query = query.filter(Cons_NacModel.madre.ilike(f"%{madre}%"))
        if medico is not None:
            query = query.filter(Cons_NacModel.medico == medico)
        if certifica is not None:
            query = query.filter(Cons_NacModel.certifica == certifica)
        if tipo_parto is not None:
            query = query.filter(Cons_NacModel.tipo_parto == tipo_parto)
        if clase_parto is not None:
            query = query.filter(Cons_NacModel.clase_parto == clase_parto)
        if lb is not None:
            query = query.filter(Cons_NacModel.lb == lb)
        if onz is not None:
            query = query.filter(Cons_NacModel.onz == onz)
            
        result = query.all()
        return result
    except Exception as e:
        return {"error": str(e)}
        

