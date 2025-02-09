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
    `fecha_referencia` DATE DEFAULT NULL,
    `fecha_contacto` DATE DEFAULT NULL,
    `hora_contacto` TIME DEFAULT NULL,
    `estadia` INT DEFAULT NULL,
    `cama` INT DEFAULT NULL,
    `especialidad` INT DEFAULT NULL,
    `servicio` INT DEFAULT NULL,
    `informacion` VARCHAR(2) DEFAULT NULL,
    `contacto` VARCHAR(255) DEFAULT NULL,
    `parentesco` INT DEFAULT NULL,
    `telefono` INT DEFAULT NULL,
    `fecha` DATE DEFAULT NULL,
    `hora` TIME DEFAULT NULL,
    `nota` TEXT DEFAULT NULL,
    `estudios` VARCHAR(255) DEFAULT NULL,
    `evolucion` TEXT DEFAULT NULL,
    `recetado_por` VARCHAR(2),
    `shampoo` TINYINT(1) DEFAULT 0,
    `toalla` TINYINT(1) DEFAULT 0,
    `peine` TINYINT(1) DEFAULT 0,
    `jabon` TINYINT(1) DEFAULT 0,
    `cepillo_dientes` TINYINT(1) DEFAULT 0,
    `pasta_dental` TINYINT(1) DEFAULT 0,
    `sandalias` TINYINT(1) DEFAULT 0,
    `agua` TINYINT(1) DEFAULT 0,
    `papel` TINYINT(1) DEFAULT 0,
    `panales` TINYINT(1) DEFAULT 0
    `id_consulta` INT DEFAULT NULL,
    `dxA` VARCHAR(20) DEFAULT NULL,
    `dxB` VARCHAR(20) DEFAULT NULL,
    `dxC` VARCHAR(20) DEFAULT NULL,
    `dxD` VARCHAR(20) DEFAULT NULL,
    `dxE` VARCHAR(20) DEFAULT NULL,
    `created_by` VARCHAR(8) DEFAULT NULL,
    `update_by` VARCHAR(8) DEFAULT NULL,
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
    consulta_id = Column(Integer)
    expediente = Column(Integer)
    nombres = Column(String(100))
    apellidos = Column(String(100))
    estado = Column(Integer)
    situacion = Column(Integer)
    lugar_referencia = Column(Integer)
    fecha_referencia = Column(Date)
    estadia = Column(Integer)   
    cama = Column(Integer)
    especialidad = Column(Integer)
    servicio = Column(Integer)
    informacion = Column(String(2))
    contacto = Column(String(100))
    parentesco = Column(Integer)
    telefono = Column(Integer)
    fecha = Column(Date)
    hora = Column(Time)
    fecha_contacto = Column(Date)
    hora_contacto = Column(Time)
    nota = Column(Text)
    estudios = Column(Text)
    evolucion = Column(Text)
    receta_por = Column(String(2))
    shampoo = Column(Boolean)
    toalla = Column(Boolean)
    peine = Column(Boolean)
    jabon = Column(Boolean)
    cepillo_dientes = Column(Boolean)
    pasta_dental = Column(Boolean)
    sandalias = Column(Boolean)
    agua = Column(Boolean)
    papel = Column(Boolean)
    panales = Column(Boolean)
    dxA = Column(String(20))
    dxB = Column(String(20))
    dxC = Column(String(20))
    dxD = Column(String(20))
    dxE = Column(String(20))
    id_consulta = Column(Integer)
    created_by = Column(String(8))
    update_by = Column(String(8))
    # created_at = Column(String(25))
    # updated_at = Column(String(25))
   
 # Establece la relación con la tabla de pacientes
  #  pacientes = relationship("PacienteModel", back_populates="uisau")