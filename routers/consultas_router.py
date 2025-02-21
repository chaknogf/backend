from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime, time
from database.database import Session
from sqlalchemy.orm import  lazyload 
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, desc
from models.paciente import PacienteModel
from sqlalchemy.orm import Session as SQLAlchemySession
from models.consulta import ConsultasModel, VistaConsultas
from database import database

router = APIRouter()

# Dependencia para obtener sesión de base de datos
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

class Consultas(BaseModel):
    id: int
    hoja_emergencia: Optional[str] = None
    expediente: Optional[int] = None
    fecha_consulta: Optional[date] = None
    hora: Optional[time] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    nacimiento: Optional[date] = None
    edad: Optional[str] = None
    sexo: Optional[str] = None
    dpi: Optional[str] = None
    direccion: Optional[str] = None
    acompa: Optional[str] = None
    parente: Optional[int] = None
    telefono: Optional[str] = None
    nota: Optional[str] = None
    especialidad: Optional[int] = None
    servicio: Optional[int] = None
    status: Optional[int] = None
    fecha_egreso: Optional[date] = None
    fecha_recepcion: Optional[datetime] = None
    tipo_consulta: Optional[int] = None
    prenatal: Optional[int] = None
    lactancia: Optional[int] = None
    dx: Optional[str] = None
    folios: Optional[int] = None
    medico: Optional[str] = None
    archived_by: Optional[str] = None
    created_by: Optional[str] = None
    bomberos: Optional[bool] = None
    transito: Optional[bool] = None
    arma_blanca: Optional[bool] = None
    arma_fuego: Optional[bool] = None
    estudiante_publica: Optional[bool] = None
    accidente_laboral: Optional[bool] = None
    personal_hospital: Optional[bool] = None
    reserva: Optional[bool] = None

@router.get("/consultas/", tags=["Consultas"])
async def obtener_consultas(db: SQLAlchemySession = Depends(get_db)):
    try:
        # Consultar solo las últimas 1000 consultas ordenadas por ID descendente
        result = db.query(VistaConsultas).order_by(desc(VistaConsultas.id)).limit(500).all()
        
        if not result:
            return JSONResponse(status_code=200, content=jsonable_encoder([]))

        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")

@router.get("/filtro/", tags=["Consultas"])
async def filtro(
    id: Optional[int] = Query(None, description="Número de id"),
    hoja_emergencia: Optional[str] = Query(None, description="Hoja de Emergencia"),
    expediente: Optional[int] = Query(None, description="Número de Expediente"),
    fecha_consulta: Optional[str] = Query(None, description="Fecha de Consulta"),
    nombres: Optional[str] = Query(None, description="Nombres"),
    apellidos: Optional[str] = Query(None, description="Apellidos"),
    dpi: Optional[str] = Query(None, description="DPI"),
    fecha_egreso: Optional[str] = Query(None, description="Fecha de Egreso"),
    tipo_consulta: Optional[int] = Query(None, description="Tipo de consulta"),
    status: Optional[int] = Query(None, description="Status"),
    fecha_recepcion: Optional[str] = Query(None, description="Fecha de Recepción"),
    no_es: Optional[int] = Query(None, description="No es consulta"),
    db: SQLAlchemySession = Depends(get_db)
):
    try:
        query = db.query(ConsultasModel)

        # Aplicar filtros de manera condicional
        if id is not None:
            query = query.filter(ConsultasModel.id == id)

        if hoja_emergencia:
            query = query.filter(ConsultasModel.hoja_emergencia.ilike(f"%{hoja_emergencia}%"))

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

        if no_es:
            query = query.filter(ConsultasModel.tipo_consulta != no_es)

        if fecha_recepcion:
            query = query.filter(func.DATE_FORMAT(ConsultasModel.fecha_recepcion, '%Y-%m-%d').ilike(f"%{fecha_recepcion}%"))

        if status is not None:
            query = query.filter(ConsultasModel.status == status)

        # Ordenar y limitar resultados
        query = query.order_by(desc(ConsultasModel.id)).limit(500)

        # Obtener resultados
        result = query.all()

        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")
    
        
