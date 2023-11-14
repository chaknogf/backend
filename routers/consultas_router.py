from fastapi import APIRouter, HTTPException, Query, Form
from pydantic import BaseModel
from typing import List
from datetime import date, datetime, time
from database.database import engine, Session, Base
from database import database
from models.consulta import ConsultasModel, VistaConsultas
from models.paciente import PacienteModel
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
    telefono: str | None = None
    nota: str | None = None
    especialidad: int | None = None
    servicio: int | None = None
    status: int | None = None
    fecha_egreso: date | None = None
    fecha_recepcion: datetime | None = None
    tipo_consulta: int | None = None
    prenatal: int | None = None
    lactancia: int | None = None
    dx: str | None = None
    folios: int | None = None
    medico: int | None = None
    archived_by: str | None = None
    created_by: str | None = None
    
    
    
   
    

    
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
   
ConsultasModel = ConsultasModel
@router.get("/filtro/", tags=["Consultas"])
async def filtro(
    id: int = Query(None, description="Número de id"),
    hoja_emergencia: str = Query(None, description="Hoja de Emergencia"),
    expediente: int = Query(None, description="Número de Expediente"),
    fecha_consulta: str = Query(None, description="Fecha de Consulta"),
    nombres: str = Query(None, description="Nombres"),
    apellidos: str = Query(None, description="Apellidos"),
    dpi: str = Query(None, description="DPI"),
    fecha_egreso: str = Query(None, description="Fecha de Egreso"),
    tipo_consulta: int = Query(None, description="Tipo de consulta"),
    status: int = Query(None, description="status"),
    fecha_recepcion: str = Query(None, description="fecha recepcion"),
    no_es: int =Query(None, description="No es consulta"),
    
                ):
    try:
        
        db = Session()
        query = db.query(ConsultasModel)

        # Agregar condiciones para los filtros con coincidencias parciales
        if id is not None:
            query = query.filter(ConsultasModel.id == id)
            
        if hoja_emergencia:
            query = query.filter(ConsultasModel.hoja_emergencia == hoja_emergencia)

        if expediente is not None:
            query = query.filter(ConsultasModel.expediente == expediente)

        if fecha_consulta:
            query = query.filter(ConsultasModel.fecha_consulta.ilike(f"%{fecha_consulta}%"))

        if nombres:
            query = query.filter(ConsultasModel.nombres.ilike(f"%{nombres}%"))

        if apellidos:
            query = query.filter(ConsultasModel.apellidos.ilike(f"%{apellidos}%"))

        if dpi:
            query = query.filter(ConsultasModel.dpi.ilike(f"%{dpi}%"))

        if fecha_egreso:
            query = query.filter(ConsultasModel.fecha_egreso == fecha_egreso)
            
        if tipo_consulta:
            query = query.filter(ConsultasModel.tipo_consulta == tipo_consulta)
            
        if  no_es:
            query = query.filter(ConsultasModel.tipo_consulta != no_es)
            
        if fecha_recepcion:
            query = query.filter(func.DATE_FORMAT(ConsultasModel.fecha_recepcion, '%Y-%m-%d').ilike(f"%{fecha_recepcion}%"))
            
        if status:
            query = query.filter(ConsultasModel.status == status)

        result = query.all()
        return result
    except Exception as e:
        return {"error": str(e)}    
        
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
        
@router.get("/exp/{exp}", tags=["Buscar Consulta"])
async def expedienteBuscar(exp: int):
    try:
        db = Session()
        result = db.query(ConsultasModel).filter(ConsultasModel.expediente == exp).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
    finally:
        print("CONSULTADO")   

@router.get("/hoja/{hoja}", tags=["Buscar Consulta"])
async def hojaBuscar(hoja: str):
    try:
        db = Session()
        result = db.query(ConsultasModel).filter(ConsultasModel.hoja_emergencia == hoja).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
    finally:
        print("CONSULTADO")   


@router.get("/nombre/", tags=["Buscar Consulta"])
async def nombreBuscar(nombre: str = Query(None, title="Nombre a buscar"), 
                  apellido: str = Query(None, title="Apellido a buscar")):
    try:
        db  = Session()
        
        query = db.query(ConsultasModel)
        if nombre:
            query = query.filter(ConsultasModel.nombres.ilike(f"%{nombre}%"))
        if apellido:
            query = query.filter(ConsultasModel.apellidos.ilike(f"%{apellido}%"))
        vista_paciente = query.all()
        return vista_paciente
    
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
    finally:
        print(f"id: {id} datetime:{now} CONSULTADO")  
        
@router.get("/cui/{cui}", tags=["Buscar Consulta"])
async def cuiBuscar(cui:str):
    try:
        db = Session()
        query = db.query(ConsultasModel)
        if cui:
            query = query.filter(ConsultasModel.dpi == cui)
        result = query.all()
        return result
    except SQLAlchemyError as error:
        return {'message': f"Erro al consultar: {repr(error)}"}
    finally:
        db.close()
        print ("Consultado {cui}")

@router.get("/recepcion/", tags=["Buscar Consulta"])
async def recepcionBuscar(recepcion: str = Query(None, title="Recepcion"), 
                  fecha: str = Query(None, title="Fecha de Recepcion")):
    try:
        db  = Session()
        
        query = db.query(ConsultasModel)
        if recepcion:
            query = query.filter(ConsultasModel.recepcion == recepcion)
        if fecha:
            query = query.filter(ConsultasModel.fecha_recepcion == fecha)
        vista_paciente = query.all()
        return vista_paciente
    
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
    finally:
        print(f"id: {id} datetime:{now} CONSULTADO") 

@router.get("/egresos/", tags=["Buscar Consulta"])
async def egresosBuscar(fecha_inicio: str = Query(None, title="Fecha inicial"),
    fecha_final: str = Query(None, title="Fecha final"),
):
    try:
        db = Session()
        query = db.query(ConsultasModel)

        if fecha_inicio and fecha_final:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d")
            query = query.filter(ConsultasModel.fecha_egreso.between(fecha_inicio, fecha_final))
        elif fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            query = query.filter(ConsultasModel.fecha_egreso >= fecha_inicio)
        elif fecha_final:
            fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d")
            query = query.filter(ConsultasModel.fecha_egreso <= fecha_final)

        consultas = query.all()
        return consultas
    except Exception as e:
        return {"error": f"Ocurrió un error: {e}"}
    finally:
        db.close()

@router.get("/consult/", tags=["Consultas"])
async def consult(tipo: int):
    try: 
        db = Session()
        NoEncontrado = []
        result = (
            db.query(ConsultasModel)
            .filter(ConsultasModel.tipo_consulta == tipo)
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
@router.post("/coex/",response_model=consultas, tags=["Consultas"])
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
        
@router.post("/emergencia/",response_model=consultas, tags=["Consultas"])
async def registrar(data: Consultas ):
    try:
        db = Session()
        # verificar si ya existe una consulta
        consulta_verificacion = db.query(ConsultasModel).filter(
            ConsultasModel.hoja_emergencia == data.hoja_emergencia, 
            
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
        result.servicio = consulta.servicio
        result.status = consulta.status
        result.fecha_egreso = consulta.fecha_egreso
        result.fecha_recepcion = consulta.fecha_recepcion
        result.tipo_consulta = consulta.tipo_consulta
        result.prenatal = consulta.prenatal
        result.lactancia = consulta.lactancia
        result.dx = consulta.dx
        result.folios = consulta.folios
        result.created_by = consulta.created_by
        result.archived_by = consulta.archived_by
        result.updated_at = consulta.updated_at
    
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




