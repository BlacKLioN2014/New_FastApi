from fastapi import APIRouter

from app.models.saludo_model import  Saludo

router = APIRouter()

@router.get("/saludo")
def decir_hola():
    return {"mensaje": "Hola mundo desde FastAPI"}

@router.post("/saludo")
def saludar_persona(data: Saludo):
    return {"mensaje": f"Hola {data.nombre}, bienvenido a FastAPI"}
