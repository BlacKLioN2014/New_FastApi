from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.rol_model import  Rol
from app.schemas.rol_schema import RolCreateResponse, RolCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/Crear", response_model=RolCreateResponse)
def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):

    existe = db.query(Rol).filter(Rol.nombre == rol.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="Rol ya registrado")

    # nuevo = Usuario(**usuario.model_dump(exclude_none=True))
    nuevo_rol = Rol(
                nombre=rol.nombre,
                descripcion=rol.descripcion,
                estado=rol.estado,
    )

    db.add(nuevo_rol)
    try :
        db.commit()
        db.refresh(nuevo_rol)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al guardar el rol")
    return {
        "message": "Se ha creado un nuevo rol",
        "rol": nuevo_rol
    }

