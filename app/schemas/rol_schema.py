from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class RolCreate(BaseModel):
    nombre: constr(min_length=3, max_length=50)
    descripcion: constr(min_length=5, max_length=255)
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