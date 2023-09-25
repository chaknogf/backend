from database import database
import mysql.connector
from datetime import datetime
from database.database import Base
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

db = database.get_database_connection()
now = datetime.now()

Tconsultas = ('''
               CREATE TABLE `consultas`(
              `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              `hoja_emergencia` VARCHAR(15) UNIQUE,
              `expediente` INT DEFAULT NULL,
              `fecha_consulta` DATE DEFAULT NULL,
              `hora` TIME DEFAULT NULL,
              `nombres` VARCHAR(50) DEFAULT NULL,
              `apellidos` VARCHAR(50) DEFAULT NULL,
              `nacimiento` DATE DEFAULT NULL,
              `edad` VARCHAR(25) DEFAULT NULL,
              `sexo` VARCHAR(1) DEFAULT NULL,
              `dpi` VARCHAR(20) DEFAULT NULL,
              `direccion` VARCHAR(100) DEFAULT NULL,
              `acompa` VARCHAR(50) DEFAULT NULL,
              `telefono` INT DEFAULT NULL,
              `nota` VARCHAR(200) DEFAULT NULL,
              `especialidad` INT DEFAULT NULL,
              `recepcion` BOOLEAN DEFAULT FALSE,
              `fecha_egreso` DATE DEFAULT NULL,
              `fecha_recepcion`DATE DEFAULT NULL,
              `tipo_consulta` INT DEFAULT NULL,
              `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
              FOREIGN KEY (expediente) REFERENCES pacientes (expediente)
             )   ENGINE=InnoDB CHARSET=utf8mb4
               ''')

tabla_sql = Tconsultas

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
            
def vista():
    try:
        command_vistaEmergencia =('''CREATE VIEW vista_emergencia AS SELECT id, tipo_consulta, hoja_emergencia, expediente, nombres, apellidos, fecha_consulta, nacimiento, recepcion  FROM consultas''')
        command_vistaCoex =('''CREATE VIEW vista_coex AS SELECT id, tipo_consulta, expediente, nombres, apellidos, fecha_consulta, nacimiento, especialidad, recepcion  FROM consultas''')
        command_vistaIngreso =('''CREATE VIEW vista_ingreso AS SELECT id, tipo_consulta, expediente, nombres, apellidos, fecha_consulta, nacimiento, especialidad, fecha_egreso, recepcion  FROM consultas''')
        cursor = db.cursor()
        cursor.execute(command_vistaEmergencia, command_vistaCoex, command_vistaIngreso)
        db.commit()
        return {"message": "Vistas creadas correctamente."}
    except Exception as error:
        if "Table 'vista_emergencia' already exists" in str(error):
            return {"message": "La vistas ya existe."}
        else:
            return {"error": f"Error al crear las vistas: {error}"}
    finally:
        if db.is_connected():
            cursor.close
            
            
#Definición del modelo de datos
class ConsultasModel(Base):
    __tablename__ = "consultas"
    
    id = Column(Integer, primary_key=True)
    hoja_emergencia = Column(String(12))
    expediente = Column(Integer, ForeignKey('pacientes.expediente'))
    fecha_consulta = Column(Date)
    hora = Column(Time)
    nombres = Column(String(50))
    apellidos = Column(String(50))
    nacimiento = Column(Date)
    edad = Column(String(25))
    sexo = Column(String(1))
    dpi = Column(String(20))
    direccion = Column(String(100))
    acompa = Column(String(50))
    telefono = Column(Integer)
    nota = Column(String(200))
    especialidad = Column(Integer)
    recepcion = Column(Boolean)
    fecha_egreso = Column(Date)
    fecha_recepcion = Column(Date)
    tipo_consulta = Column(Integer)
    created_at = Column(DateTime)
    
    # Establece la relación con la tabla de pacientes
    pacientes = relationship("PacienteModel", back_populates="consultas")
    
    
class VistaEmergencia(Base):
    __tablename__ = "vista_emergencia"
        
    id = Column(Integer, primary_key=True)
    hoja_emergencia = Column(String(12))
    expediente = Column(Integer,ForeignKey('pacientes.expediente'))
    nombres = Column(String(50))
    apellidos = Column(String(50))
    fecha_consulta = Column(Date)
    nacimiento = Column(Date)
    tipo_consulta = Column(Integer)
    
class VistaCoex(Base):
    __tablename__ = "vista_coex"
        
    id = Column(Integer, primary_key=True)
    expediente = Column(Integer,ForeignKey('pacientes.expediente'))
    nombres = Column(String(50))
    apellidos = Column(String(50))
    fecha_consulta = Column(Date)
    nacimiento = Column(Date)
    especialidad = Column(Integer)
    tipo_consulta = Column(Integer)
    
class VistaIngreso(Base):
    __tablename__ = "vista_ingreso"
        
    id = Column(Integer, primary_key=True)
    expediente = Column(Integer,ForeignKey('pacientes.expediente'))
    nombres = Column(String(50))
    apellidos = Column(String(50))
    fecha_consulta = Column(Date)
    nacimiento = Column(Date)
    especialidad = Column(Integer)
    fecha_egreso = Column(Date)
    tipo_consulta = Column(Integer)
    
     