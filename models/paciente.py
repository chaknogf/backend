from database import database
import mysql.connector
from datetime import datetime
from database.database import Base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

db = database.get_database_connection()
 
now = datetime.now()

Tpacientes = ('''
    CREATE TABLE `pacientes` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `expediente` int UNIQUE DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `dpi` bigint DEFAULT NULL,
  `pasaporte` varchar(50) DEFAULT NULL,
  `sexo` varchar(2) DEFAULT NULL,
  `nacimiento` date DEFAULT NULL,
  `nacionalidad` int DEFAULT NULL,
  `lugar_nacimiento` int DEFAULT NULL,
  `estado_civil` int DEFAULT NULL,
  `educacion` int DEFAULT NULL,
  `pueblo` int DEFAULT NULL,
  `idioma` int DEFAULT NULL,
  `ocupacion` varchar(50) DEFAULT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `telefono` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `padre` varchar(50) DEFAULT NULL,
  `madre` varchar(50) DEFAULT NULL,
  `responsable` varchar(50) DEFAULT NULL,
  `parentesco` int DEFAULT NULL,
  `dpi_responsable` bigint DEFAULT NULL,
  `telefono_responsable` int DEFAULT NULL,
  `estado` varchar(2) DEFAULT NULL,
  `exp_madre` int DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `fechaDefuncion` varchar(10) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `expediente_unico` (`expediente`)
) ENGINE=InnoDB AUTO_INCREMENT=72879 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
''')



def vista():
    try:
        command_vista =('''CREATE VIEW vista_paciente AS SELECT id, nombre, apellido, expediente, nacimiento, dpi, sexo, estado  FROM pacientes''')
        cursor = db.cursor()
        cursor.execute(command_vista)
        db.commit()
        return {"message": "Vista 'vista_paciente' creada correctamente."}
    except Exception as error:
        if "Table 'vista_paciente' already exists" in str(error):
            return {"message": "La vista 'vista_paciente' ya existe."}
        else:
            return {"error": f"Error al crear la vista: {error}"}
    finally:
        if db.is_connected():
            cursor.close
        

def crear_tabla():
    try:
        cursor = db.cursor()
        cursor.execute(Tpacientes)
        db.commit()
        return {"message": "Tabla pacientes creada"}
    except mysql.connector.Error as error:
        return {"message": f"Erro al crear Tabla: {error}"}
    finally:
        if db.is_connected():
            cursor.close
            print(f"Tabla pacientes datetime:{now} CREADA")
    

# Definición del modelo de datos
class PacienteModel(Base):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True) 
    expediente = Column(Integer)
    nombre = Column(String(50), index=True)
    apellido = Column(String(50), index=True)
    dpi = Column(Integer)
    pasaporte = Column(String(50))
    sexo = Column(String(2))
    nacimiento = Column(Date)
    nacionalidad = Column(Integer)
    lugar_nacimiento = Column(Integer)
    estado_civil = Column(Integer)
    educacion = Column(Integer)
    pueblo= Column(Integer)
    idioma = Column(Integer)
    ocupacion = Column(String(50))
    direccion = Column(String(100))
    telefono = Column(String(50))
    email = Column(String(100))
    padre = Column(String(50))
    madre = Column(String(50))
    responsable = Column(String(50))
    parentesco = Column(Integer)
    dpi_responsable = Column(Integer)
    telefono_responsable = Column(Integer)
    estado = Column(String(2))
    exp_madre = Column(Integer)
    user = Column(String(50))
    fechaDefuncion = Column(String(10))
   
# Configura la relación con la tabla de citas
    citas = relationship("CitasModel", back_populates="pacientes")
    consultas= relationship("ConsultasModel", back_populates="pacientes")

class VistaPaciente(Base):
    __tablename__ = "vista_paciente"
    
    id = Column(Integer,primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    expediente = Column(Integer)
    nacimiento = Column(String)
    dpi = Column(Integer)
    sexo = Column(String)
    estado = Column(String)
    
#CREATE VIEW vista_paciente AS SELECT id, nombre, apellido, expediente, nacimiento  FROM pacientes;    
#SELECT table_name FROM information_schema.views WHERE table_schema = 'test_api';

