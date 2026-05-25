# Monitoring Innovation - Backend by Laura Reyes Arias

API REST para el sistema de gestion de vehiculos del concesionario hipotetico Monitoring Innovation.

## Demo
[https://prueba-backend-3lgp.onrender.com/docs](https://prueba-backend-3lgp.onrender.com/docs)

## Repositorio Frontend
[https://github.com/ltlauRarias/prueba-frontend](https://github.com/ltlauRarias/prueba-frontend)

## Tecnologias
- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- JWT

## Endpoints principales
| Metodo | Endpoint | Acceso | Descripcion |
|--------|----------|--------|-------------|
| POST | /api/auth/register | Publico | Registrar usuario |
| POST | /api/auth/login | Publico | Iniciar sesion |
| GET | /api/vehicles/ | Admin y Viewer | Listar vehiculos |
| POST | /api/vehicles/ | Solo Admin | Crear vehiculo |
| PUT | /api/vehicles/{id} | Solo Admin | Editar vehiculo |
| DELETE | /api/vehicles/{id} | Solo Admin | Eliminar vehiculo |

## Usuarios de prueba
> El plan gratuito de Render resetea la base de datos al reiniciarse o cada cierto tiempo. Si los usuarios no funcionan recomiendo crearlos nuevamente en [/docs](https://prueba-backend-3lgp.onrender.com/docs) usando el endpoint `/api/auth/register`.

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | admin123 | Admin - CRUD completo |
| viewer | viewer123 | Viewer - Solo lectura |

## Correr localmente
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Abrir en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
