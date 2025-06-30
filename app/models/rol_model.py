from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import  relationship
from app.db.database import Base
from datetime import datetime, timezone

class Rol(Base):
    __tablename__ = "rol"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion= Column(String, nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    usuarios = relationship("Usuario", back_populates="rol")