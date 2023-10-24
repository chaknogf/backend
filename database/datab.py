import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""  # Deja esto en blanco si no hay contraseña
MYSQL_DATABASE = "test_api"

def get_database_connection():
    db = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    return db

# Configuración de la conexión a la base de datos
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

# Declaración de la base de datos
Base = declarative_base()
