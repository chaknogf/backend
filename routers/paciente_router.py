from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func,select, desc
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, datetime
from database import database
from routers.municipio import municipio
from additionals.adicionales import Desc_Civil,Desc_educacion, Desc_idiomas, Desc_nacionalidad, Desc_parentesco, Desc_people
from .enums import GeneroEnum, EstadoEnum
from database.database import Session
from models.paciente import PacienteModel, VistaPaciente
import logging
from typing import List


 

router = APIRouter()


db = database.get_database_connection()
cursor = db.cursor()
logger = logging.getLogger(__name__)


ultimo_expediente = 0

def actualizar_ultimo_exp():
    try:
        Db = Session()
        max_exp = Db.execute(select(func.max(PacienteModel.expediente))).scalar()
        New_exp = max_exp + 1
        Db.close()
        return New_exp
    except SQLAlchemyError as error:
        return {"message": f"error al consultar paciente: {error}"}
    finally:
        print(f"Ultimo expediente generado no. {max_exp}")
            
            
cont: int 

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
    estado: EstadoEnum| None = None
    exp_madre: int | None = None
    created_by: str | None = None
    fechaDefuncion: str | None = None
    
    
class Created ( Paciente):
    created_at: str | None = None
    updated_at: str  | None = None

    
#Get conectado a SQL

@router.get("/expediente")
async def obtener_ultimo_expediente():
    result = actualizar_ultimo_exp()
    return result

@router.get("/pacientes", tags=["Busquedas de Pacientes"])
def retornar_pacientes():
    try:
        db  = Session()
        
        #result = db.query(VistaPaciente).order_by(desc(VistaPaciente.id)).limit(10000).all()
        result = db.query(VistaPaciente).order_by(desc(VistaPaciente.id)).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"error al consultar paciente: {error}"}
    finally:
        print(f"CONSULTADO")
    
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
    finally:
        print("CONSULTADO")
        
        
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
        print(f"id: {id} datetime:{now} CONSULTADO")
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
        print ("Consultado {cui}")
    


#Post conectado a SQL
@router.post("/paciente/", tags=["Pacientes"])
async def crear_paciente(Pacient: Paciente ):
    try:
        db = Session()
        nuevo_paciente = PacienteModel(**Pacient.dict())
        db.add(nuevo_paciente)
        db.commit()  
        actualizar_ultimo_exp()
        cursor.close()
        return JSONResponse(status_code=201, content={"message": "Se ha registrado el paciente"})
    except SQLAlchemyError as error:
         return {"message": f"error al crear paciente: {error}"}
        
 
 
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
        
        
      
        Db.commit()
        return JSONResponse(status_code=201, content={"message": "Actualización Realizada"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
    finally: 
            print(f"expediente: {exp} datetime: {now} ACTUALIZADO")



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
    finally:
        print("ELIMINADO realizado")



#Funciones de busqueda
def buscar_paciente(expe: int):
    try:
        Db = Session()
        result = Db.query(PacienteModel).filter(PacienteModel.expediente == expe).first()
        adicional = municipio(result.lugar_nacimiento)
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
         # Crear el diccionario adicional con la información extra
        adicional = {
            "municipio": municipio(result.lugar_nacimiento),
            "nation": Desc_nacionalidad(result.nacionalidad),
            "people": Desc_people(result.pueblo),
            "ecivil": Desc_Civil(result.estado_civil),
            "academic": Desc_educacion(result.educacion),
            "parents": Desc_parentesco(result.parentesco),
            "lenguage": Desc_idiomas(result.idioma)
                     
            }
         # Combinar los datos del paciente con la información adicional
        response_data = {**jsonable_encoder(result), **adicional}
        return JSONResponse(status_code=200, content=jsonable_encoder(response_data))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
    finally:
        print(f"Expediente: {expe} datetime:{now} CONSULTADO")
   
def buscar_id(id: int):
    try:
        db = Session()
        result = db.query(PacienteModel).filter(PacienteModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar paciente: {error}"}
    finally:
        print(f"id: {id} datetime:{now} CONSULTADO")
           
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
    finally:
        print(f"id: {id} datetime:{now} CONSULTADO")


#Funcion para obtener tiempo ahora
now = datetime.now()

