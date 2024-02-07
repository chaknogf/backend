from database import database
import mysql.connector
from datetime import datetime
from database.database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship



db = database.get_database_connection()

now = datetime.now()

Tcitas = ('''
          CREATE TABLE `citas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` date DEFAULT NULL,
  `expediente` int DEFAULT NULL,
  `especialidad` int DEFAULT NULL,
  `fecha_cita` date DEFAULT NULL,
  `nota` varchar(255) DEFAULT NULL,
  `tipo` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `expediente` (`expediente`),
  CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`expediente`) REFERENCES `pacientes` (`expediente`)
     )   ENGINE=InnoDB CHARSET=utf8mb4
          
          ''')

tabla_sql = Tcitas

def vistaC():
    try:
        command_vista =('''CREATE VIEW vista_citas AS
SELECT
    ROW_NUMBER() OVER () AS id,
    especialidad,
    DATE_FORMAT(fecha, '%Y-%m-%d') AS dia,
    COUNT(*) AS total_citas
FROM
    citas
WHERE
    tipo = false  
GROUP BY
    especialidad, dia
''')
        cursor = db.cursor()
        cursor.execute(command_vista)
        db.commit()
        return {"message": "Vista 'vista_citas' creada correctamente."}
    except Exception as error:
        if "Table 'vista_paciente' already exists" in str(error):
            return {"message": "La vista 'vista_citas' ya existe."}
        else:
            return {"error": f"Error al crear la vista: {error}"}
    finally:
        if db.is_connected():
            cursor.close

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
            

            
# Definición del modelo de datos
class CitasModel(Base):
    __tablename__ = "citas"
    
    id = Column(Integer, primary_key=True)
    fecha = Column(Date)
    expediente = Column(Integer,ForeignKey('pacientes.expediente'))
    especialidad = Column(Integer)
    fecha_cita = Column(Date)
    nota = Column(String(255)) 
    tipo = Column(Integer)
    created_by = Column(String(8))
    
 # Establece la relación con la tabla de pacientes
    pacientes = relationship("PacienteModel", back_populates="citas")
    
class VistaCitas(Base):
    __tablename__ = "vista_citas"
    
    id = Column(Integer, primary_key=True)
    especialidad = Column(Integer)
    dia = Column(String)
    total_citas = Column(Integer)
     
    
   