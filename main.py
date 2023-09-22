from fastapi import FastAPI, File, UploadFile, WebSocket
from routers import citas_router, consultas_router, municipio, paciente_router, enums
from models import citas, consulta, paciente
from database import xDB
from fastapi.staticfiles import StaticFiles
import getpass
from fastapi.middleware.cors import CORSMiddleware
from middlewares.error_hendler import ErrorHandler
import websockets
#from middlewares.jwt_bearer import JWTBearer



app = FastAPI()
app.add_middleware(ErrorHandler)


allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/mkVp', tags=["SQL"])
def mkbd():
   # cts = citas.crear_tabla()
    #patien = paciente.crear_tabla()
    v_paciente = paciente.vista()
    v_consulta = consulta.vista()
    v_citas = citas.vistaC()
    return  v_paciente, v_citas, v_consulta

@app.get('/importdb', tags=["SQL"])
def import_data(file: UploadFile = File(...)):
    data = xDB.import_db(file)
    return {"filename": file.filename}

@app.get('/xportDB', tags=["SQL"])
def export_data(table_name: str):
    
    result = xDB.run_mysqldump(table_name)
    return {"message": result}


#importacion de routers
app.include_router(citas_router.router)
app.include_router(paciente_router.router)
app.include_router(municipio.router)
app.include_router(consultas_router.router)

 