from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.usuario_model import Usuario
from passlib.context import CryptContext
from app.schemas.usuario_schema import  UsuarioCreate, UsuarioCreateResponse, UsuarioOut, UsuarioLoginResponse, UsuarioLogin
from typing import  List
from app.utils.jwt_manager import crear_token
from app.models.rol_model import segun_rol, RolEnum
from app.utils.auth import  obtener_usuario_id
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash_password(password: str) -> str:
    return  pwd_context.hash(password)

# Verificar contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

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
                contrasena_hash=hashed_password,
                estado=usuario.estado,
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

@router.post('/Login', response_model=UsuarioLoginResponse)
def login(login_usuario: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.correo_electronico == login_usuario.correo_electronico).first()
    if not usuario or not verify_password(login_usuario.contrasena, usuario.contrasena_hash):
        raise HTTPException(status_code=401, detail="Usuario y/o contraseña no válidos")
    token = crear_token({"sub": str(usuario.id)})
    return {
        "token": token ,
        "usuario": usuario
    }

@router.get("/Obtener", response_model=List[UsuarioOut])
def obtener_usuarios( db: Session = Depends(get_db),usuario_id: str = Depends(obtener_usuario_id)):
    try :
        usuario = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        rol = segun_rol(usuario.id_rol)
        if rol ==  RolEnum.ADMINISTRADOR :
            usuarios = db.query(Usuario).all()
            return [UsuarioOut.model_validate(u) for u in usuarios]
        else:
            raise HTTPException(status_code=403, detail="Usuario no autorizado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los usuarios: {str(e)}")

# @router.get("/Eliminar", response_model=UsuarioOut)
# def Eliminar_usuarios( db: Session = Depends(get_db)):
#     try :
#         usuarios =  db.query(Usuario).all()
#         return usuarios
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error al obtener los usuarios: {str(e)}")

