import io
from fastapi import APIRouter, File, HTTPException, UploadFile, Query
from fastapi.responses import StreamingResponse
from io import BytesIO
import pandas as pd  # Importa Pandas
from database.database import Session
from database import database
from models.consulta import ConsultasModel
from models.uisau import uisauModel
from models.paciente import PacienteModel
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter()
db = database.get_database_connection()
cursor = db.cursor()

# ... (Otras configuraciones de CORS, middlewares, etc.)

# Ruta para cargar un archivo CSV con datos
@router.post('/upload-csv/', tags=["Data Analysis"])
async def upload_csv(file: UploadFile = File(...)):
    # Asegúrate de que el archivo es un archivo CSV
    if file.filename.endswith('.csv'):
        data = await file.read()  # Lee el contenido del archivo
        df = pd.read_csv(io.BytesIO(data))  # Carga los datos en un DataFrame de Pandas
        return {"message": "Archivo CSV cargado exitosamente", "dataframe": df.to_dict()}  # Puedes devolver los datos como un diccionario si lo deseas
    else:
        return {"error": "El archivo debe ser un archivo CSV"}

# Ruta para realizar operaciones de análisis de datos
@router.post('/analyze-data/', tags=["Data Analysis"])
async def analyze_data(data: dict):  # Recibe los datos como un diccionario
    # Convierte el diccionario en un DataFrame de Pandas (si es necesario)
    df = pd.DataFrame(data)
    
    # Realiza operaciones de análisis de datos aquí utilizando Pandas
    # Por ejemplo, puedes calcular estadísticas descriptivas, filtrar datos, realizar agregaciones, etc.
    
    # Devuelve los resultados del análisis
    results = {}  # Agrega los resultados de tus análisis aquí
    return {"message": "Operaciones de análisis de datos completadas", "results": results}

# ... (Otras rutas y configuraciones)

@router.get('/analyze-data/', tags=["Data Analysis"])
async def analyze_data():
    db =  Session()  # Crea una instancia de la sesión de SQLAlchemy
    
    # Consulta la base de datos utilizando SQLAlchemy
    results = db.query(ConsultasModel).all()  # Por ejemplo, consulta todos los registros de la tabla MyDataModel
    
    # Realiza operaciones de análisis de datos en results (por ejemplo, conviértelos en un DataFrame de Pandas)
    
    db.close()  # Cierra la sesión de SQLAlchemy
    
    return {"message": "Operaciones de análisis de datos completadas", "results": results}



@router.get("/estadisticas/", tags=["Estadísticas"])
async def obtener_estadisticas(
    fecha_inicio: str = Query(None, title="Fecha inicial"),
    fecha_final: str = Query(None, title="Fecha final"),
):
    try:
        db = Session()
        
        query = db.query(
            ConsultasModel.especialidad,
            ConsultasModel.tipo_consulta,
            ConsultasModel.fecha_consulta,
            ConsultasModel.fecha_egreso
        )

        if fecha_inicio and fecha_final:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d")
            query = query.filter(ConsultasModel.fecha_consulta.between(fecha_inicio, fecha_final))
        elif fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            query = query.filter(ConsultasModel.fecha_consulta >= fecha_inicio)
        elif fecha_final:
            fecha_final = datetime.strptime(fecha_final, "%Y-%m-%d")
            query = query.filter(ConsultasModel.fecha_consulta <= fecha_final)

        resultados = query.all()
        
        # Crear un DataFrame de Pandas con los resultados
        df = pd.DataFrame(resultados, columns=["especialidad", "tipo_consulta", "fecha_consulta", "fecha_egreso"])

        # Filtrar los datos según el tipo de consulta
        ingresos = df[df["tipo_consulta"] == 2]
        consultas = df[df["tipo_consulta"] == 1]

        # Realizar cálculos de suma o conteo
        total_ingresos = len(ingresos)
        total_consultas = len(consultas)
        total_egresos = len(df.dropna(subset=["fecha_egreso"]))
        
        # Puedes realizar más cálculos aquí según tus necesidades

        return {
            "total_ingresos": total_ingresos,
            "total_consultas": total_consultas,
            "total_egresos": total_egresos
        }
    except SQLAlchemyError as error:
        return {"error": f"Error al consultar la base de datos: {error}"}
    finally:
        db.close()


