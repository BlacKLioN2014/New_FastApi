from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.usuario_model import Usuario
from passlib.context import CryptContext
from app.schemas.usuario_schema import  UsuarioCreate, UsuarioCreateResponse

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash_password(password: str) -> str:
    return  pwd_context.hash(password)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/Crear", response_model=UsuarioCreateResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):

    existe = db.query(Usuario).filter(Usuario.correo_electronico == usuario.correo_electronico).first()
    if existe:
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    hashed_password = hash_password(usuario.contrasena)

    # nuevo = Usuario(**usuario.model_dump(exclude_none=True))
    nuevo_usuario = Usuario(
                nombre_usuario=usuario.nombre_usuario,
                correo_electronico=usuario.correo_electronico,
                contrasena=hashed_password,
                estado=usuario.estado,
                ultimo_login=usuario.ultimo_login,
                id_rol=usuario.id_rol
    )

    db.add(nuevo_usuario)
    try :
        db.commit()
        db.refresh(nuevo_usuario)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al guardar el usuario")
    return {
        "message": "Se ha creado un nuevo usuario",
        "usuario": nuevo_usuario
    }

