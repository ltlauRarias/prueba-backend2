from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carga las variables del archivo .env
load_dotenv()

# Lee la URL de la base de datos desde .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Crea la conexion a la base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crea una fabrica de sesiones para hablar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de la que heredan todos los modelos
Base = declarative_base()

# Funcion que abre y cierra la sesion automaticamente en cada peticion
def get_db():
    db = SessionLocal()
    try:
        yield db  # Le pasa la sesion al endpoint que la necesite
    finally:
        db.close()  # Siempre cierra la sesion al terminar
    