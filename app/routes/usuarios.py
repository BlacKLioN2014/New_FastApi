from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.usuario_model import Usuario
from pydantic import BaseModel

router = APIRouter()

# Pydantic model para entrada de datos
class UsuarioInput(BaseModel):
    nombre: str
    contrasena: str

# Dependencia para obtener sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/usuario")
def crear_usuario(usuario: UsuarioInput, db: Session = Depends(get_db)):
    nuevo = Usuario(nombre=usuario.nombre, contrasena= usuario.contrasena)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
