from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date, datetime, timedelta
from database.database import engine, Session, Base
from database import database
from models.citas import CitasModel , VistaCitas
from models.paciente import PacienteModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

router = APIRouter()

db = database.get_database_connection()
cursor = db.cursor()

now = datetime.now()

class Citas(BaseModel):
    id: int
    fecha: date | None = None
    expediente: int | None = None
    especialidad: int  | None = None
    fecha_cita: date | None = None
    nota: str | None = None
    tipo: int | None = None
    lab: int | None = None
    fecha_lab: date | None = None
    created_by: str | None = None

hoy = date.today()
# Convertir el objeto date a una cadena de texto con formato "YYYY-MM-DD"
cadena_fecha = hoy.strftime("%Y-%m-%d")


#Get conectado a SQL
@router.get("/citas/", tags=["Citas"])
async def obtener_todas_citas():
    try:
        db = Session()
        result = (
            db.query(CitasModel, func.concat(PacienteModel.nombre, " ", PacienteModel.apellido).label("name"))
            .join(CitasModel.pacientes)
            .all()
        )
        
        citas_con_names = [
            {**cita.__dict__, "name": name} for cita, name in result
        ]
            
        print(f"** datetime: {now} CONSULTA - GET **")
        return JSONResponse(status_code=200, content=jsonable_encoder(citas_con_names))
    except SQLAlchemyError as error:
        return HTTPException(status_code=500, detail=f"error al consultar citas: {error}")
    finally:
        db.close()
        print(f"CONSULTADO datetime: {now}")

#Get conectados a SQL
@router.get("/cita/expediente/{cita_exp}", response_model=Citas, tags=["Citas"])
async def obtener_cita_exp(value: int):
   return buscar_exp(value)

@router.get("/cita/hoy/", response_model=Citas, tags=["Citas"])
async def obtener_citas_hoy():
    hoy = date.today()
    return buscar_fecha(hoy)

@router.get("/cita/id/", tags=["Citas"])
async def cita_id(value: int):
    return buscar_citaId(value)


@router.get("/cita/fecha/", response_model=Citas, tags=["Citas"])
async def obtener_cita_fecha(value: date):
   return buscar_fecha(value)

@router.get("/cita/servicio/", tags=["Citas"])
def cantidad_citas_diarias(especialidad: int):
    try:
        db = Session()
         # Consulta la vista filtrando por especialidad
        citas = db.query(VistaCitas).filter_by(especialidad=especialidad).all()
        
        
        if not citas:
            raise HTTPException(status_code=404, detail="No se encontraron citas para esta especialidad.")
        
        citas_dict = [{"id": cita.id, "especialidad": cita.especialidad, "dia": cita.dia, "total_citas": cita.total_citas} for cita in citas]
    
        return JSONResponse(status_code=200, content=citas_dict)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar citas: {error}")
    finally:
        db.close()
        

@router.get("/cita_lab/{fecha_cita}", tags=["Citas"])
async def cita_lab(fecha_cita: str):
    #parsear el input
    input_fecha = datetime.strptime(fecha_cita, '%Y-%m-%d').date()
    
    #calculo previo 2 dias habiles
    dia_habil = pd.date_range(end=input_fecha - timedelta(days=2), periods=2, freq='B').to_pydatetime().tolist()
    
    dos_dias_habiles_antes = dia_habil[-1].date()
    
    return {"fecha": str(dos_dias_habiles_antes)}
    


#Post conectado a SQL
@router.post("/cita/", response_model=Citas, tags=["Citas"])
async def crear_cita(cita: Citas):
    try:
        db = Session()
        # Verificar si ya existen 10 citas para la misma especialidad en la misma fecha
        citas_del_dia = db.query(CitasModel).filter(
            CitasModel.especialidad == cita.especialidad,
            CitasModel.fecha == cita.fecha,
            CitasModel.tipo == cita.tipo
            
        ).count()
        
        if citas_del_dia > 9:
            return JSONResponse(status_code=400, content={"message": "Ya se han agendado 10 citas para esta especialidad en esta fecha"})
        
        # Verificar si ya existe una cita con la misma especialidad en la misma fecha
        cita_existente = db.query(CitasModel).filter(
            CitasModel.expediente == cita.expediente,
            CitasModel.especialidad == cita.especialidad,
            CitasModel.fecha == cita.fecha,
            #CitasModel.tipo ==cita.tipo
            
        ).first()
        
        if cita_existente:
            return JSONResponse(status_code=400, content={"message": "Ya existe una cita en la misma especialidad en esta fecha"})
        
        nueva_cita = CitasModel(**cita.dict())
        db.add(nueva_cita)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Se ha registrado una nueva cita"})
    except SQLAlchemyError as error:
        return {"message": f"Error al agendar cita: {error}"}
    
