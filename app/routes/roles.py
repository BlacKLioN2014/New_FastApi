from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.rol_model import  Rol
from app.models.usuario_model import  Usuario
from app.schemas.rol_schema import RolCreateResponse, RolCreate, RolOut
from typing import List
from app.utils.auth import obtener_usuario_id
from app.utils.extensions import limiter

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/obtener", response_model=List[RolOut])
@limiter.limit("5/minute")
def obtener_roles(
        request: Request,
        db: Session = Depends(get_db),
        usuario_id: str = Depends(obtener_usuario_id)
):
    try :
        usuario = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="No se encontró token")
        roles =  db.query(Rol).all()
        return roles
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los roles: {str(e)}")

@router.post("/Crear", response_model=RolCreateResponse)
@limiter.limit("5/minute")
def crear_rol(
    request: Request,
    rol: RolCreate,
    db: Session = Depends(get_db),
    usuario_id: str = Depends(obtener_usuario_id)
):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="No se encontró token")

        existe = db.query(Rol).filter(Rol.nombre == rol.nombre).first()
        if existe:
            raise HTTPException(status_code=400, detail="Rol ya registrado")

        nuevo_rol = Rol(
            nombre=rol.nombre,
            descripcion=rol.descripcion,
            estado=rol.estado,
        )

        db.add(nuevo_rol)
        db.commit()
        db.refresh(nuevo_rol)

        return {
            "message": "Se ha creado un nuevo rol",
            "rol": nuevo_rol
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar el rol: {str(e)}")