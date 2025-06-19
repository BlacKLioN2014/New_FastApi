from fastapi import  FastAPI
from app.routes import  saludos, usuarios
from app.db.database  import  Base, engine
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Crear tablas en la base si no existen
Base.metadata.create_all(bind=engine)

app.include_router(saludos.router)
app.include_router(usuarios.router)