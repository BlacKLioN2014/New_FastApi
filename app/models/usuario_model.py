from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import  relationship
from app.db.database import Base
from datetime import datetime, timezone

class Usuario(Base):
    __tablename__ = "usuario"

    id= Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, nullable=False)
    correo_electronico = Column(String, nullable=False, unique=True)
    contrasena_hash = Column(String, nullable=False)
    fecha_registro = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)
    ultimo_login = Column(DateTime, nullable= True)

    id_rol = Column(Integer, ForeignKey("rol.id_rol"), nullable=False)

    rol = relationship("Rol", back_populates="usuarios")

