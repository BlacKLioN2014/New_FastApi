from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.usuario_model import Usuario
from passlib.context import CryptContext
from app.schemas.usuario_schema import  UsuarioCreate, UsuarioCreateResponse, UsuarioOut, UsuarioLoginResponse, UsuarioLogin,UsuarioEditar
from typing import  List
from app.utils.jwt_manager import crear_token
from app.utils.auth import  obtener_usuario_id
from datetime import  datetime, timedelta,timezone
from app.utils.extensions import limiter

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
@limiter.limit("5/minute")
def crear_usuario(request: Request, usuario: UsuarioCreate, db: Session = Depends(get_db)):

    existe = db.query(Usuario).filter(Usuario.correo_electronico == usuario.correo_electronico).first()
    if existe:
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    hashed_password = hash_password(usuario.contrasena)

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
@limiter.limit("5/minute")
def login(request: Request, login_usuario: UsuarioLogin, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.correo_electronico == login_usuario.correo_electronico).first()
    if not usuario or not verify_password(login_usuario.contrasena, usuario.contrasena_hash):
        raise HTTPException(status_code=401, detail="Usuario y/o contraseña no válidos")

    usuario.ultimo_login = datetime.now(timezone.utc)
    try :
        db.commit()
        db.refresh(usuario)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al actualizar el usuario")
    token = crear_token({"sub": str(usuario.id)})

    return {
        "token": token ,
        "usuario": usuario,
        "token_type": "bearer",
        "expire": (datetime.now(timezone.utc) + timedelta(minutes=30)).isoformat()
    }

@router.get("/Obtener", response_model=List[UsuarioOut])
@limiter.limit("5/minute")
def obtener_usuarios(request: Request, db: Session = Depends(get_db),usuario_id: int = Depends(obtener_usuario_id)):
    try :
        usuario_token = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario_token:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if usuario_token.id_rol !=  1:
            raise HTTPException(status_code=403, detail="Usuario no autorizado")

        usuarios = db.query(Usuario).all()
        return usuarios

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los usuarios: {str(e)}")

@router.get("/Perfil", response_model=UsuarioOut)
@limiter.limit("5/minute")
def obtener_mi_perfil(request: Request, db: Session = Depends(get_db),usuario_id: int = Depends(obtener_usuario_id)):
    try :
        usuario_token = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario_token:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if not usuario_token.estado:
            raise HTTPException(status_code=403, detail="Usuario inactivo. No puede acceder al perfil.")

        return usuario_token

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener perfil: {str(e)}")

@router.put("/Editar", response_model=UsuarioCreateResponse)
@limiter.limit("5/minute")
def editar_usuarios(request: Request, usuario: UsuarioEditar, db: Session = Depends(get_db),usuario_id: str = Depends(obtener_usuario_id)):
    try :

        usuario_token = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()
        if not usuario_token:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if usuario_token.id_rol !=  1:
            raise HTTPException(status_code=403, detail="Usuario no autorizado")

        usuario_editar  = db.query(Usuario).filter(Usuario.id == int(usuario.id)).first()
        if not usuario_editar:
             raise HTTPException(status_code=404, detail="Usuario a editar no existe")

        usuario_correo_existe = db.query(Usuario).filter(
            Usuario.correo_electronico == usuario.correo_electronico, Usuario.id != usuario_editar.id).first()
        if usuario_correo_existe:
            raise HTTPException(status_code=400, detail="El nuevo correo electrónico ya está en uso por otro usuario")

        usuario_editar.nombre_usuario = usuario.nombre_usuario.strip()
        usuario_editar.correo_electronico = usuario.correo_electronico
        usuario_editar.contrasena_hash = hash_password(usuario.contrasena)
        usuario_editar.estado = usuario.estado
        usuario_editar.id_rol = usuario.id_rol

        db.commit()
        db.refresh(usuario_editar)

        return {
            "message":  f"Se ha actualizado el usuario con id {usuario_editar.id}",
            "usuario": usuario_editar
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al editar el usuario: {str(e)}")

@router.delete("/Eliminar", response_model=UsuarioCreateResponse)
@limiter.limit("5/minute")
def eliminar_usuarios(request: Request, id_usuario_eliminar: int, db: Session = Depends(get_db),usuario_id: str = Depends(obtener_usuario_id)):
    try :

        usuario_token = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()
        if not usuario_token:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if usuario_token.id_rol !=  1:
            raise HTTPException(status_code=403, detail="Usuario no autorizado")

        if usuario_token.id == id_usuario_eliminar:
            raise HTTPException(status_code=400, detail="No puedes eliminar tu propio usuario")

        usuario_eliminar  = db.query(Usuario).filter(Usuario.id == id_usuario_eliminar).first()
        if not usuario_eliminar:
             raise HTTPException(status_code=404, detail="Usuario a eliminar no existe")

        db.delete(usuario_eliminar)
        db.commit()

        return {
            "message":  f"Se ha eliminado el usuario con id {usuario_eliminar.id}",
            "usuario": usuario_eliminar
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar el usuario: {str(e)}")