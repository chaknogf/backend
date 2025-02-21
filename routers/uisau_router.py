from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from datetime import datetime, date
from database.database import Session
from models.uisau import uisauModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session as SQLAlchemySession

router = APIRouter()
now = datetime.now()

# Definir esquema con Pydantic
class UisauSchema(BaseModel):
    id: int
    consulta_id: int
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
    receta_por: str | None = None
    id_consulta: int | None = None
    created_by: str | None = None
    update_by: str | None = None
    shampoo: bool | None = None
    toalla: bool | None = None
    peine: bool | None = None
    jabon: bool | None = None
    cepillo_dientes: bool | None = None
    pasta_dental: bool | None = None
    sandalias: bool | None = None
    agua: bool | None = None
    papel: bool | None = None
    panales: bool | None = None
    dxA: str | None = None
    dxB: str | None = None
    dxC: str | None = None
    dxD: str | None = None
    dxE: str | None = None
    toalla_humeda: bool | None = None
    ropa_bebe: bool | None = None
    ropa_interior: bool | None = None
    panal_bebe: bool | None = None
    panal_adulto: bool | None = None
    babero: bool | None = None
    otros: bool | None = None
    receta: str | None = None

    class Config:
        from_attributes = True

# Dependencia para obtener sesión de base de datos
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# Obtener todas las consultas
@router.get("/uisau/", tags=["UISAU"])
def obtener_consultas(db: SQLAlchemySession = Depends(get_db)):
    try:
        result = db.query(uisauModel).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    
    
@router.get("/infos/", tags=["UISAU"])
def buscar_id(consulta: int, db: SQLAlchemySession = Depends(get_db)):
    try:
        result = db.query(uisauModel).filter(uisauModel.id_consulta == consulta).all()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}
    finally:
        print(f"consulta_id: {consulta} datetime:{now} CONSULTADO")

# Buscar consulta por ID
@router.get("/registro/", tags=["UISAU"])
def buscar_por_id(id: int, db: SQLAlchemySession = Depends(get_db)):
    try:
        result = db.query(uisauModel).filter(uisauModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}

# Buscar consultas por fecha y servicio
@router.get("/resumen_uisau/", tags=["UISAU"])
def reporte_fecha(fecha: str, servicio: int, db: SQLAlchemySession = Depends(get_db)):
    try:
        result = db.query(uisauModel).filter(
            or_(uisauModel.fecha == fecha, uisauModel.fecha_contacto == fecha),
            uisauModel.servicio == servicio
        ).all()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as error:
        return {"message": f"Error al consultar: {error}"}

# Guardar nueva consulta
@router.post("/uisausave/", tags=["UISAU"])
def crear_consulta(data: UisauSchema, db: SQLAlchemySession = Depends(get_db)):
    try:
        registro = uisauModel(**data.dict())
        db.add(registro)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Se ha registrado la consulta"})
    except SQLAlchemyError as error:
        return {"message": f"Error al crear consulta: {error}"}

# Editar consulta existente
@router.put("/uisauedit/{id}", tags=["UISAU"])
def editar_consulta(id: int, edit: UisauSchema, db: SQLAlchemySession = Depends(get_db)):
    try:
        result = db.query(uisauModel).filter(uisauModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        for key, value in edit.dict(exclude_unset=True).items():
            setattr(result, key, value)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Actualización realizada"})
    except SQLAlchemyError as error:
        return {"message": f"Error al actualizar la consulta: {error}"}

# Eliminar consulta
# Eliminar consulta
@router.delete("/uisaudelet/{id}", tags=["UISAU"])
def eliminar_consulta(id: int, db: SQLAlchemySession = Depends(get_db)):
    try:
        result = db.query(uisauModel).filter(uisauModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Eliminado con éxito"})
    
    except SQLAlchemyError as error:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": f"Error al eliminar: {error}"})

bModel = uisauModel
@router.get("/filter/", tags=["UISAU"])
async def filtro(
    id: int = Query(None, description="Id"),
    id_consulta: int = Query(None, description="Número de id de consulta"),
    expediente: int = Query(None, description="Número de Expediente"),
    estado: int = Query(None, description="Estado del Paciente"),
    fecha: str = Query(None, description="Fecha de Consulta"),
    fecha_contacto: str = Query(None, description="Fecha de Contacto"),
    fecha_referencia: str = Query(None, description="Fecha de Referencia"),
    lugar_referencia: int = Query(None, description="Lugar de referencia"),
    nombres: str = Query(None, description="Nombres"),
    apellidos: str = Query(None, description="Apellidos"),
    usuario: int = Query(None, description="Usuario de UISAU"),
    estadia: int = Query(None, description="Estadia de paciente"),
    servicio: int = Query(None, description="Servicio de paciente"),
    db: SQLAlchemySession = Depends(get_db)
):
    try:
        query = db.query(uisauModel)

        if id is not None:
            query = query.filter(uisauModel.id == id)
        if id_consulta is not None:
            query = query.filter(uisauModel.id_consulta == id_consulta)
        if estado is not None:
            query = query.filter(uisauModel.estado == estado)
        if expediente is not None:
            query = query.filter(uisauModel.expediente == expediente)
        if fecha:
            query = query.filter(uisauModel.fecha == fecha)
        if fecha_contacto:
            query = query.filter(uisauModel.fecha_contacto == fecha_contacto)
        if nombres:
            query = query.filter(uisauModel.nombres.ilike(f"%{nombres}%"))
        if apellidos:
            query = query.filter(uisauModel.apellidos.ilike(f"%{apellidos}%"))
        if fecha_referencia:
            query = query.filter(uisauModel.fecha_referencia == fecha_referencia)
        if lugar_referencia is not None:
            query = query.filter(uisauModel.lugar_referencia == lugar_referencia)
        if usuario is not None:
            query = query.filter(uisauModel.usuario == usuario)
        if estadia is not None:
            query = query.filter(uisauModel.estadia == estadia)
        if servicio is not None:
            query = query.filter(uisauModel.servicio == servicio)

        result = query.order_by(desc(uisauModel.id)).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    
    except SQLAlchemyError as error:
        return JSONResponse(status_code=500, content={"error": str(error)})