@router.get("/consulta/", tags=["Consultas"])
async def buscar_id(id: int, db: SQLAlchemySession = Depends(get_db)):
    try:
        # Consulta la consulta por id
        consulta = db.query(ConsultasModel).filter(ConsultasModel.id == id).first()
        
        if not consulta:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})

        # Convertir las fechas a un formato adecuado si es necesario
        created_at_str = consulta.created_at.strftime("%Y-%m-%d %H:%M:%S") if consulta.created_at else None
        updated_at_str = consulta.updated_at.strftime("%Y-%m-%d %H:%M:%S") if consulta.updated_at else None

        # Agregar created_at y updated_at al diccionario de resultados
        consulta_dict = consulta.__dict__
        consulta_dict["created_at"] = created_at_str
        consulta_dict["updated_at"] = updated_at_str

        return JSONResponse(status_code=200, content=jsonable_encoder(consulta_dict))

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")

@router.get("/consulta/servicio/", tags=["Consultas"])
async def consultas_servicio(fecha: str, tipo: int, db: SQLAlchemySession = Depends(get_db)):
    try:
        # Obtener consultas con información del paciente
        result = (
            db.query(ConsultasModel, PacienteModel.nombre, PacienteModel.apellido)
            .join(PacienteModel, ConsultasModel.pacientes)
            .filter(ConsultasModel.fecha_consulta == fecha, ConsultasModel.tipo_consulta == tipo)
            .all()  # Obtener solo el primer resultado
        )
        
        if not result:
            return JSONResponse(status_code=200, content=jsonable_encoder([]))

        consulta, name, lastname = result  # Desempaquetar la tupla
        
        consulta_dict = consulta.__dict__
        consulta_dict["name"] = name
        consulta_dict["lastname"] = lastname
        
        return JSONResponse(status_code=200, content=jsonable_encoder(consulta_dict))

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")
        
@router.get("/consultando/", tags=["Consultas"])
async def consultas(fecha: str, tipo: int, especialidad: int, db: SQLAlchemySession = Depends(get_db)):
    try:
        result = (
            db.query(ConsultasModel)
            .filter(ConsultasModel.fecha_consulta == fecha, ConsultasModel.tipo_consulta == tipo, ConsultasModel.especialidad == especialidad)
            .all()
        )
        
        if not result:
            return JSONResponse(status_code=200, content=jsonable_encoder([]))

        # Convertir los resultados en una lista de diccionarios
        consultas_list = [consulta.__dict__ for consulta in result]
        
        return JSONResponse(status_code=200, content=jsonable_encoder(consultas_list))

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")

@router.get("/exp/{exp}", tags=["Buscar Consulta"])
async def expediente_buscar(exp: int, db: SQLAlchemySession = Depends(get_db)):
    try:
        result = db.query(ConsultasModel).filter(ConsultasModel.expediente == exp).first()
        
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar expediente: {error}")

@router.get("/hoja/{hoja}", tags=["Buscar Consulta"])
async def hoja_buscar(hoja: str, db: SQLAlchemySession = Depends(get_db)):
    try:
        result = db.query(ConsultasModel).filter(ConsultasModel.hoja_emergencia == hoja).first()
        
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar hoja de emergencia: {error}")


@router.get("/nombre/", tags=["Buscar Consulta"])
async def nombre_buscar(nombre: str = Query(None, title="Nombre a buscar"), 
                         apellido: str = Query(None, title="Apellido a buscar"),
                         db: SQLAlchemySession = Depends(get_db)):
    try:
        query = db.query(ConsultasModel)
        
        if nombre:
            query = query.filter(ConsultasModel.nombres.ilike(f"%{nombre}%"))
        if apellido:
            query = query.filter(ConsultasModel.apellidos.ilike(f"%{apellido}%"))
        
        vista_paciente = query.all()
        
        if not vista_paciente:
            return JSONResponse(status_code=404, content={"message": "No se encontraron resultados"})
        
        return JSONResponse(status_code=200, content=jsonable_encoder(vista_paciente))
    
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar paciente: {error}")

