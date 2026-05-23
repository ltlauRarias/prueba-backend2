from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.database import engine, Base
from app.routers import vehicles, auth
from app.middleware import log_requests

# Crea todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crea la aplicación FastAPI
app = FastAPI(
    title="API Concesionario",
    description="Backend para gestión de vehículos con autenticación JWT",
    version="1.0.0"
)

# Configura que el frontend pueda comunicarse con el backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  \
    allow_credentials=True,
    allow_methods=["*"],  \
    allow_headers=["*"], 
)

# Registrar cada petición
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

# Registra los routers con sus endpoints
app.include_router(auth.router)
app.include_router(vehicles.router)

# Endpoint de bienvenida
@app.get("/")
def root():
    return {"message": "API Concesionario funcionando correctamente"}