@router.post("/citaespecial/", response_model=Citas, tags=["Citas"])
async def cita_especial(cita: Citas):
    try:
        db = Session()
        # Verificar si ya existen 10 citas para la misma especialidad en la misma fecha
        citas_del_dia = db.query(CitasModel).filter(
            CitasModel.especialidad == cita.especialidad,
            CitasModel.fecha == cita.fecha
        ).count()
        
        if citas_del_dia >3:
            return JSONResponse(status_code=400, content={"message": "Ya se han agendado 3 citas especiales para esta especialidad en esta fecha"})
        
        # Verificar si ya existe una cita con la misma especialidad en la misma fecha
        cita_existente = db.query(CitasModel).filter(
            CitasModel.expediente == cita.expediente,
            CitasModel.especialidad == cita.especialidad,
            CitasModel.fecha == cita.fecha,
            CitasModel.tipo ==cita.tipo
            
        ).first()
        
        if cita_existente:
            return JSONResponse(status_code=400, content={"message": "Ya existe una cita en la misma especialidad en esta fecha"})
        
        nueva_cita = CitasModel(**cita.dict())
        db.add(nueva_cita)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Se ha registrado una nueva cita"})
    except SQLAlchemyError as error:
        return {"message": f"Error al agendar cita: {error}"}

   