@router.get("/cui/{cui}", tags=["Buscar Consulta"])
async def cui_buscar(cui: str, db: SQLAlchemySession = Depends(get_db)):
    try:
        query = db.query(ConsultasModel)
        
        if cui:
            query = query.filter(ConsultasModel.dpi == cui)
        
        result = query.first()  # Usamos `first()` ya que solo esperamos un resultado
        
        if not result:
            return JSONResponse(status_code=404, content={"message": "No se encontró el paciente"})
        
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar CUI: {error}")

@router.get("/recepcion/", tags=["Buscar Consulta"])
async def recepcion_buscar(recepcion: str = Query(None, title="Recepcion"), 
                           fecha: str = Query(None, title="Fecha de Recepcion"),
                           db: SQLAlchemySession = Depends(get_db)):
    try:
        query = db.query(ConsultasModel)
        
        if recepcion:
            query = query.filter(ConsultasModel.recepcion == recepcion)
        if fecha:
            query = query.filter(ConsultasModel.fecha_recepcion == fecha)
        
        vista_paciente = query.all()
        
        if not vista_paciente:
            return JSONResponse(status_code=404, content={"message": "No se encontraron resultados"})
        
        return JSONResponse(status_code=200, content=jsonable_encoder(vista_paciente))
    
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar recepcion: {error}")

@router.get("/egresos/", tags=["Buscar Consulta"])
async def egresos_buscar(fecha_inicio: str = Query(None, title="Fecha inicial"),
                          fecha_final: str = Query(None, title="Fecha final"),
                          db: SQLAlchemySession = Depends(get_db)):
    try:
        query = db.query(ConsultasModel)

        # Procesamiento de las fechas para el filtro
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
        
        if not consultas:
            return JSONResponse(status_code=404, content={"message": "No se encontraron resultados"})

        return JSONResponse(status_code=200, content=jsonable_encoder(consultas))

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar egresos: {error}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")

@router.get("/consult/", tags=["Consultas"])
async def consult(tipo: int, db: SQLAlchemySession = Depends(get_db)):
    try: 
        result = (
            db.query(ConsultasModel)
            .filter(ConsultasModel.tipo_consulta == tipo)
            .order_by(desc(ConsultasModel.id))  # Ordena por id en orden descendente
            .limit(1000)  # Ajusta el límite según tus necesidades
            .options(lazyload('*'))  # Si es necesario cargar relaciones de manera diferida
            .all()
        )
        
        if not result:
            return JSONResponse(status_code=200, content={"message": "No se encontraron resultados"})
        
        # Convertir los resultados en una lista de diccionarios
        consulta_dict = [consulta.__dict__ for consulta in result]
        
        return JSONResponse(status_code=200, content=jsonable_encoder(consulta_dict))

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")
    
@router.get("/emerg/", tags=["Consultas"])
async def consult_3(db: SQLAlchemySession = Depends(get_db)):
    try:
        result = (
            db.query(ConsultasModel)
            .filter(ConsultasModel.tipo_consulta == 3)
            .order_by(desc(ConsultasModel.id))  # Ordena por id en orden descendente
            .limit(500)  # Ajusta el límite según tus necesidades
            .options(lazyload('*'))  # Si es necesario cargar relaciones de manera diferida
            .all()
        )

        if not result:
            return JSONResponse(status_code=200, content={"message": "No se encontraron resultados"})

        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar: {error}")

