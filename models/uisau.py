from database import database
import mysql.connector
from datetime import datetime
from database.database import Base
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship


db = database.get_database_connection()
now = datetime.now()

Tuisau = ('''
            CREATE TABLE uisau (
    id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `expediente` INT DEFAULT NULL,
    `nombres`VARCHAR(100) DEFAULT NULL,
    `apellidos` VARCHAR(100) DEFAULT NULL,
    `estado` INT DEFAULT NULL,
    `situacion` INT DEFAULT NULL,
    `lugar_referencia` INT DEFAULT NULL,
    `fecha_referencia` DATETIME DEFAULT NULL,
    `estadia` INT DEFAULT NULL,
    `cama` INT DEFAULT NULL,
    `especialidad` INT DEFAULT NULL,
    `servicio` INT DEFAULT NULL,
    `informacion` BOOLEAN DEFAULT NULL,
    `contacto` VARCHAR(255) DEFAULT NULL,
    `parentesco` INT DEFAULT NULL,
    `telefono` INT DEFAULT NULL,
    `fecha` DATE DEFAULT NULL,
    `nota` TEXT DEFAULT NULL,
    `estudios` VARCHAR(255) DEFAULT NULL,
    `evolucion` TEXT DEFAULT NULL,
    `id_consulta` INT DEFAULT NULL,
    `Usuario` INT DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4

          ''')

tabla_sql = Tuisau

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
            print(f"Tabla {tabla_sql} datetime:{now} CREADA")
            
    
#Definición del modelo de datos            
class uisauModel(Base):
    __tablename__ = "uisau"
    id = Column(Integer, primary_key=True)
    expediente = Column(Integer)
    nombres = Column(String(100))
    apellidos = Column(String(100))
    estado = Column(Integer)
    situacion = Column(Integer)
    lugar_referencia = Column(Integer)
    fecha_referencia = Column(DateTime)
    estadia = Column(Integer)
    cama = Column(Integer)
    especialidad = Column(Integer)
    servicio = Column(Integer)
    informacion = Column(Boolean)
    contacto = Column(String(100))
    parentesco = Column(Integer)
    telefono = Column(Integer)
    fecha = Column(DateTime)
    nota = Column(Text)
    estudios = Column(Text)
    evolucion = Column(Text)
    id_consulta = Column(Integer)
    Usuario = Column(Integer)
   
 # Establece la relación con la tabla de pacientes
  #  pacientes = relationship("PacienteModel", back_populates="uisau")