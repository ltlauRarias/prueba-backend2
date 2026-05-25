# Prueba Tecnica - Laura Reyes Arias


# Endpoints para crear, ver, editar y eliminar vehiculos
from fastapi import APIRouter, Depends, HTTPException, status # Organiza endpoints (url), errores 404, lista de codigos http
from sqlalchemy.orm import Session # Representa la conexion activa con la base de datos (Es pera hacer consultas)
from app.database import get_db # Abre y cierra la conexion con la base de datos con cada peticion
from app import models, schemas # Tablas de la base de datos / Estructura
from app.auth import get_current_user, require_admin # Revisa Token / Revisa si es admin
from typing import List


# Crea el router (Agrupa todos los endpoints de los vehiculos)
router = APIRouter(prefix="/api/vehicles", tags=["Vehículos"])

#Peticion GET
@router.get("/", response_model=List[schemas.VehicleResponse])
def get_vehicles(
    db: Session = Depends(get_db), # Abre la conexion a la base de datos
    current_user = Depends(get_current_user)  # Cualquier usuario autenticado puede ver (Verifica token)
):
    """
    Devuelve la lista completa de vehículos.
    Acceso: Admin y Viewer
    """
    vehicles = db.query(models.Vehicle).all()
    return vehicles

@router.get("/{vehicle_id}", response_model=schemas.VehicleResponse)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # Cualquier usuario autenticado puede ver
):
    """
    Devuelve un vehículo por su ID.
    Acceso: Admin y Viewer
    """
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first() # Busca en la tabla el id que sea igual que el de la URL
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, # Si no encuentra lanza error 
            detail="Vehículo no encontrado"
        )
    return vehicle

# POST es para crear vehiculo
@router.post("/", response_model=schemas.VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    vehicle_data: schemas.VehicleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)  # Solo admin puede crear
):
    """
    Crea un vehículo nuevo.
    Acceso: Solo Admin
    """

    # Crea un objeto vehiculo con los datos recibidos
    new_vehicle = models.Vehicle(
        marca=vehicle_data.marca,
        localidad=vehicle_data.localidad,
        aspirante=vehicle_data.aspirante
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

# PUT actualiza registro existente
@router.put("/{vehicle_id}", response_model=schemas.VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    vehicle_data: schemas.VehicleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)  # Solo admin puede editar
):
    """
    Actualiza un vehículo existente por su ID.
    Acceso: Solo Admin
    """
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado"
        )
    # Actualiza cada campo
    vehicle.marca = vehicle_data.marca
    vehicle.localidad = vehicle_data.localidad
    vehicle.aspirante = vehicle_data.aspirante

    db.commit()
    db.refresh(vehicle)
    return vehicle

# DELETE es para eliminar un vehiculo
@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)  # Solo admin puede eliminar
):
    """
    Elimina un vehículo por su ID.
    Acceso: Solo Admin
    """
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado"
        )
    db.delete(vehicle)
    db.commit()
    return None