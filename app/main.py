from fastapi import  FastAPI, Request
from slowapi import  _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routes import  saludos, usuarios, roles
from app.db.database  import  Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.utils.extensions import limiter
# from app.models import  usuario_model, saludo_model, rol_model

app = FastAPI(
    title="New Api",
    description="Documentación interactiva de la API con FastAPI y PostgreSQL",
    version="1.0",
    docs_url="/apidocs",
    redoc_url=None
)

# orígenes permitidos
origins = [
    "http://localhost:3000",  # Ejemplo local
    "http://localhost:4200",  # Ejemplo local
    "https://tudominio.com"  # Producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # En desarrollo puedes usar ["*"]
    allow_credentials=True,
    allow_methods=["*"],           # Puedes restringir si lo deseas
    allow_headers=["*"],           # Por ejemplo, Authorization, Content-Type
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Crear tablas en la base si no existen
Base.metadata.create_all(bind=engine)

# app.include_router(saludos.router, prefix="/saludos", tags=["Saludos"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(roles.router, prefix="/roles", tags=["Roles"])