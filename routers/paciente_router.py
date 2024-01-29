from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func,select, desc
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, datetime, timedelta
from database import database
from routers.municipio import municipio
from additionals.adicionales import Desc_Civil,Desc_educacion, Desc_idiomas, Desc_nacionalidad, Desc_parentesco, Desc_people
from .enums import GeneroEnum, EstadoEnum
from database.database import Session
from models.paciente import PacienteModel, VistaPaciente, VistaPersona
import logging
from sqlalchemy.orm import lazyload
from typing import List
from uvicorn.config import LOGGING_CONFIG


 

router = APIRouter()
# Configura el logger de FastAPI
log = logging.getLogger("uvicorn.access")
log.setLevel(logging.WARNING)  # Puedes ajustar el nivel según tus necesidades
# Configura el formato del registro de acceso para mostrar solo la IP
LOGGING_CONFIG["formatters"]["default"]["fmt"] = '%(h)s - - [%(D)s] "%(r)s" %(s)s'


ultimo_expediente = 0

def actualizar_ultimo_exp():
    try:
        with Session() as db:
            max_exp = db.execute(select(func.max(PacienteModel.expediente))).scalar()
            return max_exp + 1 if max_exp is not None else 1
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


class Paciente(BaseModel):
    #id: int
    expediente: int
    nombre: str | None = None
    apellido: str| None = None
    dpi: int | None = None
    pasaporte: str | None = None
    sexo: GeneroEnum | None = None
    nacimiento: date | None = None
    nacionalidad: int| None = None
    depto_nac: int | None = None
    lugar_nacimiento: int | None = None
    estado_civil: int | None = None
    educacion: int | None = None
    pueblo: int | None = None
    idioma: int | None = None
    ocupacion: str | None = None
    municipio: int | None = None
    depto: int | None = None
    direccion: str | None = None
    telefono: str | None = None
    email: EmailStr | None = None
    padre: str | None = None
    madre: str | None = None
    responsable: str | None = None
    parentesco: int | None = None
    dpi_responsable: int | None = None
    telefono_responsable: int | None = None
    estado: str| None = None
    exp_madre: int | None = None
    created_by: str | None = None
    fechaDefuncion: str | None = None
    gemelo: str | None = None
    conyugue: str | None = None
    
    

    
#Get conectado a SQL

@router.get("/expediente")
async def obtener_ultimo_expediente():
    result = actualizar_ultimo_exp()
    return result

@router.get("/pacientes", tags=["Busquedas de Pacientes"])
def retornar_pacientes():
    try:
        result = (
            Session().query(VistaPaciente)
            .order_by(desc(VistaPaciente.id))
            .limit(1000)
            #.options(lazyload('*'))
            .all()
        )
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
    
@router.get("/pacientes_asc", tags=["Busquedas de Pacientes"])
def retornar_pacientes_ASC():
    try:
        result = (
            Session().query(VistaPaciente)
            .limit(1000)
            #.options(lazyload('*'))
            .all()
        )
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}   

@router.get("/personas", tags=["Busquedas de Pacientes"])
def retornar_personas():
    try:
        result = (
            Session().query(VistaPersona)
            .order_by(desc(VistaPersona.id))
            .limit(1000)
            #.options(lazyload('*'))
            .all()
        )
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
      
    
@router.get("/paciente/{exp}", tags=["Busquedas de Pacientes"])
async def obtener_paciente(exp: int):
    try:
        db = Session()
        result = db.query(PacienteModel).filter(PacienteModel.expediente == exp).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
    
        
@router.get("/pacienteId/", tags=["Busquedas de Pacientes"])
async def obtener_paciente_id(id: int):
    return buscar_id(id)

@router.get("/fecha_nacimiento/", tags=["Busquedas de Pacientes"])
async def buscar_nacimiento(fecha: str = Query( title="Fecha de nacimiento")):
    try:
        db  = Session()
        query = db.query(VistaPaciente)
        if fecha:
            query = query.filter(VistaPaciente.nacimiento == fecha)
        vista_paciente = query.all()
        return vista_paciente
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente:  {repr(error.erros()[0]['typpe'])}"}
    finally:
        db.close()

@router.get("/pacientefind/", tags=["Busquedas de Pacientes"])
async def buscar_paciente(nombre:str,apellido:str):
    return buscar_nombre(nombre,apellido)

@router.get("/dpi/", tags=["Busquedas de Pacientes"])
async def buscar_paciente(cui:int=Query(title="DPI")):
    try:
        db = Session()
        query = db.query(VistaPaciente)
        if cui:
            query = query.filter(VistaPaciente.dpi.ilike(f"%{cui}%"))
        result = query.all()
        return result
    except SQLAlchemyError as error:
        return {'message': f"Erro al consultar: {repr(error)}"}
    finally:
        db.close()
        


