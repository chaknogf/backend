from database import database
import mysql.connector
from datetime import datetime
from database.database import Base
from sqlalchemy import Column, Integer, String,BigInteger, Date, Time
from sqlalchemy.orm import relationship


db = database.get_database_connection()

Tcons_nac = ('''
             CREATE TABLE cons_nac (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `fecha` DATE DEFAULT NULL,
    `cor` INT DEFAULT NULL,
    `ao` INT DEFAULT NULL,
    `doc` VARCHAR(9) DEFAULT NULL UNIQUE,
    `fecha_parto` DATE DEFAULT NULL,  
    `madre` VARCHAR(100) DEFAULT NULL,
    `dpi` BIGINT DEFAULT NULL,
    `passport` VARCHAR(30) DEFAULT NULL,
    `libro` INT DEFAULT NULL,
    `folio` INT DEFAULT NULL,
    `partida` INT DEFAULT NULL,
    `muni` INT DEFAULT NULL,
    `edad` INT DEFAULT NULL,
    `vecindad` INT DEFAULT NULL,
    `sexo_rn` VARCHAR(1) DEFAULT NULL,
    `lb` INT DEFAULT NULL,
    `onz` INT DEFAULT NULL,
    `hora` TIME DEFAULT NULL,
    `medico` INT DEFAULT NULL, 
    `colegiado` INT DEFAULT NULL,
    `dpi_medico` BIGINT DEFAULT NULL,
    `hijos` INT DEFAULT NULL,
    `vivos` INT DEFAULT NULL,
    `muertos` INT DEFAULT NULL,
    `tipo_parto` INT DEFAULT NULL,
    `clase_parto` INT DEFAULT NULL,
    `certifica` INT DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARSET=utf8mb4
             ''')

tabla_sql = Tcons_nac

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
class Cons_NacModel(Base):
    __tablename__ = "cons_nac"
    id = Column(Integer, primary_key=True)
    fecha = Column(Date)
    cor = Column(Integer)
    ao = Column(Integer)
    doc = Column(String(9))
    fecha_parto = Column(Date)
    madre = Column(String(100))
    dpi = Column(BigInteger)
    passport = Column(String(30))
    libro = Column(Integer)
    folio = Column(Integer)
    partida = Column(Integer)
    muni = Column(Integer)
    edad = Column(Integer)
    vecindad = Column(Integer)
    sexo_rn = Column(String(1))
    lb = Column(Integer)
    onz = Column(Integer)
    hora = Column(Time)
    medico = Column(Integer)
    colegiado = Column(Integer)
    dpi_medico = Column(BigInteger)
    hijos = Column(Integer)
    vivos = Column(Integer)
    muertos = Column(Integer)
    tipo_parto = Column(Integer)
    clase_parto = Column(Integer)
    certifica = Column(Integer)
    created_at = Column(String(25))
    updated_at = Column(String(25))
    
    
   