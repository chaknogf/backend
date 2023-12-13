from fastapi import APIRouter, HTTPException, Query, Form
from pydantic import BaseModel
from typing import List
from datetime import date, datetime, time
from database.database import engine, Session, Base
from database import database
from models.uisau import uisauModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()
db = database.get_database_connection()
cursor = db.cursor()
now = datetime.now()

class uisau(BaseModel):
    id: int
    expediente: int | None = None
    nombres: str | None = None
    apellidos: str | None = None
    estado: int | None = None
    situacion: int | None = None
    lugar_referencia: int | None = None
    fecha_referencia: date | None = None
    estadia: int | None = None
    cama: int | None = None
    especialidad: int | None = None
    servicio: int | None = None
    informacion: str | None = None
    contacto: str | None = None
    parentesco: int | None = None
    telefono: int | None = None
    fecha: str | None = None
    hora: str | None = None
    fecha_contacto: str | None = None
    hora_contacto: str | None = None
    nota: str | None = None
    estudios: str | None = None
    evolucion: str | None = None
    id_consulta: int | None = None
    created_by: str | None = None
    update_by: str | None = None
    
    
bModel = uisauModel


#Get conectado a sql
@router.get("/uisau/", tags=["UISAU"])
async def obtener_consultas():
    try:
        db = Session()
        result = db.query(bModel).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
        print("consultado")
        
@router.get("/registro/", tags=["UISAU"])
def buscar_id(id: int):
    try:
        db = Session()
        result = db.query(bModel).filter(uisauModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally:
        print(f"id: {id} datetime:{now} CONSULTADO")
        
@router.get("/infos/", tags=["UISAU"])
def buscar_id(consulta: int):
    try:
        db = Session()
        result = db.query(bModel).filter(uisauModel.id_consulta == consulta).all()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally:
        print(f"id: {id} datetime:{now} CONSULTADO")
        

@router.get("/filter/", tags=["UISAU"])
async def filtro(
    id: int = Query(None, description="Id"),
    id_consulta: int = Query(None, description="Número de id de consulta"),
    expediente: int = Query(None, description="Número de Expediente"),
    estado: int = Query(None, description="Estado del Paciente"),
    fecha: str = Query(None, description="Fecha de Consulta"),
    fecha_referencia: str = Query(None, description="Fecha de Consulta"),
    lugar_referencia: int = Query(None, description="Lugar de referencia"),
    nombres: str = Query(None, description="Nombres"),
    apellidos: str = Query(None, description="Apellidos"),
    usuario: int = Query(None, description="Usuario de UISAU"),
    estadia: int = Query(None, description="Estadia de paciente")
    
                ):
    try:
        
        db = Session()
        query = db.query(bModel)

        # Agregar condiciones para los filtros con coincidencias parciales
        if id is not None:
            query = query.filter(bModel.id == id)
            
        if id_consulta is not None:
            query = query.filter(bModel.id_consulta == id_consulta)
            
        if estado:
            query = query.filter(bModel.estado == estado)

        if expediente:
            query = query.filter(bModel.expediente == expediente)

        if fecha:
            query = query.filter(bModel.fecha.ilike(f"%{fecha}%"))

        if nombres:
            query = query.filter(bModel.nombres.ilike(f"%{nombres}%"))

        if apellidos:
            query = query.filter(bModel.apellidos.ilike(f"%{apellidos}%"))

        if fecha_referencia:
            query = query.filter(bModel.fecha_referencia.ilike(f"%{fecha_referencia}%"))

        if lugar_referencia:
            query = query.filter(bModel.lugar_referencia == lugar_referencia)
            
        if usuario:
            query = query.filter(bModel.Usuario == usuario)
            
        if estadia:
            query = query.filter(bModel.estadia == estadia)

        result = query.all()
        return result
    except Exception as e:
        return {"error": str(e)}    
  
    #Post conectado a SQL

@router.post("/uisausave/", tags=["UISAU"])
async def crear(data: uisau ):
    try:
        db = Session()
        
        resgistro = bModel(**data.dict())
        db.add(resgistro)
        db.commit()  
         
        return JSONResponse(status_code=201, content={"message": "Se ha registrado la consulta"})
    except SQLAlchemyError as error:
         return {"message": f"error al crear consulta: {error}"}
    finally:
        cursor.close()


@router.put("/uisauedit", tags=["UISAU"])
async def editar(edit: uisau, id: int):
    try:
        db = Session()
        result = db.query(uisauModel).filter(uisauModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        result.parentesco = edit.parentesco
        result.fecha_contacto = edit.fecha_contacto
        result.hora_contacto = edit.hora_contacto
        result.update_by = edit.update_by
        result.contacto = edit.contacto
        result.telefono = edit.telefono
        result.informacion = edit.informacion
        result.nota = edit.nota
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Actualizacion realizada"})
    except SQLAlchemyError as error:
        return {"message": f"Error al actualizar la cita: {error}"}
    finally:
        db.close()
        
@router.delete("/uisaudelet/{id}",  tags=["UISAU"])
async def eliminar_cita(id: int):
    try:
        db = Session()
        result = db.query(uisauModel).filter(uisauModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Eliminado con exito"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar cita: {error}"}
    finally:
           db.close()