from fastapi import  FastAPI
from app.routes import  saludos

app = FastAPI()

app.include_router(saludos.router)