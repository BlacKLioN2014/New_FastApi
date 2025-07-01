from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class UsuarioCreate(BaseModel):
    nombre_usuario: constr(min_length=3, max_length=15)
    correo_electronico: EmailStr
    contrasena: constr(min_length=6)
    estado: Optional[bool] = True
    ultimo_login: Optional[datetime] = None
    id_rol: int

class UsuarioLogin(BaseModel):
    correo_electronico: EmailStr
    contrasena: constr(min_length=6)

class UsuarioOut(BaseModel):
    id: int
    nombre_usuario: str
    correo_electronico: EmailStr
    estado: Optional[bool]
    ultimo_login: Optional[datetime]
    id_rol: int

class UsuarioCreateResponse(BaseModel):
    message: str
    usuario: UsuarioOut

class UsuarioLoginResponse(BaseModel):
    usuario: UsuarioOut
    token: str


class Config:
    from_attributes = True