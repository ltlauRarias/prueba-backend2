from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user, require_admin
from typing import List

# Crea el router

router = APIRouter(prefix="/api/vehicles", tags=["Vehículos"])

@router.get("/", response_model=List[schemas.VehicleResponse])
def get_vehicles(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # Cualquier usuario autenticado puede ver
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
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado"
        )
    return vehicle

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
    new_vehicle = models.Vehicle(
        marca=vehicle_data.marca,
        localidad=vehicle_data.localidad,
        aspirante=vehicle_data.aspirante
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

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