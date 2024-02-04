from database import database
import mysql.connector
from datetime import datetime
from database.database import Base
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship

db = database.get_database_connection()
now = datetime.now()

Tconsultas = ('''
  CREATE TABLE `consultas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `hoja_emergencia` varchar(15) DEFAULT NULL,
  `expediente` int DEFAULT NULL,
  `fecha_consulta` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `nombres` varchar(50) DEFAULT NULL,
  `apellidos` varchar(50) DEFAULT NULL,
  `nacimiento` date DEFAULT NULL,
  `edad` varchar(25) DEFAULT NULL,
  `sexo` varchar(1) DEFAULT NULL,
  `dpi` varchar(20) DEFAULT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `acompa` varchar(50) DEFAULT NULL,
  `parente` int DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `nota` varchar(200) DEFAULT NULL,
  `especialidad` int DEFAULT NULL,
  `servicio` int DEFAULT NULL,
  `status` int DEFAULT NULL,
  `fecha_egreso` date DEFAULT NULL,
  `fecha_recepcion` datetime DEFAULT NULL,
  `tipo_consulta` int DEFAULT NULL,
  `prenatal` int DEFAULT NULL,
  `lactancia` int DEFAULT NULL,
  `dx` varchar(100) DEFAULT NULL,
  `folios` int DEFAULT NULL,
  `medico` varchar(25) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `archived_by` varchar(8) DEFAULT NULL,
  `created_by` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hoja_emergencia` (`hoja_emergencia`),
  KEY `expediente` (`expediente`),
  CONSTRAINT `consultas_ibfk_1` FOREIGN KEY (`expediente`) REFERENCES `pacientes` (`expediente`)
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
        # command_vistaEmergencia =('''CREATE VIEW vista_emergencia AS SELECT id, tipo_consulta, hoja_emergencia, expediente, nombres, apellidos, fecha_consulta, nacimiento, status, fecha_recepcion  FROM consultas''')
        # command_vistaCoex =('''CREATE VIEW vista_coex AS SELECT id, tipo_consulta, expediente, nombres, apellidos, fecha_consulta, nacimiento, especialidad, status, fecha_recepcion  FROM consultas''')
        # command_vistaIngreso =('''CREATE VIEW vista_ingreso AS SELECT id, tipo_consulta, expediente, nombres, apellidos, fecha_consulta, nacimiento, especialidad, fecha_egreso, status, fecha_recepcion  FROM consultas''')
        command_vistaConsulta =(''' CREATE VIEW vista_consultas AS SELECT hoja_emergencia,expediente,fecha_consulta,nombres,apellidos,dpi,id,hora,fecha_egreso,especialidad,servicio,tipo_consulta, status FROM consultas''')
        cursor = db.cursor()
        cursor.execute(command_vistaConsulta)
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
    parente = Column(Integer)
    telefono = Column(String)
    nota = Column(String(200))
    especialidad = Column(Integer)
    servicio = Column(Integer)
    status = Column(Integer)
    fecha_egreso = Column(Date)
    fecha_recepcion = Column(DateTime)
    tipo_consulta = Column(Integer)
    prenatal = Column(Integer)
    lactancia = Column(Integer)
    dx = Column(String(100))
    folios = Column(Integer)
    medico = Column(String(25))
    archived_by = Column(String(8))
    created_by = Column(String(8))
    created_at = Column(String(25))
    updated_at = Column(String(25))
    
   
    
    
    # Establece la relación con la tabla de pacientes
    pacientes = relationship("PacienteModel", back_populates="consultas")
    
    
    
class VistaConsultas(Base):
    __tablename__ = "vista_consultas"

    id = Column(Integer, primary_key=True)
    hoja_emergencia = Column(String)
    expediente = Column(Integer)
    fecha_consulta = Column(Date)
    nombres = Column(String)
    apellidos = Column(String)
    dpi = Column(String)
    hora = Column(Time)
    fecha_egreso = Column(Date)
    especialidad = Column(String)
    servicio = Column(String)
    tipo_consulta = Column(String)
    status = Column(Integer)
    
    
     