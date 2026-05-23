import logging
import time
from fastapi import Request

# Configuracion del sistema de logs fecha, nivel y mensaje
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Crea el logger con el nombre del modulo
logger = logging.getLogger(__name__)

async def log_requests(request: Request, call_next):
    """
    Middleware que se ejecuta en cada peticion que llega al servidor.
    Registra: método HTTP, ruta, tiempo de respuesta y codigo de estado.
    """
    start_time = time.time()  # Marca el tiempo de inicio

    # Deja pasar la peticion al endpoint correspondiente
    response = await call_next(request)

    # Calcula cuanto tardo en responder
    duration = (time.time() - start_time) * 1000  # En milisegundos

    # Intenta leer el rol del usuario desde los headers
    user_role = request.headers.get("X-User-Role", "no autenticado")

    # Escribe el log en consola
    logger.info(
        f"{request.method} {request.url.path} "
        f"- Status: {response.status_code} "
        f"- Duración: {duration:.2f}ms "
        f"- Rol: {user_role}"
    )

    return response