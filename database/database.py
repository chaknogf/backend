import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "Prometeus.0"
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
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Prometeus.0@localhost/test_api"
engine = create_engine(SQLALCHEMY_DATABASE_URL,echo=False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#Declaración de la base de datos
Base = declarative_base()



def get_database_session() -> Session:
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Session()
    return db



#Base.metada.create_all(bind=engine)