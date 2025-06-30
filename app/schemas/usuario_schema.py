from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioCreate(BaseModel):
    nombre_usuario: str
    correo_electronico: EmailStr
    contrasena: str  # sin hash
    estado: Optional[bool] = True
    ultimo_login: Optional[datetime] = None
    id_rol: int

class UsuarioOut(BaseModel):
    id_usuario: int
    nombre_usuario: str
    correo_electronico: EmailStr
    estado: Optional[bool]
    ultimo_login: Optional[datetime]
    id_rol: int

class UsuarioCreateResponse(BaseModel):
    message: str
    usuario: UsuarioOut


    class Config:
        from_attributes = True