@router.put("/citas/{id}", response_model=Citas, tags=["Citas"])
async def actualizar_cita(cita: Citas, id: int):
    try:
        Db = Session()
        result = Db.query(CitasModel).filter(CitasModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        result.nota = cita.nota
        result.tipo = cita.tipo
        result.lab = cita.lab
        result.fecha_lab = cita.fecha_lab
        result.fecha_cita = cita.fecha_cita
        result.created_by = cita.created_by
        Db.commit()
        return JSONResponse(status_code=201, content={"message": "Actualización realizada"})
    except SQLAlchemyError as error:
        return {"message": f"Error al actualizar cita: {error}"}
    finally: 
            print(f"cita: {id} datetime: {now} ACTUALIZADO")
        

@router.delete("/borrar/{id}", response_model=Citas, tags=["Citas"])
async def eliminar_cita(id: int):
    try:
        Db = Session()
        result = Db.query(CitasModel).filter(CitasModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        Db.delete(result)
        Db.commit()
        return JSONResponse(status_code=200, content={"message": "Eliminado con exito"})
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar cita: {error}"}
    finally:
            print(f"Cita: {id} datetime:{now} ELIMINADO realizado")

def buscar_exp(data: int):
    try:
        db = Session()
        result = (
            db.query(CitasModel, func.concat(PacienteModel.nombre, " ", PacienteModel.apellido).label("name"))
            .join(CitasModel.pacientes)
            .filter(CitasModel.expediente == data)
            .first()
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="No encontrado")
        
        cita, name = result  # Desempaquetar la tupla
        
        cita_dict = cita.__dict__
        cita_dict["name"] = name
        
        print(f"expediente: {data} datetime: {now} CONSULTADO")
        return JSONResponse(status_code=200, content=jsonable_encoder(cita_dict))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar paciente: {error}")
    finally:
        db.close()
      
        

        
def buscar_fecha(data: date):
    try:
        db = Session()
        result = (
            db.query(CitasModel, func.concat(PacienteModel.nombre, " ", PacienteModel.apellido).label("name"))
            .join(CitasModel.pacientes)
            .filter(CitasModel.fecha == data)
            .all()
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="No hay citas registrasdas para esta fecha")
        
        cita_dict = [
            {**cita.__dict__, "name": name} for cita, name in result
        ]
        
        print(f"expediente: {data} datetime: {now} CONSULTADO")
        return JSONResponse(status_code=200, content=jsonable_encoder(cita_dict))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar paciente: {error}")
    finally:
        db.close()
        
        
def buscar_especialidad(data: int):
    try:
        db = Session()
        result = (
            db.query(CitasModel, func.concat(PacienteModel.nombre, " ", PacienteModel.apellido).label("name"))
            .join(CitasModel.pacientes)
            .filter(CitasModel.especialidad == data)
            .all()
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="No hay citas registrasdas para esta fecha")
        
        cita_dict = [
            {**cita.__dict__, "name": name} for cita, name in result
        ]
        
        print(f"expediente: {data} datetime: {now} CONSULTADO")
        return JSONResponse(status_code=200, content=jsonable_encoder(cita_dict))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar paciente: {error}")
    finally:
        db.close()
        
def buscar_citaId(id: int):
    try:
        db = Session()
        NoEncontrado = {
            "id": None,
            "fecha": None,
            "expediente": None,
            "especialidad": None,
            "cirugia_programada": None,
            "nota": None,
            "tipo": None
        }
        result = (
            db.query(CitasModel, func.concat(PacienteModel.nombre, " ", PacienteModel.apellido).label("name"))
            .join(CitasModel.pacientes)
            .filter(CitasModel.id == id)
            .first()
        )
        
        if not result:
            return JSONResponse(status_code=200, content=jsonable_encoder(NoEncontrado))
        
        cita, name = result  # Desempaquetar la tupla
        
        cita_dict = cita.__dict__
        cita_dict["name"] = name
        
        print(f"expediente: {id} datetime: {datetime.now()} CONSULTADO")
        return JSONResponse(status_code=200, content=jsonable_encoder(cita_dict))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar paciente: {error}")
    finally:
        db.close()

@router.get("/cita/tabla/", tags=["Citas"])
def tablaCitas(fecha: str, especialidad: int, tipo: int):
    try:
        db = Session()
        NoEncontrado = []
        result = (
            db.query(CitasModel, func.concat(PacienteModel.nombre, " ", PacienteModel.apellido).label("name"))
            .join(CitasModel.pacientes)
            .filter(CitasModel.fecha == fecha , CitasModel.especialidad == especialidad, CitasModel.tipo == tipo)
            .all()
            )
            
        if not result:
            return JSONResponse(status_code=202, content=jsonable_encoder(NoEncontrado))
                
        cita_dict = [
            {**cita.__dict__, "name": name} for cita, name in result
        ]
            
        print(f"expediente: {fecha} datetime: {now} CONSULTADO")
        return JSONResponse(status_code=200, content=jsonable_encoder(cita_dict))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar paciente: {error}")
    finally:
        db.close()    
        
        
@router.get("/citasVigentes", tags=["Citas"])
def Vigentes(especialidad: int, tipo: int):
    try:
        db = Session()
         # Consulta la vista filtrando por especialidad
        citas = db.query(VistaCitas).filter(VistaCitas.dia >= cadena_fecha, VistaCitas.especialidad == especialidad, VistaCitas.tipo == tipo).all()
        
        
        if not citas:
            raise HTTPException(status_code=404, detail="No se encontraron citas para esta especialidad.")
        
        citas_dict = [{"id": cita.id, "especialidad": cita.especialidad, "dia": cita.dia, "total_citas": cita.total_citas} for cita in citas]
    
        return JSONResponse(status_code=200, content=citas_dict)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar citas: {error}")
    finally:
        db.close()
        
@router.get("/citas_disponible", tags=["Citas"])
def Vigentes(especialidad: int, tipo: int, fecha: str):
    try:
        db = Session()
         # Consulta la vista filtrando por especialidad
        citas = db.query(VistaCitas).filter(VistaCitas.dia == fecha, VistaCitas.especialidad == especialidad, VistaCitas.tipo == tipo).all()
        
        
        if not citas:
            raise HTTPException(status_code=404, detail="No se encontraron citas para esta especialidad.")
        
        citas_dict = [{"id": cita.id, "especialidad": cita.especialidad, "dia": cita.dia, "total_citas": cita.total_citas} for cita in citas]
    
        return JSONResponse(status_code=200, content=citas_dict)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar citas: {error}")
    finally:
        db.close()
        
@router.get("/citashoy/", tags=["Citas"])
def buscar_fecha():
    try:
        db = Session()
        result = (
            db.query(CitasModel,(PacienteModel.nombre).label("nombres"), (PacienteModel.apellido).label("apellidos"))
            .join(CitasModel.pacientes)
            .filter(CitasModel.fecha == hoy)
            .all()
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="No hay citas registrasdas para esta fecha")
        
        cita_dict = [
            {**cita.__dict__, "nombres": nombres, "apellidos": apellidos} for cita, nombres, apellidos in result
        ]
        
        
        return JSONResponse(status_code=200, content=jsonable_encoder(cita_dict))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar paciente: {error}")
    finally:
        db.close()
        
