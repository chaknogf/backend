from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import subprocess
from database import database
import getpass






# ... Configuración de la base de datos ...
db = database.get_database_connection()
DB_PROJECT = "test_api"


# Función para ejecutar el comando mysqldump
def run_mysqldump(table_name: str):
    
    password = getpass.getpass("Prometeus.0")
    command_mk = "mkdir -p ~/Desktop/BACKUP_SQL/"
    command_mk = "mkdir -p ~/Desktop/BACKUP_SQL/"
    command =  f"mysqldump -u root -p{password} --complete-insert {DB_PROJECT} {table_name} > ~/Desktop/BACKUP_SQL/{table_name}.sql"
    
    try:
        subprocess.run(command_mk, shell=True, check=True)
        subprocess.run(command, shell=True, check=True)
        return "Exportación exitosa"
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Error en la exportación")

async def import_db(file: UploadFile = File(...)):
    path_sql = file.file.name
    command_import = "source {path_sql}"
    try:
        cursor = db.cursor()
        cursor.execute(command_import)
        db.commit()
        
        return {"message": "tabla importada."}
    except Exception as error:
        return {"error": f"Error al importar: {error}"}
    finally:
        if db.is_connected():
            cursor.close
    
    
            

