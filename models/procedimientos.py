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
    `procedimiento` VARCHAR(200) DEFAULT NULL,
    `especialidad` INT DEFAULT NULL,
    `cantidad` INT DEFAULT NULL,
    `medico` INT DEFAULT NULL,
    `created_by` VARCHAR(10) DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4
             ''')

Tcodigo_Proce = ('''
    CREATE TABLE codigo_Proce (
    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `abreviatura` VARCHAR(10) DEFAULT NULL,
    `procedimiento` VARCHAR(200) DEFAULT NULL
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4
                           ''')


tabla_sql_a = Tproce_medicos
tabla_sql_b = Tcodigo_Proce

def crear_tabla():
    try:
        cursor = db.cursor()
        cursor.execute(tabla_sql_a, tabla_sql_b)
        db.commit()
        return {"message": f"Tabla {tabla_sql_a, tabla_sql_b} creada"}
    except mysql.connector.Error as error:
        return {"message": f"Error al creaer Tabla: {error}"}
    finally:
        if db.is_connected():
            cursor.close()
            
            
#Definición del modelo de datos            
class ProceMedicosModel(Base):
    __tablename__ = "proce_medicos"
    id = Column(Integer, primary_key=True)
    fecha = Column(String)
    servicio = Column(Integer)
    sexo = Column(String)
    abreviatura = Column(String)
    procedimiento = Column(String)
    especialidad = Column(Integer)
    cantidad = Column(Integer)
    medico = Column(Integer)
    created_by = Column(String)
    
    
#Definición del modelo de datos            
class CodigosProceModel(Base):
    __tablename__ = "codigo_Proce"
    id = Column(Integer, primary_key=True)
    abreviatura = Column(String)
    procedimiento = Column(String)
    