@router.get("/report_consult/", tags=["Estadísticas"])
async def excel_consultas(
    fecha_inicio: str = Query(None, title="Fecha inicial"),
    fecha_final: str = Query(None, title="Fecha final"),
):
    try:
        db = Session()

        # Obtener datos de la base de datos en el rango de fechas
        result = db.query(ConsultasModel).filter(ConsultasModel.fecha_consulta.between(fecha_inicio, fecha_final)).all()

        # Verificar si hay datos en el rango de fechas
        if not result:
            raise HTTPException(status_code=404, detail="No hay datos en el rango de fechas seleccionado")

       # Corregir datos según necesidades específicas
        for row in result:
            # Convertir el valor de la columna 'status' a un texto descriptivo
            if row.status == 1:
                row.status = "Activo"
            elif row.status == 2:
                row.status = "Archivado"
                
            # Eliminar la columna '_sa_instance_state'
            del row._sa_instance_state


        # Crear un DataFrame de Pandas con los resultados
        df = pd.DataFrame([row.__dict__ for row in result])

        # Crear un objeto BytesIO para almacenar el archivo Excel
        excel_io = BytesIO()

        # Utilizar Pandas para escribir el DataFrame en un archivo Excel en BytesIO
        df.to_excel(excel_io, index=False, engine="openpyxl")

        # Configurar la posición del puntero al principio del BytesIO
        excel_io.seek(0)

        # Configurar los encabezados de la respuesta para indicar un archivo Excel
        headers = {
            "Content-Disposition": "attachment; filename=informe.xlsx",
            "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }

        # Devolver una StreamingResponse con el archivo Excel
        return StreamingResponse(io.BytesIO(excel_io.read()), headers=headers)

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar la base de datos: {error}")
    

@router.get("/report_uisau/", tags=["Estadísticas"])
async def excel_uisau(
    fecha_inicio: str = Query(None, title="Fecha inicial"),
    fecha_final: str = Query(None, title="Fecha final"),
):
    try:
        db = Session()

        # Obtener datos de la base de datos en el rango de fechas
        result = db.query(uisauModel).filter(uisauModel.fecha.between(fecha_inicio, fecha_final)).all()

        # Verificar si hay datos en el rango de fechas
        if not result:
            raise HTTPException(status_code=404, detail="No hay datos en el rango de fechas seleccionado")

       # Corregir datos según necesidades específicas
        for row in result:
            # Convertir el valor de la columna 'status' a un texto descriptivo
            
                
            # Eliminar la columna '_sa_instance_state'
            del row._sa_instance_state


        # Crear un DataFrame de Pandas con los resultados
        df = pd.DataFrame([row.__dict__ for row in result])

        # Crear un objeto BytesIO para almacenar el archivo Excel
        excel_io = BytesIO()

        # Utilizar Pandas para escribir el DataFrame en un archivo Excel en BytesIO
        df.to_excel(excel_io, index=False, engine="openpyxl")

        # Configurar la posición del puntero al principio del BytesIO
        excel_io.seek(0)

        # Configurar los encabezados de la respuesta para indicar un archivo Excel
        headers = {
            "Content-Disposition": "attachment; filename=informe.xlsx",
            "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }

        # Devolver una StreamingResponse con el archivo Excel
        return StreamingResponse(io.BytesIO(excel_io.read()), headers=headers)

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar la base de datos: {error}")
    

@router.get("/report_paciente/", tags=["Estadísticas"])
async def excel_pacientes():
    try:
        db = Session()

        # Obtener datos de la base de datos en el rango de fechas
        result = db.query(PacienteModel).all()

        # Verificar si hay datos en el rango de fechas
        if not result:
            raise HTTPException(status_code=404, detail="No hay datos en el rango de fechas seleccionado")

       # Corregir datos según necesidades específicas
        for row in result:
            # Convertir el valor de la columna 'status' a un texto descriptivo
           
                
            # Eliminar la columna '_sa_instance_state'
            del row._sa_instance_state


        # Crear un DataFrame de Pandas con los resultados
        df = pd.DataFrame([row.__dict__ for row in result])

        # Crear un objeto BytesIO para almacenar el archivo Excel
        excel_io = BytesIO()

        # Utilizar Pandas para escribir el DataFrame en un archivo Excel en BytesIO
        df.to_excel(excel_io, index=False, engine="openpyxl")

        # Configurar la posición del puntero al principio del BytesIO
        excel_io.seek(0)

        # Configurar los encabezados de la respuesta para indicar un archivo Excel
        headers = {
            "Content-Disposition": "attachment; filename=informe.xlsx",
            "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }

        # Devolver una StreamingResponse con el archivo Excel
        return StreamingResponse(io.BytesIO(excel_io.read()), headers=headers)

    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail=f"Error al consultar la base de datos: {error}")