# Post conectado a SQL
@router.post("/paciente/", tags=["Pacientes"])
async def crear_paciente(Pacient: Paciente):
    try:
        with Session() as db:
            nuevo_paciente = PacienteModel(**Pacient.dict())
            db.add(nuevo_paciente)
            db.commit()
            actualizar_ultimo_exp()
        return JSONResponse(status_code=201, content={"message": "Se ha registrado el paciente"})
    except SQLAlchemyError as error:
        return {"message": f"Error al crear paciente: {error}"}

        
 
 
#Put conectado a SQL
@router.put("/paciente/{exp}", tags=["Pacientes"])
async def actualizar_paciente( Pacient: Paciente, exp: int):
    try:
        Db = Session()
        result = Db.query(PacienteModel).filter(PacienteModel.expediente == exp).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        #result.expediente = Pacient.expediente
        result.nombre = Pacient.nombre
        result.apellido = Pacient.apellido
        result.dpi = Pacient.dpi
        result.pasaporte = Pacient.pasaporte
        result.sexo = Pacient.sexo
        result.nacimiento = Pacient.nacimiento
        result.nacionalidad = Pacient.nacionalidad
        result.depto_nac = Pacient.depto_nac
        result.lugar_nacimiento = Pacient.lugar_nacimiento
        result.estado_civil = Pacient.estado_civil
        result.educacion = Pacient.educacion
        result.pueblo = Pacient.pueblo
        result.idioma = Pacient.idioma
        result.ocupacion = Pacient.ocupacion
        result.direccion = Pacient.direccion
        result.municipio = Pacient.municipio
        result.depto = Pacient.depto
        result.telefono = Pacient.telefono
        result.email = Pacient.email
        result.padre = Pacient.padre
        result.madre = Pacient.madre
        result.responsable = Pacient.responsable
        result.parentesco = Pacient.parentesco
        result.dpi_responsable = Pacient.dpi_responsable
        result.telefono_responsable = Pacient.telefono_responsable
        result.estado = Pacient.estado
        result.exp_madre = Pacient.exp_madre
        result.created_by = Pacient.created_by
        result.fechaDefuncion = Pacient.fechaDefuncion
        result.gemelo = Pacient.gemelo
        result.conyugue = Pacient.conyugue
        
        
      
        Db.commit()
        return JSONResponse(status_code=201, content={"message": "Actualización Realizada"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
    



#Delete conectado a SQL
@router.delete("/borrarpaciente/{id}", tags=["Pacientes"])
async def eliminar_paciente(id: int):
    try:
        db = Session()
        result = db.query(PacienteModel).filter(PacienteModel.id == id).first()
          # Busca el paciente por su ID
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        db.delete(result)  # Elimina el paciente
        db.commit()  # Realiza la confirmación de la transacción
        return JSONResponse(status_code=200, content={"message": "Eliminado con éxito"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
  



#Funciones de busqueda
def buscar_paciente(expe: int):
    try:
        Db = Session()
        result = Db.query(PacienteModel).filter(PacienteModel.expediente == expe).first()
        adicional = municipio(result.lugar_nacimiento)
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
   
   
def buscar_id(id: int):
    try:
        db = Session()
        result = db.query(PacienteModel).filter(PacienteModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})

        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
   
           
def buscar_nombre(nombre: str = Query(None, title="Nombre a buscar"), 
                  apellido: str = Query(None, title="Apellido a buscar")):
    try:
        db  = Session()
        
        query = db.query(VistaPaciente)
        if nombre:
            query = query.filter(VistaPaciente.nombre.ilike(f"%{nombre}%"))
        if apellido:
            query = query.filter(VistaPaciente.apellido.ilike(f"%{apellido}%"))
        vista_paciente = query.all()
        return vista_paciente
    
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
    


#Funcion para obtener tiempo ahora
now = datetime.now()


@router.get("/filtrarmujer/", tags=["Pacientes"])
async def filtro(
    id: int = Query(None, description="Id"),
    expediente: int = Query(None, description="Número de Expediente"),
    nombre: str = Query(None, description="Nombres"),
    apellido: str = Query(None, description="Apellidos"),
    dpi: str = Query(None, description="DPI"),
):
    try:
        db = Session()
        query = db.query(VistaPaciente).order_by(desc(VistaPaciente.id)).filter(VistaPaciente.sexo == "F")

        # Calcular la fecha de nacimiento mínima para ser mayor de 10 años
        fecha_nacimiento_minima = date.today() - timedelta(days=10 * 365)

        # Aplicar la condición de edad
        query = query.filter(VistaPaciente.nacimiento <= fecha_nacimiento_minima)

        if expediente is not None:
            query = query.filter(VistaPaciente.expediente == expediente)

        if nombre:
            query = query.filter(VistaPaciente.nombre.ilike(f"%{nombre}%"))

        if apellido:
            query = query.filter(VistaPaciente.apellido.ilike(f"%{apellido}%"))

        if dpi:
            query = query.filter(VistaPaciente.dpi.ilike(f"%{dpi}%"))

        result = query.limit(1000).all()
        return result
    except SQLAlchemyError as e:
        # Manejar errores específicos de SQLAlchemy, si es necesario
        return {"error": str(e)}
    except Exception as e:
        # Manejar otros errores inesperados
        return {"error": str(e)}
    
   