# Prueba Tecnica - Laura Reyes Arias

# Contiene Endpoints para registrarse e iniciar sesion
from fastapi import APIRouter, Depends, HTTPException, status # Organiza endpoints (url), errores 404, lista de codigos http
from fastapi.security import OAuth2PasswordRequestForm # Importa el formulario estandar de OAuth2
from sqlalchemy.orm import Session # Representa la conexion activa con la base de datos (Es pera hacer consultas)
from app.database import get_db # Abre y cierra la conexion con la base de datos con cada peticion
from app import models, schemas # Tablas de la base de datos / Estructura
from app.auth import hash_password, verify_password, create_access_token # Token y contraseñas

# Crea el router
router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/register", response_model=schemas.TokenResponse)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar un usuario nuevo.
    Recibe: username, password y role (opcional, por defecto 'viewer')
    Devuelve: token JWT para que pueda usar la app inmediatamente
    """
    # Verifica si el username ya existe en la base de datos
    existing_user = db.query(models.User).filter(
        models.User.username == user_data.username
    ).first()

    # Si ya existe...
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya existe"
        )

    # Encripta la contraseña antes de guardarla
    hashed = hash_password(user_data.password)

    # Crea el nuevo usuario en la base de datos
    new_user = models.User(
        username=user_data.username,
        password=hashed,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Genera el token JWT con el username y rol del usuario
    token = create_access_token({"sub": new_user.username, "role": new_user.role})

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": new_user.role
    }

@router.post("/login", response_model=schemas.TokenResponse)
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Endpoint para iniciar sesión desde el frontend.
    Recibe: username y password en JSON
    Devuelve: token JWT si las credenciales son correctas
    """
    # Busca el usuario en la base de datos
    user = db.query(models.User).filter(
        models.User.username == user_data.username
    ).first()

    # Verifica que el usuario exista y la contraseña sea correcta
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )

    # Genera el token JWT
    token = create_access_token({"sub": user.username, "role": user.role})

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }

@router.post("/token")
def login_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint especial para que Swagger UI pueda autenticarse.
    Usa el formato de formulario que espera OAuth2.
    """
    # Busca el usuario en la base de datos
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )

    token = create_access_token({"sub": user.username, "role": user.role})

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }