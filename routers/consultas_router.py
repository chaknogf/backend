from fastapi import APIRouter, HTTPException, Query, Form
from pydantic import BaseModel
from typing import List
from datetime import date, datetime, time
from database.database import engine, Session, Base
from database import database
from models.consulta import ConsultasModel, VistaEmergencia, VistaCoex, VistaIngreso
from models.paciente import PacienteModel
#from models.paciente import PacienteModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()
db = database.get_database_connection()
cursor = db.cursor()
now = datetime.now()
#año = date.year(now)

class Consultas(BaseModel):
    id: int
    hoja_emergencia: str| None = None
    expediente: int | None = None
    fecha_consulta: date | None = None
    hora: time | None = None
    nombres: str | None = None
    apellidos: str | None = None
    nacimiento: date | None = None
    edad: str | None = None
    sexo: str | None = None
    dpi: str | None = None
    direccion: str | None = None
    acompa: str | None = None
    parente: int  | None = None
    telefono: int | None = None
    nota: str | None = None
    especialidad: int | None = None
    recepcion: bool | None = None
    fecha_egreso: date | None = None
    fecha_recepcion: datetime | None = None
    tipo_consulta: int | None = None
    created_at: datetime | None = None
    
    
    
    #Get conectados a SQL
@router.get("/consultas/", tags=["Consultas"])
async def obtener_consultas():
    try:
        db = Session()
        result = db.query(ConsultasModel).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar: {error}"}
    finally:
        print("consultado")
        
        
@router.get("/consulta/", tags=["Consultas"])
async def buscarId(id: int):
    try:
        db = Session()
        result = (
            db.query(ConsultasModel,(PacienteModel.nombre).label("name"), (PacienteModel.apellido).label("lastname"))
            .join(ConsultasModel.pacientes)
            .filter(ConsultasModel.id == id)
            .first()
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="No encontrado")
        
        consulta, name, lastname = result  # Desempaquetar la tupla
        
        consulta_dict = consulta.__dict__
        consulta_dict["name"] = name
        consulta_dict["lastname"] = lastname
        
        print(f"expediente: {id} datetime: {now} CONSULTADO")
        return JSONResponse(status_code=200, content=jsonable_encoder(consulta_dict))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")
    finally:
        db.close()

@router.get("/consulta/servicio/", tags=["Consultas"])
async def consultas(fecha: str, tipo: int):
    try: 
        db = Session()
        NoEncontrado = []
        result = (
            db.query(ConsultasModel, PacienteModel.nombre, PacienteModel.apellido)
            .join(ConsultasModel.pacientes)
            .filter(ConsultasModel.fecha_consulta == fecha, ConsultasModel.tipo_consulta == tipo)
        ).all()
        
        if not result:
            return JSONResponse(status_code=200, content=jsonable_encoder(NoEncontrado))

        consulta, name, lastname = result[0]  # Desempaquetar la tupla
        
        consulta_dict = consulta.__dict__
        consulta_dict["name"] = name
        consulta_dict["lastname"] = lastname
        
        print(f"expediente: {consulta.id} datetime: {now} CONSULTADO")
        return JSONResponse(status_code=200, content=jsonable_encoder(consulta_dict))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")
    finally:
        db.close()

        
@router.get("/consultando/", tags=["Consultas"])
async def consultas(fecha: str, tipo: int,especialidad: int):
    try: 
        db = Session()
        NoEncontrado = []
        result = (
            db.query(ConsultasModel)
            .filter(ConsultasModel.fecha_consulta == fecha, ConsultasModel.tipo_consulta == tipo, ConsultasModel.especialidad == especialidad)
        ).all()
        
        if not result:
            return JSONResponse(status_code=200, content=jsonable_encoder(NoEncontrado))

       # Convertir los resultados en una lista de diccionarios
        consulta = [consulta.__dict__ for consulta in result]
        
        return consulta

        
        print(f"expediente: {consulta.id} datetime: {now} CONSULTADO")
        return JSONResponse(status_code=200, content=jsonable_encoder(consulta_dict))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")
    finally:
        db.close()
                
 
#       #Post conectado a SQL

    #Post conectado a SQL
@router.post("/consultas/",response_model=consultas, tags=["Consultas"])
async def crear(data: Consultas ):
    try:
        db = Session()
        # verificar si ya existe una consulta
        consulta_verificacion = db.query(ConsultasModel).filter(
            ConsultasModel.expediente == data.expediente, 
            ConsultasModel.tipo_consulta == data.tipo_consulta,
            ConsultasModel.especialidad == data.especialidad,
            ConsultasModel.fecha_consulta == data.fecha_consulta
        ).first()
        
        if consulta_verificacion: 
            return JSONResponse(status_code=400, content={"message": "ya existe consulta"})
            
        resgistro = ConsultasModel(**data.dict())
        db.add(resgistro)
        db.commit()  
         
        return JSONResponse(status_code=201, content={"message": "Se ha registrado la consulta"})
    except SQLAlchemyError as error:
         return {"message": f"error al crear consulta: {error}"}
    finally:
        cursor.close()

#Put conectado a SQL
@router.put("/consultado/{id}", tags=["Consultas"])
async def actualizar( consulta: Consultas, id: int):
    try:
        db = Session()
        result = db.query(ConsultasModel).filter(ConsultasModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        result.id = consulta.id
        result.hoja_emergencia = consulta.hoja_emergencia
        result.expediente = consulta.expediente
        result.fecha_consulta = consulta.fecha_consulta
        result.hora = consulta.hora
        result.nombres = consulta.nombres
        result.apellidos = consulta.apellidos
        result.nacimiento = consulta.nacimiento
        result.edad = consulta.edad
        result.sexo = consulta.sexo
        result.dpi = consulta.dpi
        result.direccion = consulta.direccion
        result.acompa = consulta.acompa
        result.parente = consulta.parente
        result.telefono = consulta.telefono
        result.nota = consulta.nota
        result.especialidad = consulta.especialidad
        result.recepcion = consulta.recepcion
        result.fecha_egreso = consulta.fecha_egreso
        result.fecha_recepcion = consulta.fecha_recepcion
        result.tipo_consulta = consulta.tipo_consulta
    
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Actualización Realizada"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally: 
            print(f" ACTUALIZADO")
            
@router.patch("/recepcion/{id}", tags=["Consultas"])
async def recepcion(id: int, fecha_recep: str, recep: bool):
    try:
        db = Session()
        result = db.query(ConsultasModel).filter(ConsultasModel.id == id).first()
        if not result:
            raise HTTPException(status_code=404, detail="No encontrado")
        result.recepcion = recep  
        result.fecha_recepcion = fecha_recep  # Convertir a objeto date
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Actualización Realizada"})
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")
    finally:
        db.close()


#Delete conectado a SQL
@router.delete("/consulta/{id}", tags=["Consultas"])
async def eliminar_consulta(id: int):
    try:
        db = Session()
        result = db.query(ConsultasModel).filter(ConsultasModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Eliminado con exito"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally:
            print(f" ELIMINADO realizado")




