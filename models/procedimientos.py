from database import database
import mysql.connector
from datetime import datetime
from database.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


db = database.get_database_connection()

Tproce_medicos = ('''
             CREATE TABLE proce_medicos (
    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `fecha` DATE DEFAULT NULL,
    `servicio` INT DEFAULT NULL,
    `sexo` VARCHAR(1) DEFAULT NULL,
    `abreviatura` VARCHAR(10) DEFAULT NULL,
    `procedimiento` INT DEFAULT NULL,
    `especialidad` INT DEFAULT NULL,
    `cantidad` INT DEFAULT NULL,
    `medico` INT DEFAULT NULL,
    `created_by` VARCHAR(10) DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4
             ''')

tabla_sql = Tproce_medicos

def crear_tabla():
    try:
        cursor = db.cursor()
        cursor.execute(tabla_sql)
        db.commit()
        return {"message": f"Tabla {tabla_sql} creada"}
    except mysql.connector.Error as error:
        return {"message": f"Error al creaer Tabla: {error}"}
    finally:
        if db.is_connected():
            cursor.close()
            print(f"Tabla {tabla_sql} datetime: {datetime.now()} CREADA")
            
#Definición del modelo de datos            
class ProceMedicos(Base):
    __tablename__ = "proce_medicos"
    id = Column(Integer, primary_key=True)
    fecha = Column(String)
    servicio = Column(Integer)
    sexo = Column(String)
    abreviatura = Column(String)
    especialidad = Column(Integer)
    cantidad = Column(Integer)
    medico = Column(Integer)
    created_by = Column(String)