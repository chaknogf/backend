from database import database
import mysql.connector
from datetime import datetime
from database.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


db = database.get_database_connection()

Tcie10 = ('''
             CREATE TABLE cie10 (
    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `cod` VARCHAR(7) DEFAULT NULL,
    `grupo`VARCHAR(1) DEFAULT NULL,
    `dx` VARCHAR(250) DEFAULT NULL,
    `abreviatura` VARCHAR(10) DEFAULT NULL,
    `especialidad` INT DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4
             ''')

tabla_sql = Tcie10



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
class Cie10Model(Base):
    __tablename__ = "medicos"
    id = Column(Integer, primary_key=True)
    cod = Column(String(7))
    grupo = Column(String(1))
    dx = Column(String(250))
    abreviatura = Column(String(10))
    especialidad = Column(Integer)
   