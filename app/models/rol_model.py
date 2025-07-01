from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import  relationship
from app.db.database import Base
from datetime import datetime, timezone
from enum import Enum

class Rol(Base):
    __tablename__ = "rol"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion= Column(String, nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    usuarios = relationship("Usuario", back_populates="rol")


class RolEnum(str, Enum):
    ADMINISTRADOR = "Administrador"
    MORTAL = "Mortal"
    DESCONOCIDO = "Número no reconocido"

def segun_rol(numero: int) -> Rol:
    match numero:
        case 1:
            return Rol.ADMINISTRADOR
        case 2:
            return Rol.MORTAL
        case _:
            return Rol.DESCONOCIDO