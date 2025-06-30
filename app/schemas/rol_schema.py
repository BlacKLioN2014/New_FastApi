from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class RolCreate(BaseModel):
    nombre: str
    descripcion: str
    estado: Optional[bool] = True

class RolOut(BaseModel):
    id_rol: int
    nombre: str
    descripcion: str
    estado: Optional[bool]
    fecha_creacion: datetime

class RolCreateResponse(BaseModel):
    message: str
    rol: RolOut


    class Config:
        from_attributes = True