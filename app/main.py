from fastapi import  FastAPI
from app.routes import  saludos, usuarios, roles
from app.db.database  import  Base, engine
from app.models import  usuario_model, saludo_model, rol_model

app = FastAPI(
    title="API ---NoNe",
    description="Documentación interactiva de la API de pruebas con FastAPI y PostgreSQL",
    version="1.0.0",
    docs_url="/apidocs",
    redoc_url=None
)

# Crear tablas en la base si no existen
Base.metadata.create_all(bind=engine)

app.include_router(saludos.router, prefix="/saludos", tags=["Saludos"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(roles.router, prefix="/roles", tags=["Roles"])