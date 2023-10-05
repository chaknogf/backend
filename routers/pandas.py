import io
from fastapi import APIRouter, File, UploadFile
import pandas as pd  # Importa Pandas
from database.database import Session
from database import database
from models.consulta import ConsultasModel

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