# Prueba Tecnica - Laura Reyes Arias

# Aqui se arranca la aplicacion, conexion de modulos, configuracion de comunicacion


from fastapi import FastAPI  # la clase principal que crea la web
from fastapi.middleware.cors import CORSMiddleware  # Para que el Front se conecte con el Back
from starlette.middleware.base import BaseHTTPMiddleware  # Crear middlewares personalizado
from app.database import engine, Base, SessionLocal
from app.routers import vehicles, auth  # Archivos con los endpoints de vehiculos y autenticacion
from app.middleware import log_requests  # Funcion que registra cada petición HTTP
from app import models  # las tablas de la base de datos para sql
from app.auth import hash_password

# Crea todas las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

def seed_database():
    """
    Función que puebla la base de datos con datos iniciales.
    Se ejecuta cada vez que el servidor arranca.
    Solo crea los datos si no existen ya.
    """
    db = SessionLocal()
    try:
        # Crea el usuario admin si no existe
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            db.add(models.User(
                username="admin",
                password=hash_password("admin123"),
                role="admin"
            ))

        # Crea el usuario viewer si no existe
        viewer = db.query(models.User).filter(models.User.username == "viewer").first()
        if not viewer:
            db.add(models.User(
                username="viewer",
                password=hash_password("viewer123"),
                role="viewer"
            ))

        # Crea vehiculos de ejemplo si la tabla esta vacia
        if db.query(models.Vehicle).count() == 0:
            vehiculos = [
                models.Vehicle(marca="Toyota", localidad="Usaquén", aspirante="Carlos Martínez"),
                models.Vehicle(marca="Mazda", localidad="Suba", aspirante="Laura Gómez"),
                models.Vehicle(marca="Renault", localidad="Kennedy", aspirante="Andrés Torres"),
                models.Vehicle(marca="Chevrolet", localidad="Bosa", aspirante="María Rodríguez"),
                models.Vehicle(marca="Kia", localidad="Chapinero", aspirante="Felipe Vargas"),
                models.Vehicle(marca="Hyundai", localidad="Fontibón", aspirante="Valentina Cruz"),
                models.Vehicle(marca="Ford", localidad="Engativá", aspirante="Santiago López"),
                models.Vehicle(marca="Volkswagen", localidad="Teusaquillo", aspirante="Daniela Herrera"),
                models.Vehicle(marca="Honda", localidad="Barrios Unidos", aspirante="Julián Moreno"),
                models.Vehicle(marca="Nissan", localidad="Rafael Uribe", aspirante="Camila Jiménez"),
                models.Vehicle(marca="BMW", localidad="Puente Aranda", aspirante="David Ospina"),
            ]
            db.add_all(vehiculos)

        db.commit()
    finally:
        db.close()

# Ejecuta al arrancar el servidor
seed_database()

# Crea la aplicación FastAPI
app = FastAPI(
    title="API Concesionario",
    description="Backend para gestión de vehículos con autenticación JWT",
    version="1.0.0"
)

# Configura CORS para permitir peticiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agrega el middleware de logging
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

# Registra los routers
app.include_router(auth.router)
app.include_router(vehicles.router)

# Endpoint de bienvenida
@app.get("/")
def root():
    return {"message": "API Concesionario funcionando correctamente"}