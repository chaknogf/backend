from database import database
import mysql.connector
from datetime import datetime
from database.database import Base
from sqlalchemy import Column, Integer, String,BigInteger
from sqlalchemy.orm import relationship


db = database.get_database_connection()

Tusuarios = ('''
             CREATE TABLE usuarios (
    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `code` INT DEFAULT NULL,
    `name`VARCHAR(200) DEFAULT NULL,
    `dpi` BIGINT DEFAULT NULL,
    `email` VARCHAR(100) DEFAULT NULL,
    `password` VARCHAR(10) DEFAULT NULL,
    `rol` INT DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4
             ''')

tabla_sql = Tusuarios

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
class UsuariosModel(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    name = Column(String(200))
    dpi = Column(BigInteger)
    email = Column(String(100))
    password = Column(String(10))
    rol = Column(Integer)
    