@router.post("/coex/", response_model=Consultas, tags=["Consultas"])
async def crear(data: Consultas, db: SQLAlchemySession = Depends(get_db)):
    try:
        # Verificar si ya existe una consulta con los mismos datos
        consulta_verificacion = db.query(ConsultasModel).filter(
            ConsultasModel.expediente == data.expediente, 
            ConsultasModel.tipo_consulta == data.tipo_consulta,
            ConsultasModel.especialidad == data.especialidad,
            ConsultasModel.fecha_consulta == data.fecha_consulta
        ).first()
        
        if consulta_verificacion: 
            return JSONResponse(status_code=400, content={"message": "Ya existe una consulta con los mismos datos"})
        
        # Registrar la nueva consulta
        registro = ConsultasModel(**data.dict())
        db.add(registro)
        db.commit()  
         
        return JSONResponse(status_code=201, content={"message": "Se ha registrado la consulta exitosamente"})

    except SQLAlchemyError as error:
         raise HTTPException(status_code=500, detail=f"Error al crear la consulta: {error}")
        
# Endpoint POST para registrar una consulta
@router.post("/emergencia/", response_model=Consultas, tags=["Consultas"])
async def registrar(data: Consultas, db: SQLAlchemySession = Depends(get_db)):
    try:
        # Verificar si ya existe una consulta con el mismo número de hoja de emergencia
        consulta_verificacion = db.query(ConsultasModel).filter(
            ConsultasModel.hoja_emergencia == data.hoja_emergencia
        ).first()

        if consulta_verificacion:
            return JSONResponse(status_code=400, content={"message": "Ya existe una consulta con esa hoja de emergencia."})
        
        # Registrar nueva consulta
        registro = ConsultasModel(**data.dict())
        db.add(registro)
        db.commit()  
         
        return JSONResponse(status_code=201, content={"message": "Consulta registrada exitosamente."})
    
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al registrar la consulta: {error}")

# Endpoint PUT para actualizar una consulta
@router.put("/consultado/{id}", tags=["Consultas"])
async def actualizar(consulta: Consultas, id: int, db: SQLAlchemySession = Depends(get_db)):
    try:
        # Buscar la consulta por ID
        result = db.query(ConsultasModel).filter(ConsultasModel.id == id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Consulta no encontrada.")
        
        # Actualizar los campos de la consulta
        for key, value in consulta.dict(exclude_unset=True).items():
            setattr(result, key, value)
        
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Consulta actualizada exitosamente."})
    
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la consulta: {error}")

# Endpoint PATCH para actualizar solo ciertos campos (como la recepción)
@router.patch("/recepcion/{id}", tags=["Consultas"])
async def recepcion(id: int, fecha_recep: str, recep: bool, db: SQLAlchemySession = Depends(get_db)):
    try:
        # Buscar la consulta por ID
        result = db.query(ConsultasModel).filter(ConsultasModel.id == id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Consulta no encontrada.")
        
        # Actualizar los campos de recepción
        result.recepcion = recep  
        result.fecha_recepcion = fecha_recep  # Asegúrate de que la fecha esté en el formato correcto
        db.commit()
        
        return JSONResponse(status_code=200, content={"message": "Datos de recepción actualizados exitosamente."})
    
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al actualizar los datos de recepción: {error}")

@router.delete("/consulta/{id}", tags=["Consultas"])
async def eliminar_consulta(id: int, db: SQLAlchemySession = Depends(get_db)):
    try:
        # Buscar la consulta por ID
        result = db.query(ConsultasModel).filter(ConsultasModel.id == id).first()
        
        # Si no se encuentra la consulta, retornar 404
        if not result:
            raise HTTPException(status_code=404, detail="Consulta no encontrada.")
        
        # Eliminar la consulta
        db.delete(result)
        db.commit()
        
        # Retornar respuesta exitosa
        return JSONResponse(status_code=200, content={"message": "Consulta eliminada con éxito."})
    
    except SQLAlchemyError as error:
        # Si ocurre un error en la base de datos, retornamos una respuesta de error
        raise HTTPException(status_code=500, detail=f"Error al eliminar consulta: {error}")
    finally:
        # En este caso no es necesario cerrar la sesión manualmente si usas Depends
        print(f"Consulta con id {id} eliminada.")



